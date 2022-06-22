import os
import unittest
import logging
import tempfile

from py_utils.src.fs.file import (
    get_file_size,
    read_all,
    write_file,
)


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

    def test_write_file(self):
        tmpfile = tempfile.mktemp()  # 返回临时文件，但是不创建
        text = "hello world"
        write_file(tmpfile, text)
        text2 = read_all(tmpfile)
        logging.debug(f"{text}, {text2}")
        self.assertEqual(text, text2)
        os.remove(tmpfile)


# python3 -m pytest -o log_cli=true -o log_cli_level=DEBUG py_utils/src/fs/file_test.py
if __name__ == "__main__":
    unittest.main()
