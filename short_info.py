import logging
import shutil
from math import ceil


logger = logging.getLogger('debug_log.short_info')


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
        logger.debug(result_info)
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
    logger.debug(result_info)
    return result_info
