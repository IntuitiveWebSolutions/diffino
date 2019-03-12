import pandas as pd


class DataSet:
    dfs = []
    md5_hashes = []

    def __init__(self, location):
        self.location = location

    # Private methods
    def _get_from_local_file(self):
        self.dfs
        self.md5_hashes

    def _get_from_local_dir(self):
        self._get_from_local_file()

    def _get_from_s3_file(self):
        self.dfs
        self.md5_hashes

    def _get_from_s3_bucket(self):
        self._get_from_local_file()

    def _get_from_zip_local_file(self):
        # Unzip
        self._get_from_local_file()

    # Public methods
    def read(self):
        if 's3://' in self.location:
            if '/' in self.location:
                return self._get_from_s3_bucket()
            else:
                return self. _get_from_s3_file()
        else:
            if '/' in self.location:
                return self._get_from_local_dir()
            else:
                return self._get_from_local_file()


class Diffino:
    '''
    Main class that provides the diff functionalities. Specific dataset types (CSV, XLSX, etc)
    are provided by classes inheriting from DataSet

    @param left: String with the input dataset to be used (.csv, .xlsx, .xls for local files and s3 url plus extension for AWS S3)
    @param right: String with the other input dataset to compare against (.csv, .xlsx, .xls for local files and s3 url plus extension for AWS S3)
    @param output: String with the output location (.csv, .xlsx, .xls, .json for local files and s3 url plus extension for AWS S3)
    @param convert_numeric: Boolean indicating whether numeric columns should be treated as numbers (in pandas mode).
    @param mode: String with the diff mode: 'pandas' or 'md5'
    @param cols: List with subset of columns to be used for the diff check.
    @return: Nothing is returned
    '''
    def __init__(self, **kwargs):
        self.left, self._left_dataset = kwargs.get('left'), None
        self.right, self._right_dataset = kwargs.get('right'), None
        self.output, self._output_dataset = kwargs.get('output'), None
        self.convert_numeric = kwargs.get('convert_numeric', True)
        self.mode = kwargs.get('mode', 'pandas')
        self.cols = kwargs.get('cols')
        self.cols_left = kwargs.get('cols_left')
        self.cols_right = kwargs.get('cols_right')

        self.diff_results = {}

    # Private methods
    def _build_inputs(self):
        self._left_dataset = self._build_input(self.left)
        self._right_dataset = self._build_input(self.right)

    def _build_input(self, dataset_location):
        return DataSet(location=dataset_location).read()

    def to_csv(self, s3=False):
        pass

    def to_excel(self, s3=False):
        pass

    def to_json(self, s3=False):
        pass

    def _build_output(self, dataset_location):
        if not self.output:
            return False
        if '.csv' in dataset_location:
            if 's3://' in dataset_location:
                self.to_csv(s3=True)
            else:
                self.to_csv(s3=False)
        elif '.xslx' in dataset_location or '.xls' in dataset_location:
            if 's3://' in dataset_location:
                self.to_excel(s3=True)
            else:
                self.to_excel(s3=False)
        elif '.json' in dataset_location:
            if 's3://' in dataset_location:
                self.to_json(s3=True)
            else:
                self.to_json(s3=False)
        else:
            raise UserWarning('Invalid output format')
        self._output_dataset = None

    # Public methods
    def build_diff(self):
        if not self.left or not self.right:
            print '{}, {}'.format(self.left, self.right)
            raise UserWarning('Left and right datasets are both required')
        self._build_inputs()
        if self._left_dataset.md5_hashes:
            # compare self._left_dataset.md5_hashes with right one
            # { 'row_1': 'MD5-1', 'row_2': 'MD5-2'}
            self.diff_results = {}
        elif self._left_dataset.dfs:
            # compare self._left_dataset.dfs with right one
            self.diff_results = pd.DataFrame()
        self._build_output()
        return self.diff_results
