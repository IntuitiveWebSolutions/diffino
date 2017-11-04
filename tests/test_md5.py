from diffino.models import Diffino


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


def test_output_csv_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.csv')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_xlsx_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.xslx')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_json_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv', output='/tmp/diff.json')
    diff.build_diff()
    raise Exception('Finish test!')


def test_output_in_s3_md5():
    diff = Diffino(mode='md5', left='/tmp/one.csv', right='/tmp/two.csv', output='s3://fake-bucket/diff.json')
    diff.build_diff()
    raise Exception('Finish test!')
