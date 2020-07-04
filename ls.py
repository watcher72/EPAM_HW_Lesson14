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
import logging
import os
# from pprint import pprint as pp

from short_info import handle_short_info
from long_info import handle_full_info
from constants import NAME, DESCRIPTION, EPILOG, VERSION, CURRENT_DIR


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
    # TODO: look at subparser or group
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


def create_debug_logger(file=None):
    d_log = logging.getLogger('debug_log')
    d_log.setLevel(logging.INFO)

    d_log_formatter = logging.Formatter('%(message)s')

    if file:
        file_handler = logging.FileHandler(file, mode='w')
        file_handler.setFormatter(d_log_formatter)
        d_log.addHandler(file_handler)
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(d_log_formatter)
        d_log.addHandler(stream_handler)
    return d_log


def main():
    # Parse the arguments
    args = parse_arguments()

    # Create debug logger
    log = create_debug_logger(args.log) if args.log else create_debug_logger()

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