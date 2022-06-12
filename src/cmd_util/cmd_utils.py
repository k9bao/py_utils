#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import subprocess


# 运行命令，输入：字符串数组，输出：字符串结果+错误(None为成功)
def run_sys_command(cmd_arr, extra_env=None):
    my_env = os.environ.copy()
    if extra_env is not None:
        my_env.update(extra_env)

    cmd_arr = list(filter(None, cmd_arr))
    cmd_str = " ".join(cmd_arr)
    logging.debug(cmd_str)
    logging.debug(f"Running command: {cmd_str}")

    proc = subprocess.Popen(cmd_arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)

    ret = proc.communicate()
    ret = [r.decode("utf-8", errors="ignore") if r else r for r in ret]

    if proc.returncode != 0:
        msg = f"Running command {cmd_str} with non-zero, return code:{proc.returncode},\
                              STDOUT: {ret[0]}, STDERR: {ret[1]}"
        return "", msg
    return ret, None
