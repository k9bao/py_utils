import unittest
import os.path
import logging

from src.md5.md5 import get_fmd5, get_fsha1

test_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "testdata")


class FileTest(unittest.TestCase):
    def test_get_md5(self):
        file_name = os.path.join(test_path, "test.txt")
        ret = get_fmd5(file_name)
        logging.debug(f"mp5: {ret}")
        self.assertTrue(ret == "bb53d6b3802a9c79f4ebda3c81580b75")

    def test_get_sha1(self):
        file_name = os.path.join(test_path, "test.txt")
        ret = get_fsha1(file_name)
        logging.debug(f"sha1: {ret}")
        self.assertTrue(ret == "ac62252f3c6ac87f77e9652a5bf841e352948b01")


if __name__ == "__main__":
    unittest.main()
