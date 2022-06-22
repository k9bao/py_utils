import unittest
import logging

from py_utils.src.fs.dir import (
    get_ext,
    filter_str,
    list_all_files,
    list_all_dirs,
    list_all_ext,
)


class DirTest(unittest.TestCase):
    def test_get_ext(self):
        ext = get_ext("/user/test.txt")
        self.assertEqual(ext, ".txt")
        logging.debug(f"{ext}")

    def test_filter_str(self):
        ret = filter_str("111", None, ["111", "222"])
        self.assertEqual(ret, False)

        ret = filter_str("111", None, ["333", "222"])
        self.assertEqual(ret, True)

        ret = filter_str("111", ["444"], ["333", "222"])
        self.assertEqual(ret, False)

        ret = filter_str("111", ["111", "444"], ["333", "222"])
        self.assertEqual(ret, True)

    def test_list_all_files(self):
        ret = list_all_files(".", ext=[".py"])
        self.assertTrue(len(ret) > 0)

        ret = list_all_files(".", ext=[".java"])
        self.assertTrue(len(ret) == 0)

    def test_list_all_dirs(self):
        ret = list_all_dirs(".")
        self.assertTrue(len(ret) > 0)

    def test_list_all_ext(self):
        ret = list_all_ext(".")
        self.assertTrue(len(ret) > 0)


if __name__ == "__main__":
    unittest.main()
