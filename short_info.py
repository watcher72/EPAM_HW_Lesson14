import shutil


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


# TODO: calculate rows and columns
def print_in_columns_vertical(files, columns, col_width):
    print('Must be printed in vertical ordered columns')
    # print(len(files), columns)
    # total_rows = (len(files) // columns + 1
    #               if len(files) % columns
    #               else len(files) // columns)
    # full_rows = -(len(files) - total_rows * columns)
    #
    # print(full_rows, total_rows)
    # for i in range(full_rows):
    #     row = ' '.join(f'{files[i + j * total_rows]:{col_width}}' for j in range(columns))
    #     print(row)
    # for i in range(full_rows, total_rows):
    #     row = ' '.join(f'{files[i + j * total_rows]:{col_width}}' for j in range(columns - 1))
    #     print(row)


def handle_short_info(files, directories, args):
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
        if args.format == 'commas':
            print(', '.join([item for item in files]))
        elif args.format == 'vertical' or args.format == 'across':
            print_in_columns_vertical(files, columns, max_length + 1)
        else:
            print_in_columns_horizontal(files, columns, max_length + 1)
        print()
    if not files and len(directories) == 1:
        d = list(directories.keys())[0]
        if args.format == 'commas':
            print(', '.join([item for item in directories[d]]))
        elif args.format == 'vertical' or args.format == 'across':
            print_in_columns_vertical(directories[d], columns, max_length + 1)
        else:
            print_in_columns_horizontal(directories[d],
                                        columns, max_length + 1)
        print()
        return
    for d in directories:
        print(f'{d}:')
        if args.format == 'commas':
            print(', '.join([item for item in directories[d]]))
        elif args.format == 'vertical' or args.format == 'across':
            print_in_columns_vertical(directories[d], columns, max_length + 1)
        else:
            print_in_columns_horizontal(directories[d], columns, max_length + 1)
        print()
    return
