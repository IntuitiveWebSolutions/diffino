![](https://raw.githubusercontent.com/ivansabik/diffino/master/doc/diffino_icon.png) Diffino
====
[![Run Status](https://api.shippable.com/projects/590fc79a8874ee070046b384/badge?branch=master)](https://app.shippable.com/github/ivansabik/diffino)
[![Coverage Badge](https://api.shippable.com/projects/590fc79a8874ee070046b384/coverageBadge?branch=master)](https://app.shippable.com/github/ivansabik/diffino)

Diffing tools for comparing datasets in CSV, XLSX and other formats available as CLI app, API, web app and module. Powered by the awesome Pandas library for Python.

- Compare one or more CSV datasets using MD5, you can output differences to terminal or as CSV, XLSX or JSON
- Compare one or more CSV and XLSX datasets using Pandas where you can output differences row by row
- Use the following inputs for your datasets:
  - Local file in CSV (for both MD5 and pandas modes)
  - Local file in CSV or XLSX (only for pandas mode)
  - Local directory with CSVs or XSLX files (for both MD5 and pandas modes)
  - ZIP file with CSVs or XLSX files (only for pandas mode)
  - File in S3 (for both MD5 and pandas modes)
  - Bucket in S3 (for both MD5 and pandas modes)
- Define a subset of columns to use for comparing/diffing (only works with pandas mode, not supported for MD5 comparison)
- Output differences to:
  - Console (print)
  - CSV file
  - XSLX file
  - JSON file

## Install

To install as module and CLI:

```
pip install diffino
```

To run the API and web app first change any configuration params you need in `docker-compose.yml`

```
docker-compose up
```

## CLI

Diffino will try it's best to guess your input storage mechanisms, for that you need to include `s3://` in the input argument and/or the `.csv`, `.xls` and `.xlsx extensions`.

### Compare using MD5

#### Compare two CSV files using MD5 hash of both files

```
diffino before_dataset.csv after_dataset.csv --mode md5
```

#### Compare CSV files in two directories recursively using MD5 hashes of the files

Diffino will compare files with the same name in both folders recursively:

```
diffino before_dataset after_dataset --mode md5
```

#### Compare CSV files in two ZIP files recursively using MD5 hashes of the files

Diffino will compare files with the same name in both ZIP files recursively:

```
diffino before_dataset.zip after_dataset.zip --mode md5
```

#### Compare two CSV files in an S3 bucket using MD5 hash of both files

```
diffino s3://bucket/before_dataset.csv s3://bucket/after_dataset.csv --mode md5
```

#### Compare CSV files in an S3 bucket recursively using MD5 hashes of the files

```
diffino s3://bucket/before_dataset s3://bucket/after_dataset --mode md5
```

### Compare using pandas

MD5 is only useful for knowing two CSV datasets are not the same but it's not useful for knowing which are the actual differences among those. For that you can use the pandas mode which will output the differences row by row.
The same commands shown earlier for MD5 are available, you need to pass the `--mode pandas` argument for using pandas. **By default Pandas mode is used so this argument can be omitted**:

```
diffino before_dataset.csv after_dataset.csv  --mode pandas
```

When using pandas mode, by default Diffino will try to convert numeric columns, you can change this behavior with:

```
diffino before_dataset.csv after_dataset.csv --convert-numeric false
```

You can define the columns to be used for checking the diffs:

```
diffino before_dataset.csv after_dataset.csv --cols="['id', 'name']"
```

### Output diff results to file

Diffino will try it's best to guess your output storage mechanism, for that you need to include `s3://` in the input argument or use the `.csv`, `.xls` and `.xlsx extensions`.

#### Output to a local CSV file
```
diffino file_1.csv file_2.csv --output diff.csv
```

#### Output to a local Excel file

When using Excel, output will contain different sheets as well as one summary sheet containing all differences:

```
diffino file_1.csv file_2.csv --output diff.xlsx
```

#### Output to a local JSON file

```
diffino file_1.csv file_2.csv --output diff.json
```

#### Output to an CSV file in S3

```
diffino file_1.csv file_2.csv --output s3://bucket/diff.csv
```

#### Output to an Excel file in S3
When using Excel, output will contain different sheets as well as one summary sheet containing all differences:

```
diffino file_1.csv file_2.csv --output s3://bucket/diff.xlsx
```

#### Output to a JSON file in S3

```
diffino file_1.csv file_2.csv --output s3://bucket/diff.json
```

## Python module

Useful if you want to integrate as part of you ETL or as part of you Continuous Integration (CI) builds.

### Get a dictionary with differences using MD5 mode

```python
from diffino.models import Diffino

diffino = Diffino(left_input='one.csv', right_input='two.csv', mode='md5')
results = diffino.build_diff()
```

In the above example, the `results` variable contains a dictionary with differences:

```python
results['left_only']
results['right_only']
results['both']
```

### Get a dictionary with differences using pandas mode
For using all columns:

```python
from diffino.models import Diffino

diffino = Diffino(left_input='s3://bucket/one.csv', right_input='s3://bucket/two.csv', mode='pandas')
results = diffino.build_diff()
```

And for using a subset of columns you can specify a string with a Python list of the column names you want to include:

```python
from diffino.models import Diffino

diffino = Diffino(
  left_input='one.xlsx',
  right_input='two.xlsx',
  mode='pandas',
  cols=['id', 'name']
)
results = diffino.build_diff()
```

## Web App

Coming soon

## API

Coming soon

## License

**MIT** check external dependencies for their respective licenses. <a href="https://icons8.com">Icon pack by Icons8</a>
