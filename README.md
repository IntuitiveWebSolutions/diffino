diffino
====
[![Build Status](https://travis-ci.com/IntuitiveWebSolutions/diffino.svg?branch=master)](https://travis-ci.com/IntuitiveWebSolutions/diffino)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Diffing tools for comparing datasets in CSV, XLSX and other formats available as CLI app, API, web app and module. Powered by the awesome Pandas library for Python.

### Done
- Install as CLI app
- Install and use as python module
- Compare two CSV datasets using Pandas where you can output differences row by row
- Use the following inputs for your datasets:
  - Local file in CSV pandas modes
  - File in S3 pandas mode
- Define a subset of columns to use for comparing/diffing (only works with pandas mode, not supported for MD5 comparison)
- Output differences to:
  - Console (print)
  - CSV file

### To-Do (ROADMAP)
- Compare one or more CSV datasets using MD5 hash of the files
- Compare one or more XLSX datasets using Pandas where you can output differences row by row
- Use the following inputs for your datasets:
  - Local file in CSV MD5
  - Local file in XLSX (only for pandas mode)
  - Local directory with CSVs or XSLX files (for both MD5 and pandas modes)
  - ZIP file with CSVs or XLSX files (only for pandas mode)
  - File in S3 for MD5
  - Bucket in S3 (for both MD5 and pandas modes)
- Output differences to:
  - XSLX file
  - JSON file

## Install

To install as module and CLI:

```
pip install diffino
```

## CLI

Diffino will try it's best to guess your input storage mechanisms, for that you need to include `s3://` in the input argument and/or the `.csv`, `.xls` and `.xlsx extensions`.

### Compare using pandas

MD5 is only useful for knowing two CSV datasets are not the same but it's not useful for knowing which are the actual differences among those. For that you can use the pandas mode which will output the differences row by row.
The same commands shown earlier for MD5 are available, you need to pass the `--mode pandas` argument for using pandas. **By default Pandas mode is used so this argument can be omitted**:

```
diffino before_dataset.csv after_dataset.csv --mode pandas
```

When using pandas mode, by default Diffino will try to convert numeric columns, you can change this behavior with:

```
diffino before_dataset.csv after_dataset.csv --convert-numeric false
```

You can define the columns to be used for checking the diffs:

```
diffino before_dataset.csv after_dataset.csv --cols id name
```

#### Compare two CSV files in an S3 bucket using pandas mode

```
diffino s3://bucket/before_dataset.csv s3://bucket/after_dataset.csv --mode pandas
```

### Output diff results to file

Diffino will try it's best to guess your output storage mechanism, for that you need to include `s3://` in the input argument or use the `.csv`, `.xls` and `.xlsx extensions`.

#### Output to a local CSV file
```
diffino file_1.csv file_2.csv --output diff.csv
```

Note: Two files are going to be generated, comparing the left argument file to the right argument file. For the example above, 2 files are going to be created:

* `diff_left.csv`
* `diff_right.csv`

#### Avoid creating unnecesary files

If you want to avoid unnecesary noise, you can prevent diffino from creating resulting files if there are no actual differences with the `--output-only-diffs` like
```
diffino file_1.csv file_2.csv --output diff.csv
```

For the above example, if `file_1` has some extra rows that are not present in `file_2`, but `file_2` only have rows that are present in `file_1`, then we are going to end up only with a resulting `diff_left.csv` file.


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

### Get a dictionary with differences using pandas mode
For using all columns:

```python
from diffino.models import Diffino

diffino = Diffino(left='s3://bucket/one.csv', right='s3://bucket/two.csv', mode='pandas')
results = diffino.build_diff()
```

In the above example, the `results` variable contains a tuple with the first index containing
the left differences count and the second index with the right differences count:

```python
results(0)
results(1)
```

And for using a subset of columns you can specify a string with a Python list of the column names you want to include:

```python
from diffino.models import Diffino

diffino = Diffino(
  left='one.csv',
  right='two.csv',
  mode='pandas',
  cols=['id', 'name']
)
results = diffino.build_diff()
```

## COMING SOON
Different column names? No problemo that works too! 

```python
from diffino.models import Diffino

diffino = Diffino(
  left='one.xlsx',
  right='two.xlsx',
  mode='pandas',
  left_cols=['myColumn'],
  right_cols=['my_column'],
)
results = diffino.build_diff()
```

## Web App

Coming soon

## API

Coming soon
