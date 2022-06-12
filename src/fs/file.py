import os


# 通过文件句柄获取文件大小
def get_file_size(file_handle):
    pos = file_handle.tell()
    file_handle.seek(0, os.SEEK_END)
    file_size = file_handle.tell()
    file_handle.seek(pos, os.SEEK_SET)
    return file_size
