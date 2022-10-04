# -*- coding: utf-8 -*-

import re
import itertools
import hashlib
import requests
import time
import socket
import logging

from functools import wraps
from retrying import retry
from concurrent import futures


logger = logging.getLogger("other")


__author__ = "coco <coco_huibao@163.com>"


def is_cdn_in_url(url):
    if not url:
        return False

    cond1 = "cdn.zenvideo.cn" in url
    cond2 = "cdn.huijianji.cn" in url  # for compatable
    return cond1 or cond2


def floor_frame_duration(duration, fps=DEFAULT_FPS):
    if duration is None or duration < 0:
        return 0
    # at this time, 2.0 we will support any frame rate
    # not need to align to 40ms.
    # frame_duration = int(1000 / fps)
    # return int(duration / frame_duration) * frame_duration
    return round(duration)


def index_from_time(duration, fps=DEFAULT_FPS):
    if duration is None or duration < 0:
        return 0
    return int(duration * fps / 1000)


def round_frame(duration_in_ms, ndigits=None, fps=None):
    """
    对齐帧到帧率上
    比如30fps的时候:
        a) 1034ms ===> 1033ms
        b) 1033.34ms  ===> 1033.333ms
        c) 1066ms ===> 1067ms
        d) 1066.67ms ===> 1066.667ms
    同时调整可能的累积误差, 比如：
        开始时间为1067, duraton为1067
        1067ms + 1067ms前端反映的是第64帧(也就是2133ms），但是相加为64帧+1ms(2134ms)
    """
    if duration_in_ms is None:
        return 0

    if fps and isinstance(fps, int):
        num, den = fps, 1
    elif fps and fps.num > 0 and fps.den > 0:
        num, den = fps.num, fps.den
    else:
        # 30 fps for 2.0 front-end
        num, den = 30, 1
    return round(round(duration_in_ms * num / den / 1000) * den * 1000 / num, ndigits)


def atof(s):
    return float("".join(re.findall(r"-?[0-9]+(?:\.[0-9]+)?", s)))


def collapse(iterable):
    lst = sorted(set(iterable))
    cl = []
    for k, g in itertools.groupby(enumerate(lst), lambda x: x[1] - x[0]):
        g = list(g)
        cl.append((g[0][1], g[-1][1] + 1))
    return cl


def hor_to_ver(x):
    hor_width = 1920
    ver_width = 607.5  # = 1080 * 1080 / 1920
    x = x * hor_width
    x = (x - (hor_width - ver_width) / 2) / ver_width
    return x


def wait_for_results(future_results, timeout=None):
    done, not_done = futures.wait(future_results, timeout=timeout, return_when=futures.FIRST_EXCEPTION)
    return [future_result.result() for future_result in done]


def get_fmd5(fpath):
    hash_md5 = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_fsha1(fpath):
    hash_sha1 = hashlib.sha1()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()


def md5(s):
    return hashlib.md5(s.encode(encoding="UTF-8", errors="ignore")).hexdigest()


def sha1(s):
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def host_ip2():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def host_ip():
    try:
        hostname = socket.gethostname()
        hostname_s = hostname.split("-")
        if len(hostname_s) >= 5:
            hostname = "-".join(hostname_s[:-1])
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception as e:
        logger.debug(f"host_ip:{e}, try to host_ip2")
        return host_ip2()


@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000)
def post_method(*args, **kwargs):
    response = requests.post(*args, **kwargs)
    if response.status_code != 200:
        msg = f"HTTP Post fail. code: {response.status_code}, text: {response.text}, args: {args}, kwargs: {kwargs}"
        raise Exception(msg)
    return response


def cost_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        logger.info(f"time of {func.__name__}: {round(time.time()-t1, 3)}")
        return result

    return wrapper


def parse_color(color):
    if isinstance(color, str) and color.startswith("#"):
        if len(color) == 7:
            color = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
            color = (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, 1.0)
        elif len(color) == 9:
            color = tuple(int(color[i : i + 2], 16) / 255.0 for i in (1, 3, 5, 7))
        elif len(color) == 4:
            color = tuple(int(int(color[i : i + 1], 16) / 15.0) for i in (1, 2, 3))
        else:
            color = (0, 0, 0, 0)
    else:
        color = (0, 0, 0, 0)
    return color
