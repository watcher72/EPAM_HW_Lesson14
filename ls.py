"""A simple analog of command 'ls' on Linux.

It has some options:
-l  - show more information of each file or directory:
      number of links on file, user ID, file size, modification time, name
-a  - includes all hidden files or directories, which start with '.'
-S  - sort the list on the file size
--block-size  - output the size as the number of blocks of given size
-1  - output information in one column
--log  - define the file for output logging information
--format  - define, how will be output the information:
            'long' - output full info
            'single-column' - output in single column
            'commas' - the inline list of files/directories,
                       comma divided
            'horizontal', 'across'- sort the elements in columns in horizontal
            'vertical' - sort the elements in columns in vertical
If not files or directories given, show information about current directory.
"""
import argparse
import datetime as dt
import logging
import os
import shutil
import stat
# from pprint import pprint as pp

from math import ceil


NAME = 'simple_ls'
VERSION = '0.0.1'
DESCRIPTION = '''This is a simple analog of command 'ls' on Linux.'''
EPILOG = '(c) Elena Kiseleva'

CURRENT_DIR = os.getcwd()


log = logging.getLogger('debug_log')
log.setLevel(logging.INFO)

log_formatter = logging.Formatter('%(message)s')


def parse_arguments():
    """Parse the arguments from command line."""
    parser = argparse.ArgumentParser(
        prog=NAME, description=DESCRIPTION, epilog=EPILOG
    )
    parser.add_argument('file', type=str, nargs='*', default='.',
                        help='Files and/or directories')
    parser.add_argument('-l', action='store_true',
                        help='use a long listing format')
    parser.add_argument('-a', '-all', action='store_false',
                        help='do not ignore entries starting with "."')
    parser.add_argument('-S', action='store_true',
                        help='sort by file size, largest first')
    parser.add_argument('-laS')
    parser.add_argument('--block-size', type=int, nargs='?', default=None,
                        help=('show the size as a number of blocks '
                              'of given size'))
    parser.add_argument('-1', dest='one', action='store_true',
                        help='output information in one column')
    parser.add_argument('-log', type=str, nargs='?', default=None,
                        help='define a file for logging')
    parser.add_argument('--format',
                        choices=['long', 'single-column', 'commas',
                                 'horizontal', 'vertical', 'across'],
                        default='vertical',
                        help='define the format of output information')
    # parser.add_argument('--color', choices=['always', 'auto', 'never'], default='never',
    #                     help='sort by file size, largest first')
    parser.add_argument('-v', '--version', action='version',
                        help='Version', version='%(prog)s {}'.format(VERSION))

    args = parser.parse_args()
    return args


def columns_horizontal(files, columns, col_width):
    temp_info = []
    full_rows = len(files) // columns
    full_columns = len(files) % columns
    for i in range(full_rows):
        row = ' '.join(f'{files[i * columns + j]:{col_width}}'
                       for j in range(columns))
        temp_info.append(row)
    temp_info.append(' '.join(f'{files[full_rows * columns + j]:{col_width}}'
                              for j in range(full_columns)))
    temp_info.append('\n')
    return temp_info


def columns_vertical(files, columns, col_width):
    temp_info = []
    total_rows = ceil(len(files) / columns)
    columns = ceil(len(files) / total_rows)
    full_rows = (total_rows if len(files) % total_rows == 0
                 else len(files) % total_rows)
    for i in range(full_rows):
        temp_info.append(' '.join(f'{files[i + j * total_rows]:{col_width}}'
                                  for j in range(columns)))
    for i in range(full_rows, total_rows):
        temp_info.append(' '.join(f'{files[i + j * total_rows]:{col_width}}'
                                  for j in range(columns - 1)))
    temp_info.append('\n')
    return temp_info


def handle_short_info(files, directories, args):
    result_info = []
    # Define the width of columns
    max_length = 0
    if directories:
        max_length = max(max(len(item) for item in directories[d])
                         for d in directories)
    if files:
        max_length = max(max_length, max(len(item) for item in files))
    terminal_width = shutil.get_terminal_size().columns
    if args.format == 'single-column' or args.one:
        columns = 1
    else:
        columns = terminal_width // (max_length + 1) or 1

    if not files and len(directories) == 1:
        d = list(directories.keys())[0]
        if args.format == 'commas':
            result_info.append(', '.join([item for item in directories[d]]))
        elif args.format == 'vertical' or args.format == 'across':
            result_info.extend(
                columns_vertical(directories[d], columns, max_length + 1)
            )
        else:
            result_info.extend(
                columns_horizontal(directories[d], columns, max_length + 1)
            )
        log.debug(result_info)
        return result_info

    if files:
        if args.format == 'commas':
            result_info.append(', '.join([item for item in files]))
        elif args.format == 'vertical' or args.format == 'across':
            result_info.extend(
                columns_vertical(files, columns, max_length + 1)
            )
        else:
            result_info.extend(
                columns_horizontal(files, columns, max_length + 1)
            )
    for d in directories:
        result_info.append(f'{d}:')
        if args.format == 'commas':
            result_info.append(', '.join([item for item in directories[d]]))
        elif args.format == 'vertical' or args.format == 'across':
            result_info.extend(
                columns_vertical(directories[d], columns, max_length + 1)
            )
        else:
            result_info.extend(
                columns_horizontal(directories[d], columns, max_length + 1)
            )
    log.debug(result_info)
    return result_info


def full_info(files, args, dir_='.'):
    temp_info = []
    for item in files:
        f_info = {}
        f_st = os.stat(os.path.join(CURRENT_DIR, dir_, item))
        f_info['mpde'] = f'{stat.filemode(f_st.st_mode):10}'
        f_info['nlink'] = f'{f_st.st_nlink:>3}'
        f_info['uid'] = f'{f_st.st_uid:>3}'
        size = f_st.st_size
        if args.block_size:
            size = ceil(size / args.block_size)
        f_info['size'] = f'{size:>8}'
        date = dt.datetime.fromtimestamp(f_st.st_mtime)
        if (dt.datetime.now() - date).days / 30 > 6:
            date_format = '%b %d  %Y'
        else:
            date_format = '%b %d %I:%M'
        f_info['time'] = f'{date.strftime(date_format)} '
        f_info['name'] = f'{item:<}'
        temp_info.append(
            ' '.join([f_info['mpde'], f_info['nlink'], f_info['uid'],
                      f_info['size'], f_info['time'], f_info['name']])
        )
    temp_info.append('\n')
    return temp_info


def handle_full_info(files, directories, args):
    result_info = []
    if not files and len(directories) == 1:
        d = list(directories.keys())[0]
        result_info.extend(full_info(directories[d], args, d))
        log.debug(result_info)
        return result_info

    if files:
        result_info.extend(full_info(files, args))
    for d in directories:
        result_info.append(f'{d}:')
        result_info.extend(full_info(directories[d], args, d))
    log.debug(result_info)
    return result_info


def main():
    # Parse the arguments
    args = parse_arguments()

    # Create debug logger
    if args.log:
        file_handler = logging.FileHandler(args.log, mode='w')
        file_handler.setFormatter(log_formatter)
        log.addHandler(file_handler)
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        log.addHandler(stream_handler)

    log.debug(args)

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
        for d in directories:
            directories[d] = [item for item in directories[d]
                              if not item.startswith('.')]

    # If -S   - sort by size
    if args.S:
        files = sorted(
            files,
            key=lambda x: -os.path.getsize(os.path.join(CURRENT_DIR, x))
        )
        for d in directories:
            directories[d] = sorted(
                directories[d],
                key=lambda x: -os.path.getsize(os.path.join(CURRENT_DIR, d, x))
            )
    log.debug(files)
    log.debug(directories)

    # If -l  - show long info, else  - show short info
    if args.l or args.format == 'long':
        result = handle_full_info(files, directories, args)
    else:
        result = handle_short_info(files, directories, args)

    if args.log:
        for item in result:
            log.info(item)

    for item in result:
        print(item)

    return


if __name__ == '__main__':
    main()
