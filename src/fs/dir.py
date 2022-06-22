import os
import logging


# 检测 text 包含关系
def filter_str(text, in_filter, out_filter):
    """
    text 在 out_filter,返回 False
    in_filter 等于None,返回 True
    in_filter 不等于 None,不在里边返回 False,在里边返回 True
    """
    if in_filter is not None:
        assert isinstance(in_filter, list) or isinstance(in_filter, tuple)

    if out_filter is not None:
        assert isinstance(out_filter, list) or isinstance(out_filter, tuple)

    if out_filter is not None and text in out_filter:
        return False
    if in_filter is not None:
        if text in in_filter:
            return True
        else:
            return False
    else:
        return True


# 存放归档文件的所有目录，包含各级子目录(绝对路径)
def get_all_dirs(root_dir):
    if not os.path.isdir(root_dir):
        return []
    _dirs = [root_dir]
    names = os.listdir(root_dir)
    for i in range(0, len(names)):
        name = os.path.join(root_dir, names[i])
        if os.path.isdir(name):
            _dirs.extend(get_all_dirs(name))
    return _dirs


# 获取目录下所有文件(绝对路径)
def get_all_files(root_dir, ext=None, non_ext=None):
    """
    功能：获取目录下的所有文件
    输入：
        rootdir 目录，
        not_ext 排除指定后缀[.json,.txt],优先级高于ext,必须是列表或元祖
        ext     过滤指定后缀，为空不过滤比如[.png,.jpg],只返回.png和.jpg后缀,必须是列表或元祖
    输出：
        文件绝对路径列表
    """
    _files = []
    list = os.listdir(root_dir)
    for i in range(0, len(list)):
        path = os.path.join(root_dir, list[i])
        if os.path.isdir(path):
            _files.extend(get_all_files(path, ext, non_ext))
        if os.path.isfile(path):
            if filter_str(os.path.splitext(path)[-1], ext, non_ext):
                _files.append(path)
    return _files


# 获取目录下所有子目录及文件(绝对路径)
def get_all_dirs_and_files(root_dir):
    """
    功能：获取目录下的所有目录及文件
    输入：
        rootdir 目录，
    输出：
        文件绝对路径列表
    """
    _dirs = [root_dir]
    list = os.listdir(root_dir)
    for i in range(0, len(list)):
        name = os.path.join(root_dir, list[i])
        if os.path.isdir(name):
            _dirs.extend(get_all_dirs_and_files(name))
        elif os.path.isfile(name):
            _dirs.append(name)
    return _dirs


# 获取目录下所有后缀
def get_all_ext(rootdir):
    """
    功能：获取目录下的所有文件夹
    输入：
        rootdir 目录，
    输出：
        所有后缀
    """
    _ext = set()
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isdir(path):
            _ext = _ext.union(get_all_ext(path))
        if os.path.isfile(path):
            _ext.add(os.path.splitext(path)[-1])
    return _ext


# 删除指定名称文件
def del_assign_file(dir, filename):
    abs_filenames = get_all_files(dir)
    for abs_filename in abs_filenames:
        if os.path.basename(abs_filename) == filename:
            os.remove(abs_filename)


# 删除空目录
def del_empty_dir(root_dir):
    abs_dirs = get_all_dirs(root_dir)
    for dir in abs_dirs[::-1]:
        if len(os.listdir(dir)) == 0:
            os.rmdir(dir)


# 对目录下的文件重命名
def rename_dir_files(root_dir):
    abs_dirs = get_all_dirs(root_dir)
    for abs_dir in abs_dirs:
        names = os.listdir(abs_dir)
        index = 1
        for name in names:
            abs_name = os.path.join(abs_dir, name)
            if os.path.isfile(abs_name) and name[0] != ".":
                ext = os.path.splitext(abs_name)[-1]
                os.rename(abs_name, os.path.join(abs_dir, f"{index}{ext}"))
                index += 1
