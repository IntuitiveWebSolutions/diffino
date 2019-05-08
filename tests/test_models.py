import io
import os
import numpy as np
import numpy.testing as npt
import pandas as pd
from diffino.models import DataSet, Diffino


def assert_frames_equal(actual, expected):
    """
    Compare DataFrame items by index and column and
    raise AssertionError if any item is not equal.

    Ordering is unimportant, items are compared only by label.
    NaN and infinite values are supported.
    
    Parameters
    ----------
    actual : pandas.DataFrame
    expected : pandas.DataFrame

    """
    comp = npt.assert_equal

    assert isinstance(actual, pd.DataFrame) and isinstance(
        expected, pd.DataFrame
    ), "Inputs must both be pandas DataFrames."

    for i, exp_row in expected.iterrows():
        assert i in actual.index, "Expected row {!r} not found.".format(i)

        act_row = actual.loc[i]

        for j, exp_item in exp_row.iteritems():
            assert j in act_row.index, "Expected column {!r} not found.".format(j)

            act_item = act_row[j]

            try:
                comp(act_item, exp_item)
            except AssertionError as e:
                raise AssertionError(
                    e.message + "\n\nColumn: {!r}\nRow: {!r}".format(j, i)
                )


class TestModels(object):
    def _create_diff(
        self,
        target_dir,
        left_csv="sample_left.csv",
        right_csv="sample_right.csv",
        to_console=False,
        cols=None,
        output_only_diffs=False,
    ):
        output_location = (
            False if to_console else os.path.join(target_dir, "output.csv")
        )
        output_left = os.path.join(target_dir, "output_not_in_left.csv")
        output_right = os.path.join(target_dir, "output_not_in_right.csv")

        location_left = fname = os.path.join(os.path.dirname(__file__), left_csv)
        location_right = fname = os.path.join(os.path.dirname(__file__), right_csv)
        diffino = Diffino(
            left=location_left,
            right=location_right,
            output=output_location,
            cols=cols,
            output_only_diffs=output_only_diffs,
        )

        diffino.build_diff()

        if not to_console and not output_only_diffs:
            assert os.path.isfile(output_left)
            assert os.path.isfile(output_right)
        return output_location, output_left, output_right

    def test_dataset_read_from_local_file(self):
        location = fname = os.path.join(os.path.dirname(__file__), "sample_left.csv")
        dataset = DataSet(location, None, False)
        df = dataset.read()
        assert isinstance(df, pd.DataFrame)
        assert df.empty is not True

    def test_diffino_diff_is_working(self, tmpdir):
        outputs = self._create_diff(str(tmpdir))

        expected_data_not_in_left = u"""address,state,zip,name,id
eleven st,CA,66611,name eleven,11"""

        expected_data_not_in_right = u"""address,state,zip,name,id
ten st,CA,66610,name ten,10"""

        expected_df_not_in_left = pd.read_csv(io.StringIO(expected_data_not_in_left))
        expected_df_not_in_right = pd.read_csv(io.StringIO(expected_data_not_in_right))

        result_not_in_left = pd.read_csv(outputs[1])
        result_not_in_right = pd.read_csv(outputs[2])

        assert_frames_equal(expected_df_not_in_left, result_not_in_left)
        assert_frames_equal(expected_df_not_in_right, result_not_in_right)

    def test_diffino_no_diff(self, tmpdir):
        outputs = self._create_diff(str(tmpdir), right_csv="sample_left.csv")

        expected_data = u"address,state,zip,name,id"

        expected_df = pd.read_csv(io.StringIO(expected_data))
        resulting_left_csv = pd.read_csv(outputs[1])
        resulting_right_csv = pd.read_csv(outputs[2])

        assert_frames_equal(expected_df, resulting_left_csv)
        assert_frames_equal(expected_df, resulting_right_csv)

    def test_diffino_build_output_to_console(self, tmpdir, capsys):
        self._create_diff(str(tmpdir), to_console=True)
        captured = capsys.readouterr()
        assert "Differences found on left file" in captured.out
        assert "Differences found on right file" in captured.out

    def test_diffino_diff_with_selected_columns(self, tmpdir):
        outputs = self._create_diff(str(tmpdir), cols=["address", "id"])

        expected_data_right = u"""address,id
ten st,10"""
        expected_data_left = u"""address,id
eleven st,11"""

        expected_df_left = pd.read_csv(io.StringIO(expected_data_left))
        expected_df_right = pd.read_csv(io.StringIO(expected_data_right))
        resulting_left_csv = pd.read_csv(outputs[1])
        resulting_right_csv = pd.read_csv(outputs[2])

        assert_frames_equal(expected_df_left, resulting_left_csv)
        assert_frames_equal(expected_df_right, resulting_right_csv)

    def test_diffino_output_only_diffs_console(self, tmpdir, capsys):
        self._create_diff(
            str(tmpdir),
            to_console=True,
            right_csv="sample_left.csv",
            output_only_diffs=True,
        )
        captured = capsys.readouterr()
        assert "Differences found on left file" not in captured.out
        assert "Differences found on right file" not in captured.out

    def test_diffino_output_only_diffs_csv(self, tmpdir):
        outputs = self._create_diff(
            str(tmpdir), right_csv="sample_left.csv", output_only_diffs=True
        )
        assert not os.path.isfile(outputs[0])
        assert not os.path.isfile(outputs[1])
