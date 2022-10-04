# -*- coding: utf-8 -*-

import os
import shutil
import threading
import requests
import time
import logging
import urllib3

from retrying import retry
from requests.exceptions import ChunkedEncodingError


DEFAULT_FPS = 25
logger = logging.getLogger("download")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


PROXIES = {"http": "socks5h://127.0.0.1:1086", "https": "socks5h://127.0.0.1:1086"}

__author__ = "coco <coco_huibao@163.com>"


MAX_REDIRECT_TIMES = 5


class ResultThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        super(ResultThread, self).__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)
        self.result = None
        self.exc = None

    def run(self):
        try:
            for i in range(3):
                try:
                    if self._target:
                        self.result = self._target(*self._args, **self._kwargs)
                    self.exc = None
                    break
                except ChunkedEncodingError as e:
                    logger.warn(f"failed to run {self._kwargs}: {e} in {i} times.")
                    self.exc = e
                    time.sleep((i + 1) * 5)
        except Exception as e:
            self.exc = e
        finally:
            if self.exc:
                logger.error(f"exception occurs from ResultThread {self._kwargs}: {self.exc}")
            del self._target, self._args, self._kwargs


@retry(stop_max_attempt_number=10, wait_fixed=1000)
def get_download_content_size(
    file_url,
    timeout=15,
    params=None,
    stream=False,
):
    request_headers = {
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml," "application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    if params is None:
        params = {}

    file_url = normalize_url(file_url)

    # sometimes we saw image URL with spaces, this is just to be more reliant.
    file_url = file_url.replace(" ", "%20")

    kwargs = {"headers": request_headers, "timeout": timeout, "verify": False, "stream": stream}
    kwargs["params"] = params

    response = requests.head(file_url, **kwargs)
    redirect_times = 0
    while response.status_code in (301, 302, 303, 307, 308) and redirect_times < MAX_REDIRECT_TIMES:
        file_url = response.headers["Location"]
        response = requests.head(file_url, **kwargs)
        redirect_times += 1
    # NOT SUPPORT HEAD methods
    if response.status_code >= 400:
        return 0, file_url
    return int(response.headers.get("Content-Length") or 0), file_url


@retry(stop_max_attempt_number=10, wait_fixed=1000)
def download_content_from_url(
    file_url,
    text=False,
    timeout=15,
    params=None,
    stream=False,
    start=0,
    end=0,
):
    if params is None:
        params = {}

    file_url = normalize_url(file_url)

    request_headers = {
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml," "application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    # sometimes we saw image URL with spaces, this is just to be more reliant.
    file_url = file_url.replace(" ", "%20")
    if end > 0:
        request_headers["Range"] = "bytes=%d-%d" % (start, end)
    kwargs = {"headers": request_headers, "timeout": timeout, "verify": False, "stream": stream}
    kwargs["params"] = params
    resp = requests.get(file_url, **kwargs)
    logger.debug(f"download_content_from_url: {start} {end} {kwargs}")
    # 腾讯视频的ts文件，即使不设置Range,也返回206,原来这里只有200.理论 if 和 else 可以合并，这里是为了标准其特殊性没有合并
    redirect_times = 0
    while resp.status_code in (301, 302, 303, 307, 308) and redirect_times < MAX_REDIRECT_TIMES:
        file_url = resp.headers["Location"]
        resp = requests.get(file_url, **kwargs)
        redirect_times += 1
    if end <= 0 and resp.status_code not in (200, 206):
        msg = f"failed to download1 {file_url} => " f"{resp.status_code} {resp.text}"
        raise Exception(msg)
    elif end > 0 and resp.status_code not in (200, 206):
        msg = f"failed to download2 {file_url} => " f"{resp.status_code} {resp.text}"
        raise Exception(msg)
    if text:
        result = resp.text
    elif stream:
        result = resp
    else:
        result = resp.content
    content_size = int(resp.headers.get("Content-Length") or 0)
    setattr(result, "context_size", content_size)
    return result


def download_handler(start, end, total_size, url, filename):
    with download_content_from_url(url, stream=True, start=start, end=end) as resp:
        if end - start + 1 != resp.context_size:
            end = start + resp.context_size - 1

        # 206 支持分片下载
        # 200 不支持分片下载, 所有就由start为0负责下载完整文件
        if resp.status_code == 200:
            if start > 0:
                logger.debug(f"not support partial content download:{url}")
                return 0, 0
            # 当前下载整个文件
            else:
                end = resp.context_size - 1
        if end <= 0:
            end = resp.context_size - 1
        with open(filename, "rb+" if total_size > 0 else "wb") as fp:
            if start > 0:
                fp.seek(start)
            download_size = 0
            t1 = t0 = time.time()
            last_download_size = 0
            for chunk in resp.iter_content(1024 * 20):
                download_size += len(chunk)
                fp.write(chunk)
                t2 = time.time()
                dur = int(t2 - t1)
                if dur > 10 and dur % 60 == 0:
                    diff = download_size - last_download_size
                    speed = diff * 1.0 / (t2 - t1)
                    logger.debug(
                        f"downloading {start} {end} "
                        f"speed:{round(speed / 1024, 2)}k "
                        f"{round(download_size * 100 / (end - start + 1), 2)}% "
                        f"{dur // 60}:{round(t2 - t1 - (dur // 60 * 60), 3)} "
                    )
                    t1 = t2
                    last_download_size = download_size

            t2 = time.time()
            speed = download_size * 1.0 / (t2 - t0)
            dur = int(t2 - t0)
            if end - start + 1 != download_size:
                logger.error(
                    f"err downloaded {start} {end} {download_size} "
                    f"speed:{round(speed / 1024, 2)}k "
                    f"{dur // 60}:{round(t2 - t0 - (dur // 60 * 60), 3)} {url} {filename}"
                )
            else:
                logger.debug(
                    f"downloaded {start} {end} {download_size} "
                    f"speed:{round(speed / 1024, 2)}k "
                    f"{dur // 60}:{round(t2 - t0 - (dur // 60 * 60), 3)} {url} {filename}"
                )
            return download_size, start


@retry(stop_max_attempt_number=3, wait_fixed=1000)
def download_to_filesystem(file_url, file_path, max_threads=10):
    if not file_url:
        return
    file_url = normalize_url(file_url)
    if file_url[0] == "/":
        shutil.copyfile(file_url, file_path)
        return
    logger.debug(f"download_to_filesystem: {file_url} => {file_path}")
    if max_threads <= 1:
        single_thread_download_to_filesystem(file_url, file_path)
    else:
        multithreads_download_to_filesystem(file_url, file_path, max_threads=max_threads)


def single_thread_download_to_filesystem(file_url, file_path):
    try:
        download_handler(0, 0, 0, file_url, file_path)
    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
    return file_path


def multithreads_download_to_filesystem(file_url, file_path, max_threads=10):
    total_size, redirect_url = get_download_content_size(file_url, stream=True)
    try:
        if total_size < 10 * 1024 * 1024:
            num_thread = 1
        elif total_size < 100 * 1024 * 1024:
            num_thread = 3
        else:
            num_thread = 10
        # workaround: 有些图片的cdn，下载忽大或小，一开始不能限定文件大小
        # 小于10M的文件由请求县城再次确认下载内容大小
        if num_thread > 1:
            with open(file_path, "wb") as fp:
                fp.truncate(total_size)
        num_thread = max(1, min(num_thread, max_threads))
        logger.debug(
            f"redirect_url:{redirect_url} "
            f"file_url:{file_url} "
            f"total_size: {total_size} "
            f"num_thread: {num_thread}"
        )
        part = (total_size + num_thread - 1) // num_thread
        threads = []
        for i in range(num_thread):
            t = ResultThread(
                target=download_handler,
                kwargs=dict(
                    start=part * i,
                    # end == 0, 下载线程还需要再次确认大小
                    end=min(total_size, part * (i + 1)) - 1 if num_thread > 1 else 0,
                    total_size=total_size if num_thread > 1 else 0,
                    url=redirect_url,
                    filename=file_path,
                ),
            )
            t.setDaemon(True)
            t.start()
            threads.append(t)

        max_size = 0
        for t in threads:
            t.join()
            if t.exc:
                raise t.exc
            download_size, start = t.result
            if download_size:
                max_size = max(max_size, download_size + start)
        if max_size < total_size:
            logger.debug(f"HEAD size = {total_size}, GET size = {max_size}")
            with open(file_path, "rb+") as fp:
                fp.truncate(max_size)
    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
    return file_path


def normalize_url(url):
    if not url:
        return url
    if url.startswith("//"):
        url = "http:%s" % url
    elif not url.startswith("/") and not url.startswith("http"):
        url = "http://%s" % url
    return url
