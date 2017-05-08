## Models

Dataset
- local_filename
- s3_location

CSVDataset < Dataset
- separator

XLSXDataset < Dataset
- sheet_name
- skip_cols

Differ
- inputs
- outputs
- convert_numeric
- mode
- cols
- _guess_inputs()
- _guess_output()
- _validate_inputs_outputs_match()
