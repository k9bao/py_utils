import os
import unittest
import logging

from py_utils.src.fs.file import get_file_size


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


if __name__ == "__main__":
    unittest.main()
