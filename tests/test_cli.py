from subprocess import Popen, PIPE


def test_md5_csv():
    p = Popen(['diffino', 'before_dataset.csv', 'after_dataset.csv', '--mode', 'md5'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_md5_zip():
    p = Popen(['diffino', 'before_dataset.zip', 'after_dataset.zip', '--mode', 'md5'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_s3_csv():
    p = Popen(['diffino', 's3://bucket/before_dataset.csv', 's3://bucket/after_dataset.csv', '--mode', 'md5'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_s3_bucket_md5():
    p = Popen(['diffino', 's3://bucket/before_dataset', 's3://bucket/after_dataset', '--mode', 'md5'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_csv():
    p = Popen(['diffino', 'before_dataset.csv', 'after_dataset.csv', '--mode', 'pandas'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_csv_numeric_false():
    p = Popen(['diffino', 'before_dataset.csv', 'after_dataset.csv', '--mode', 'pandas', '--convert-numeric', 'false'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_csv_cols():
    p = Popen(['diffino before_dataset.csv', 'after_dataset.csv', '--mode pandas', '--cols', 'id', 'name'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_output_csv_local():
    p = Popen(['diffino', 'file_1.csv', 'file_2.csv', '--output', 'diff.csv'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_output_xlsx_local():
    p = Popen(['diffino', 'file_1.csv', 'file_2.csv', '--output', 'diff.xlsx'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_output_json_local():
    p = Popen(['diffino', 'file_1.csv', 'file_2.csv', '--output', 'diff.json'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_output_csv_s3():
    p = Popen(['diffino', 'file_1.csv', 'file_2.csv', '--output', 's3://bucket/diff.csv'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_output_xlsx_s3():
    p = Popen(['diffino', 'file_1.csv', 'file_2.csv', '--output', 's3://bucket/diff.xlsx'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')


def test_pandas_output_json_s3():
    p = Popen(['diffino', 'file_1.csv', 'file_2.csv', '--output', 's3://bucket/diff.json'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    raise Exception('Finish test!')
