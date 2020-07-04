import datetime as dt
import os
import stat
from math import ceil

from constants import CURRENT_DIR


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
    if files:
        result_info.extend(full_info(files, args))
    if not files and len(directories) == 1:
        d = list(directories.keys())[0]
        result_info.extend(full_info(directories[d], args, d))
        return result_info
    for d in directories:
        result_info.append(f'{d}:')
        result_info.extend(full_info(directories[d], args, d))
    return result_info
