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
import shutil
# import stat
# from datetime import datetime as dt

# from pprint import pprint as pp


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
    parser.add_argument('-S', action='store_true',  # default=True,
                        help='sort by file size, largest first')

    # TODO: look at subparser
    parser.add_argument('--format',
                        choices=['long', 'single-column',
                                 'horizontal', 'vertical',
                                 'across', 'verbose'],
                        default='horizontal',
                        help='define the format of output information')
    # parser.add_argument('--format', '-1', type=str, default='single-column',
    #                     help='output information in one colimn')
    parser.add_argument('--color', choices=['always', 'auto', 'never'], default='never',
                        help='sort by file size, largest first')

    args = parser.parse_args()
    return args


def print_in_columns_horizontal(files, columns, col_width):
    full_rows = len(files) // columns
    full_columns = len(files) % columns
    for i in range(full_rows):
        row = ' '.join(f'{files[i * columns + j]:{col_width}}'
                       for j in range(columns))
        print(row)
    print(' '.join(f'{files[full_rows * columns + j]:{col_width}}'
                      for j in range(full_columns)))
    print()


# TODO
def print_in_columns_vertical(files, columns, col_width):
    print(len(files), columns)
    total_rows = (len(files) // columns + 1
                  if len(files) % columns
                  else len(files) // columns)
    full_rows = -(len(files) - total_rows * columns)

    print(full_rows, total_rows)
    for i in range(full_rows):
        row = ' '.join(f'{files[i + j * total_rows]:{col_width}}' for j in range(columns))
        print(row)
    for i in range(full_rows, total_rows):
        row = ' '.join(f'{files[i + j * total_rows]:{col_width}}' for j in range(columns - 1))
        print(row)


def short_info(files, directories, args):
    max_length = 0
    if directories:
        max_length = max(max(len(item) for item in directories[d])
                         for d in directories)
    if files:
        max_length = max(max_length, max(len(item) for item in files))
    terminal_width = shutil.get_terminal_size().columns
    if args.format == 'single-column':
        columns = 1
    else:
        columns = terminal_width // (max_length + 1) or 1

    if files:
        if args.format == 'vertical':
            print_in_columns_vertical(files, columns, max_length + 1)
        else:
            print_in_columns_horizontal(files, columns, max_length + 1)
        print()
    if not files and len(directories) == 1:
        if args.format == 'vertical':
            print_in_columns_vertical(files, columns, max_length + 1)
        else:
            print_in_columns_horizontal(directories[0], columns, max_length + 1)
        print()
        return
    for item in directories:
        print(f'{item}:')
        if args.format == 'vertical':
            print_in_columns_vertical(files, columns, max_length + 1)
        else:
            print_in_columns_horizontal(directories[item], columns, max_length + 1)
        print()


def full_info(files, directories, args):
    print('Must be printed in vertical order columns!!')
    pass


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
        files = sorted(
            files,
            key=lambda x: os.path.getsize(os.path.join(CURRENT_DIR, x))
        )
        for d in directories:
            directories[d] = sorted(
                directories[d],
                key=lambda x: os.path.getsize(os.path.join(CURRENT_DIR, d, x))
            )

    # If -l  - show long info, else  - show short info
    if args.l:
        full_info(files, directories, args)
    else:
        short_info(files, directories, args)

    # print(files)
    # print(directories)
    return


if __name__ == '__main__':
    main()
