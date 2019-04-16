import io
import os
import pandas as pd
from pathlib import Path
from diffino.models import DataSet, Diffino
from pandas.testing import assert_frame_equal

class TestModels(object):
  def _create_diff(self, target_dir, left_csv='sample_left.csv', right_csv='sample_right.csv',
                  to_console=False, cols=None):
    output_location = False if to_console else os.path.join(target_dir, 'output.csv')
    output_left = os.path.join(target_dir, 'output_not_in_left.csv')
    output_right = os.path.join(target_dir, 'output_not_in_right.csv')

    location_left = fname = os.path.join(os.path.dirname(__file__), left_csv)
    location_right = fname = os.path.join(os.path.dirname(__file__), right_csv)
    diffino = Diffino(left=location_left, right=location_right, output=output_location, cols=cols)

    diffino.build_diff()

    if not to_console:
      path_left = Path(output_left)
      path_right = Path(output_right)
      assert path_left.is_file()
      assert path_right.is_file()
    return output_location, output_left, output_right

  def test_dataset_read_from_local_file(self):
    location = fname = os.path.join(os.path.dirname(__file__), 'sample_left.csv')
    dataset = DataSet(location, None, False)
    df = dataset.read()
    assert isinstance(df, pd.DataFrame)
    assert df.empty is not True
  
  def test_diffino_diff_is_working(self, tmpdir):
    outputs = self._create_diff(tmpdir)

    expected_data_not_in_left = """,address,state,zip,name,id
10,eleven st,CA,66611,name eleven,11"""

    expected_data_not_in_right = """,address,state,zip,name,id
9,ten st,CA,66610,name ten,10"""

    expected_df_not_in_left = pd.read_csv(io.StringIO(expected_data_not_in_left))
    expected_df_not_in_right = pd.read_csv(io.StringIO(expected_data_not_in_right))

    result_not_in_left = pd.read_csv(outputs[1])
    result_not_in_right = pd.read_csv(outputs[2])

    assert_frame_equal(expected_df_not_in_left, result_not_in_left)
    assert_frame_equal(expected_df_not_in_right, result_not_in_right)

  def test_diffino_no_diff(self, tmpdir):
    outputs = self._create_diff(tmpdir, right_csv='sample_left.csv')

    expected_data = ',address,state,zip,name,id'

    expected_df = pd.read_csv(io.StringIO(expected_data))
    resulting_left_csv = pd.read_csv(outputs[1])
    resulting_right_csv = pd.read_csv(outputs[2])

    assert_frame_equal(expected_df, resulting_left_csv, check_dtype=False)
    assert_frame_equal(expected_df, resulting_right_csv, check_dtype=False)
  
  def test_diffino_build_output_to_console(self, tmpdir, capsys):
    self._create_diff(tmpdir, to_console=True)
    captured = capsys.readouterr()
    assert 'Left Output' in captured.out
    assert 'Right Output' in captured.out
  
  def test_diffino_diff_with_selected_columns(self, tmpdir):
    outputs = self._create_diff(tmpdir, cols=['address', 'id'])

    expected_data_right = """,address,id
9,ten st,10"""
    expected_data_left = """,address,id
10,eleven st,11"""

    expected_df_left = pd.read_csv(io.StringIO(expected_data_left))
    expected_df_right = pd.read_csv(io.StringIO(expected_data_right))
    resulting_left_csv = pd.read_csv(outputs[1])
    resulting_right_csv = pd.read_csv(outputs[2])

    assert_frame_equal(expected_df_left, resulting_left_csv, check_dtype=False)
    assert_frame_equal(expected_df_right, resulting_right_csv, check_dtype=False)
