from io import BytesIO
import logging
import boto3
import pandas as pd
from urlparse import urlparse

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


def get_bucket_and_key_from_s3_path(path):
    o = urlparse(path, allow_fragments=False)
    return (o.netloc, o.path.lstrip("/"))


class DataSet:
    dfs = []
    md5_hashes = []

    def __init__(self, location, cols, convert_numeric):
        self.location = location
        self.cols = cols
        self.convert_numeric = convert_numeric

    # Private methods
    def _get_from_local_file(self):
        logging.info("Reading local file %s", self.location)
        return pd.read_csv(self.location, usecols=self.cols)

    def _get_from_local_dir(self):
        return self._get_from_local_file()

    def _get_from_s3_file(self):
        logging.info("Reading from S3 %s", self.location)
        bucket_key = get_bucket_and_key_from_s3_path(self.location)

        s3 = boto3.client("s3")
        obj = s3.get_object(Bucket=bucket_key[0], Key=bucket_key[1])
        return pd.read_csv(obj["Body"], usecols=self.cols)

    def _get_from_s3_bucket(self):
        raise NotImplementedError

    def _get_from_zip_local_file(self):
        # Unzip
        raise NotImplementedError

    # Public methods
    def read(self):
        df = None
        if "s3://" in self.location:
            if self.location.endswith("/"):
                df = self._get_from_s3_bucket()
            else:
                df = self._get_from_s3_file()
        else:
            if "/" in self.location:
                df = self._get_from_local_dir()
            else:
                df = self._get_from_local_file()

        if self.convert_numeric:
            logging.info("Converting to numeric for file %s", self.location)
            df.apply(pd.to_numeric, errors="ignore")
        return df


class Diffino:
    """
    Main class that provides the diff functionalities. Specific dataset types (CSV, XLSX, etc)
    are provided by classes inheriting from DataSet

    @param left: String with the input dataset to be used (.csv, .xlsx, .xls for local files and s3 url plus extension for AWS S3)
    @param right: String with the other input dataset to compare against (.csv, .xlsx, .xls for local files and s3 url plus extension for AWS S3)
    @param output: String with the output location (.csv, .xlsx, .xls, .json for local files and s3 url plus extension for AWS S3)
    @param convert_numeric: Boolean indicating whether numeric columns should be treated as numbers (in pandas mode).
    @param mode: String with the diff mode: 'pandas' or 'md5'
    @param cols: List with subset of columns to be used for the diff check.
    @param index_col: Column to be used as index
    @return: Nothing is returned
    """

    def __init__(self, **kwargs):
        self.left, self._left_dataset = kwargs.get("left"), None
        self.right, self._right_dataset = kwargs.get("right"), None
        self.output, self._output_dataset = kwargs.get("output"), None
        self.convert_numeric = kwargs.get("convert_numeric", True)
        self.mode = kwargs.get("mode", "pandas")
        self.cols = kwargs.get("cols")
        self.cols_left = kwargs.get("cols_left")
        self.cols_right = kwargs.get("cols_right")
        self.output_only_diffs = kwargs.get("output_only_diffs")

        self.diff_result_left = {}
        self.diff_result_right = {}

    # Private methods
    def _build_inputs(self):
        logging.info("Building inputs")
        self._left_dataset = self._build_input(self.left)
        self._right_dataset = self._build_input(self.right)

    def _build_input(self, dataset_location):
        logging.info("Building dataset for %s", dataset_location)
        return DataSet(dataset_location, self.cols, self.convert_numeric).read()

    def _should_print_left(self):
        return not self.diff_result_left.empty or (
            self.diff_result_left.empty and not self.output_only_diffs
        )

    def _should_print_right(self):
        return not self.diff_result_right.empty or (
            self.diff_result_right.empty and not self.output_only_diffs
        )

    def _save_csv(self, df, output_file, s3=False):
        if not s3:
            logging.info("Saving result csv file %s", output_file)
            df.to_csv(output_file, index=False)
            return

        logging.info("Saving result csv file %s to S3", output_file)

        bucket_key = get_bucket_and_key_from_s3_path(output_file)
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        s3client = boto3.client("s3")
        response = s3client.put_object(
            Body=csv_buffer.getvalue(),
            ContentType="application/vnd.ms-excel",
            Bucket=bucket_key[0],
            Key=bucket_key[1],
        )

    def to_csv(self, s3=False):
        output_name = self.output.replace(".csv", "")

        if self._should_print_left():
            output_left = output_name + "_not_in_right.csv"
            self._save_csv(self.diff_result_left, output_left, s3)

        if self._should_print_right():
            output_right = output_name + "_not_in_left.csv"
            self._save_csv(self.diff_result_right, output_right, s3)

    def to_excel(self, s3=False):
        raise NotImplementedError

    def to_json(self, s3=False):
        raise NotImplementedError

    def to_console(self):
        if self._should_print_left():
            print("=============== Differences found on left file ===============")
            print(self.diff_result_left.to_string())

        if self._should_print_right():
            print("=============== Differences found on right file ===============")
            print(self.diff_result_right.to_string())

    def _build_output(self):
        logging.info("Building output started")
        if not self.output:
            logging.info("Building output to console")
            self.to_console()
            return
        if ".csv" in self.output:
            logging.info("Building output to csv")
            if "s3://" in self.output:
                self.to_csv(s3=True)
            else:
                self.to_csv(s3=False)
        elif ".xslx" in self.output or ".xls" in self.output:
            logging.info("Building output to Excel")
            if "s3://" in self.output:
                self.to_excel(s3=True)
            else:
                self.to_excel(s3=False)
        elif ".json" in self.output:
            logging.info("Building output to json")
            if "s3://" in self.output:
                self.to_json(s3=True)
            else:
                self.to_json(s3=False)
        else:
            raise UserWarning("Invalid output format")
        self._output_dataset = None

    # Public methods
    def build_diff(self):
        if not self.left or not self.right:
            print("{}, {}".format(self.left, self.right))
            raise UserWarning("Left and right datasets are both required")

        self._build_inputs()

        logging.info("Performing merge of datasets in preparation for diff")
        merged_dataset = pd.merge(
            left=self._left_dataset,
            right=self._right_dataset,
            how="outer",
            indicator="exists",
        )

        exists_left = merged_dataset["exists"] == "left_only"
        exists_right = merged_dataset["exists"] == "right_only"

        logging.info("Creating diff result left")
        self.diff_result_left = merged_dataset[exists_left].drop(["exists"], axis=1)

        logging.info("Creating diff result right")
        self.diff_result_right = merged_dataset[exists_right].drop(["exists"], axis=1)

        self._build_output()

        return (len(self.diff_result_left.index), len(self.diff_result_right.index))
