import logging
import os


# 通过文件句柄获取文件大小
def get_file_size(file_handle):
    pos = file_handle.tell()
    file_handle.seek(0, os.SEEK_END)
    file_size = file_handle.tell()
    file_handle.seek(pos, os.SEEK_SET)
    return file_size


def _get_file_path(root_path, filenames, dirs):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    logging.debug(dir_or_files)
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        logging.debug(dir_file)
        dir_file_path = os.path.join(root_path, dir_file)
        logging.debug(dir_file_path)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            if dirs:
                dirs.append(dir_file_path)
            # 递归获取所有文件和目录的路径
            _get_file_path(dir_file_path, filenames, dirs)
        else:
            if filenames:
                filenames.append(dir_file_path)


def get_dirs(dir):
    dirs = []
    _get_file_path(dir, None, dirs)
    return dirs


def get_filenames(dir):
    filenames = []
    _get_file_path(dir, filenames, None)
    return filenames


def get_dirs_filenames(dir):
    filenames = []
    dirs = []
    _get_file_path(dir, filenames, dirs)
    return dirs, filenames
