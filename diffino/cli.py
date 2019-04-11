from models import Diffino
import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('left_dataset', help='Path or S3 loaction of the left data set (CSV, JSON, etc)')
    parser.add_argument('right_dataset', help='Path or S3 loaction of the right data set (CSV, JSON, etc)')
    parser.add_argument('--mode', default='pandas', choices=['pandas', 'md5'], help='Pandas or md5')
    parser.add_argument('--convert-numeric', action='store_true', default=True, help='Whether to convert numeric columns')
    parser.add_argument('--cols', nargs='+', default=[], help='Columns to be used for comparing')
    parser.add_argument('--index_col', default=False, help='Column to be used as index for both datasets')
    parser.add_argument('--output', help='Output file')

    args = parser.parse_args()

    diffino = Diffino(left=args.left_dataset, right=args.right_dataset,
                      index_col=args.index_col, output=args.output, cols=args.cols)

    diffino.build_diff()

    """
    A = pd.read_csv('DFs/lines_current.csv', index_col=2)

    B = pd.read_csv('DFs/lines_new.csv', index_col=2)

    C = pd.merge(left=A, right=B, how='outer', left_index=True, right_index=True, suffixes=['_left', '_right'])

    not_in_a = C.drop(A.index)
    not_in_b = C.drop(B.index)

    not_in_a.to_csv('not_in_a.csv')
    not_in_b.to_csv('not_in_b.csv')
    """


if __name__ == '__main__':
    main()
