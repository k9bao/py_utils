import os
import unittest
import logging
import uuid

from py_utils.src.download.download import download_to_filesystem, single_thread_download_to_filesystem


class DownloadTest(unittest.TestCase):
    test_file = "http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"

    def test_download(self):
        dst_path = f"{uuid.uuid1()}.mp4"
        download_to_filesystem(self.test_file, dst_path, 2)
        self.assertTrue(os.path.getsize(dst_path) > 0)
        logging.debug(f"size = {os.path.getsize(dst_path)}")
        if os.path.exists(dst_path):
            os.remove(dst_path)

    def test_download_single(self):
        dst_path = f"{uuid.uuid1()}.mp4"
        single_thread_download_to_filesystem(self.test_file, dst_path)
        self.assertTrue(os.path.getsize(dst_path) > 0)
        logging.debug(f"size = {os.path.getsize(dst_path)}")
        if os.path.exists(dst_path):
            os.remove(dst_path)


# python3 -m pytest -o log_cli=true -o log_cli_level=DEBUG py_utils/src/download/download_test.py
if __name__ == "__main__":
    unittest.main()
