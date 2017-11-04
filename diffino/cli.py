import argparse


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('left_dataset', help='Path or S3 loaction of the left data set (CSV, JSON, etc)')
    parser.add_argument('right_dataset', help='Path or S3 loaction of the right data set (CSV, JSON, etc)')
    parser.add_argument('--mode', default='pandas', choices=['pandas', 'md5'], help='Pandas or md5')
    parser.add_argument('--convert-numeric', action='store_true', default=True, help='Whether to convert numeric columns')
    parser.add_argument('--cols', nargs='+', help='Columns to be used for comparing')
    parser.add_argument('--output', help='Output file')

    args = parser.parse_args()


if __name__ == '__main__':
    main()
