import os
import unittest
import logging

from src.fs.file import get_file_size, get_dirs, get_filenames, get_dirs_filenames


class FileTest(unittest.TestCase):
    def test_file_size(self):
        file_name = __file__
        size1 = os.path.getsize(filename=file_name)
        handler = open(file_name, mode="r", encoding="utf-8")
        if handler:
            size2 = get_file_size(handler)
        handler.close()
        self.assertEqual(size1, size2)
        logging.debug(f"{size1}, {size2}")

    def test_get_dirs(self):
        dirs = get_dirs("./")
        filenames = get_filenames(".")
        dirs1, filenames1 = get_dirs_filenames(".")
        self.assertEqual(dirs, dirs1)
        self.assertEqual(filenames, filenames1)
        logging.debug(f"{dirs}, {dirs1}, {filenames}, {filenames1}")


if __name__ == "__main__":
    unittest.main()
