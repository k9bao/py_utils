import unittest
import logging

from py_utils.src.net.net import host_ip


class FileTest(unittest.TestCase):
    def test_file_size(self):
        ret = host_ip()
        logging.debug(ret)
        self.assertTrue(ret.count(".") == 3)


if __name__ == "__main__":
    unittest.main()
