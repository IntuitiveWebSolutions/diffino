import pandas as pd


class DataSet:
    dfs = []
    md5_hashes = []

    def __init__(self, location, index_col, cols):
        self.location = location
        self.index_col = index_col
        self.cols = cols

    # Private methods
    def _get_from_local_file(self):
        if len(self.cols):
            return pd.read_csv(self.location, index_col=self.index_col, usecols=self.cols)
        return pd.read_csv(self.location, index_col=self.index_col)

    def _get_from_local_dir(self):
        self._get_from_local_file()

    def _get_from_s3_file(self):
        raise NotImplementedError

    def _get_from_s3_bucket(self):
        raise NotImplementedError

    def _get_from_zip_local_file(self):
        # Unzip
        raise NotImplementedError

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
    @param index_col: Column to be used as index
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
        self.index_col = kwargs.get('index_col', False)

        self.diff_result_left = {}
        self.diff_result_right = {}

    # Private methods
    def _build_inputs(self):
        self._left_dataset = self._build_input(self.left)
        self._right_dataset = self._build_input(self.right)

    def _build_input(self, dataset_location):
        return DataSet(dataset_location, self.index_col, self.cols).read()

    def to_csv(self, s3=False):
        output_name = self.output.replace('.csv', '')
        output_left = output_name + '_left.csv'
        output_right = output_name + '_right.csv'

        self.diff_result_left.to_csv(output_left)
        self.diff_result_right.to_csv(output_right)

    def to_excel(self, s3=False):
        raise NotImplementedError

    def to_json(self, s3=False):
        raise NotImplementedError

    def to_console(self):
        print('===============Left Output===============')
        print(self.diff_result_left.to_string())

        print('===============Right Output===============')
        print(self.diff_result_right.to_string())

    def _build_output(self):
        if not self.output:
            self.to_console()
            return
        if '.csv' in self.output:
            if 's3://' in self.output:
                self.to_csv(s3=True)
            else:
                self.to_csv(s3=False)
        elif '.xslx' in self.output or '.xls' in self.output:
            if 's3://' in self.output:
                self.to_excel(s3=True)
            else:
                self.to_excel(s3=False)
        elif '.json' in self.output:
            if 's3://' in self.output:
                self.to_json(s3=True)
            else:
                self.to_json(s3=False)
        else:
            raise UserWarning('Invalid output format')
        self._output_dataset = None

    # Public methods
    def build_diff(self):
        if not self.left or not self.right:
            print('{}, {}'.format(self.left, self.right))
            raise UserWarning('Left and right datasets are both required')

        self._build_inputs()

        merged_dataset = pd.merge(left=self._left_dataset, right=self._right_dataset, how='outer',
                     left_index=True, right_index=True, suffixes=['_left', '_right'])

        self.diff_result_left = merged_dataset.drop(self._left_dataset.index)
        self.diff_result_right = merged_dataset.drop(self._right_dataset.index)

        self._build_output()
