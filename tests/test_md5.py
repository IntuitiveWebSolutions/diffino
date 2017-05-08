from diffino.models import Diffino


# MD5
def test_single_file_csv_local_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv')
    results = diff.build_diff()
    assert results


def test_single_file_excel_local_md5():
    diff = Diffino(mode='md5', left='/tmp/one.xlsx', right='/tmp/two.xlsx')
    results = diff.build_diff()
    assert results


def test_single_file_csv_s3_md5():
    diff = Diffino(mode='md5', left='s3://fake-bucket/one.csv', right='s3://fake-bucket/two.csv')
    results = diff.build_diff()
    assert results


def test_single_file_excel_s3_md5():
    diff = Diffino(mode='md5', left='s3://fake-bucket/one.xlsx', right='s3://fake-bucket/two.xlsx')
    results = diff.build_diff()
    assert results


def test_multiple_files_dir_md5():
    diff = Diffino(mode='md5', left='/tmp/one', right='/tmp/two')
    results = diff.build_diff()
    assert results


def test_multiple_files_zip_md5():
    diff = Diffino(mode='md5', left='/tmp/one.zip', right='/tmp/two.zip')
    results = diff.build_diff()
    assert results


def test_multiple_files_s3_md5():
    diff = Diffino(mode='md5', left='s3://fake-bucket/one', right='s3://fake-bucket/two')
    results = diff.build_diff()
    assert results


# Pandas
def test_single_file_csv_local_pandas():
    diff = Diffino(mode='pandas', left='/tmp/one.csv', right='/tmp/two.csv')
    results = diff.build_diff()
    assert results


def test_single_file_excel_local_pandas():
    diff = Diffino(mode='pandas', left='/tmp/one.xlsx', right='/tmp/two.xlsx')
    results = diff.build_diff()
    assert results


def test_single_file_csv_s3_pandas():
    diff = Diffino(mode='pandas', left='s3://fake-bucket/one.csv', right='s3://fake-bucket/two.csv')
    results = diff.build_diff()
    assert results


def test_multiple_files_dir_pandas():
    diff = Diffino(mode='pandas', left='/tmp/one', right='/tmp/two')
    results = diff.build_diff()
    assert results


def test_multiple_files_zip_pandas():
    diff = Diffino(mode='pandas', left='/tmp/one.zip', right='/tmp/two.zip')
    results = diff.build_diff()
    assert results


def test_multiple_files_s3_pandas():
    diff = Diffino(mode='pandas', left='s3://fake-bucket/one', right='s3://fake-bucket/two')
    results = diff.build_diff()
    assert results


# Specific features for pandas
def test_specific_cols():
    diff = Diffino(mode='pandas', left='/tmp/one.csv', right='/tmp/two.csv', cols=['id', 'name'])
    results = diff.build_diff()
    assert results


def test_convert_numeric():
    diff = Diffino(mode='pandas', left='/tmp/one_specific_cols.csv', right='/tmp/two_specific_cols.csv', convert_numeric=False)
    results = diff.build_diff()
    assert results


# Save diff results to output
def test_output_csv_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.csv')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_csv_pandas():
    diff = Diffino(mode='pandas', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.csv')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_xlsx_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.xslx')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_xlsx_pandas():
    diff = Diffino(mode='pandas', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.xslx')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_json_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.json')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_json_pandas():
    diff = Diffino(mode='pandas', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.json')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_in_s3_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv', output='s3://fake-bucket/diff.json')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_in_s3_pandas():
    diff = Diffino(mode='pandas', left='/tmp/one.csv', right='/tmp/two.csv', output='s3://fake-bucket/diff.json')
    diff.build_diff()
    raise Exception('Finish test!')
