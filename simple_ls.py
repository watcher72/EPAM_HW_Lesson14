import argparse
# import os
# import stat
# from datetime import datetime as dt


NAME = 'simple_ls'
VERSION = '0.0.1'
DESCRIPTION = '''This is a simple analog of command 'ls' on Linux.'''
EPILOG = '(c) Elena Kiseleva'


def parse_arguments():
    """Parse the arguments from command line."""
    parser = argparse.ArgumentParser(
        prog=NAME, description=DESCRIPTION, epilog=EPILOG,  # add_help=False
    )
    parser.add_argument('file', type=str, nargs='+', default='',
                        help='Files and/or directories')
    parser.add_argument('-a', '-all', action='store_false',  # default=False,
                        help='do not ignore entries starting with .')
    parser.add_argument('-l', action='store_true',  # default=True,
                        help='use a long listing format')
    # TODO: look at subparser
    parser.add_argument('--format',
                        choices=['long', 'single-column', 'horizontal',
                                 'vertical', 'accross', 'verbose'],
                        default='vertical',
                        help='define the format of output information')
    parser.add_argument('-S', action='store_true',  # default=True,
                        help='sort by file size, largest first')
    # parser.add_argument('--color', choices=['always', 'auto', 'never'], default='never',
    #                     help='sort by file size, largest first')

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    print(args)
    # Parse the arguments

    # Analise given files and directories, collect them

    # If not -a  - remove hidden

    # If -S   - sort in size

    # If -l  - show long info

    # else  - show short info
    pass


if __name__ == '__main__':
    main()
