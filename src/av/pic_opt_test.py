import unittest
import logging

from src.av.pic_opt import get_pic_time


class FileTest(unittest.TestCase):
    def test_get_pic_time(self):
        logging.debug(get_pic_time("/Users/tianwenhui/Documents/pic_classify/2010/02/20100215_215151_IMG_7671.jpeg"))


# python3 -m pytest -o log_cli=true -o log_cli_level=DEBUG src/av/pic_opt_test.py
if __name__ == "__main__":
    unittest.main()
