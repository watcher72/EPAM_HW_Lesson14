"""A simple analog of command 'ls' on Linux.

It has some options:
-l  - show more information of each file or directory:
      number of links on file, user ID, file size, modification time, name
-a  - includes all hidden files or directories, which start whith '.'
-S  - sort the list on the file size
If not files or directories given, show information about current directory.
"""
import argparse
import os
# import stat
# from datetime import datetime as dt

from pprint import pprint as pp


NAME = 'simple_ls'
VERSION = '0.0.1'
DESCRIPTION = '''This is a simple analog of command 'ls' on Linux.'''
EPILOG = '(c) Elena Kiseleva'
CURRENT_DIR = os.getcwd()


def parse_arguments():
    """Parse the arguments from command line."""
    parser = argparse.ArgumentParser(
        prog=NAME, description=DESCRIPTION, epilog=EPILOG,  # add_help=False
    )
    parser.add_argument('file', type=str, nargs='*', default='.',
                        help='Files and/or directories')
    parser.add_argument('-a', '-all', action='store_false',  # default=False,
                        help='do not ignore entries starting with .')
    parser.add_argument('-l', action='store_true',  # default=True,
                        help='use a long listing format')
    parser.add_argument('-S', action='store_true',  default=True,
                        help='sort by file size, largest first')

    # TODO: look at subparser
    # parser.add_argument('--format',
    #                     choices=['long', 'single-column', 'horizontal',
    #                              'vertical', 'across', 'verbose'],
    #                     default='vertical',
    #                     help='define the format of output information')
    # parser.add_argument('--color', choices=['always', 'auto', 'never'], default='never',
    #                     help='sort by file size, largest first')

    args = parser.parse_args()
    return args


def get_file_size(x):
    """Return a size of given file in some directory"""
    return os.path.getsize(os.path.join(CURRENT_DIR, x))


def main():
    # Parse the arguments
    args = parse_arguments()
    print(args)

    # Analise given files and directories, collect them
    files = []
    directories = {}
    for item in args.file:
        full_path = os.path.join(CURRENT_DIR, item)
        if os.path.isfile(full_path):
            files.append(item)
        elif os.path.isdir(full_path):
            directories[item] = os.listdir(full_path)
        else:
            print(f'Unknown file/directory {item}')
            return

    # If not -a  - remove hidden
    # Логичнее было бы проверять 'not args.a' сделать флаг True по умолчанию,
    # но хотелось попробовать проверить отсутствие флага.
    if args.a:
        files = [file for file in files if not file.startswith('.')]
        for item in directories:
            directories[item] = [d for d in directories[item]
                                 if not d.startswith('.')]

    # If -S   - sort by size
    if args.S:
        files = sorted(files, key=get_file_size)
        for d in directories:
            directories[d] = sorted(
                directories[d],
                key=lambda x: get_file_size(os.path.join(d, x))
            )

    # If -l  - show long info

    # else  - show short info
    print(files)
    pp(directories)
    pass


if __name__ == '__main__':
    main()
