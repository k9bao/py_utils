import os
import unittest
import logging
import tempfile
import shutil


from py_utils.src.fs.dir import (
    filter_str,
    get_all_files,
    get_all_dirs_and_files,
    get_all_ext,
    del_assign_file,
    del_empty_dir,
    get_all_dirs,
    rename_dir_files,
)
from py_utils.src.fs.file import write_file


class DirTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # root_dir
        #   subdir1
        #     subdir1_1
        #        file*.go
        #     file*.py
        #   subdir2
        #     file*.py
        #   subdir3
        #   file*.cpp
        cls.dir = tempfile.mkdtemp()
        logging.debug(cls.dir)
        os.makedirs(cls.dir, exist_ok=True)
        tmpfd, name = tempfile.mkstemp(suffix=".cpp", dir=cls.dir)
        logging.debug(name)
        os.close(tmpfd)

        dir = os.path.join(cls.dir, "subdir1")
        os.mkdir(dir)
        logging.debug(dir)
        tmpfd, name = tempfile.mkstemp(suffix=".py", dir=dir)
        logging.debug(name)
        os.close(tmpfd)

        dir = os.path.join(dir, "subdir1_1")
        os.mkdir(dir)
        logging.debug(dir)
        tmpfd, name = tempfile.mkstemp(suffix=".go", dir=dir)
        logging.debug(name)
        os.close(tmpfd)

        dir = os.path.join(cls.dir, "subdir2")
        os.mkdir(dir)
        logging.debug(dir)
        tmpfd, name = tempfile.mkstemp(suffix=".py", dir=dir)
        logging.debug(name)
        os.close(tmpfd)

        dir = os.path.join(cls.dir, "subdir3")
        os.mkdir(dir)
        logging.debug(dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir)

    def test_filter_str(self):
        ret = filter_str("111", None, ["111", "222"])
        self.assertEqual(ret, False)

        ret = filter_str("111", None, ["333", "222"])
        self.assertEqual(ret, True)

        ret = filter_str("111", ["444"], ["333", "222"])
        self.assertEqual(ret, False)

        ret = filter_str("111", ["111", "444"], ["333", "222"])
        self.assertEqual(ret, True)

    def test_get_all_files(self):
        ret = get_all_files(self.dir, ext=[".py"])
        logging.debug(ret)
        self.assertTrue(len(ret) == 2)

        ret = get_all_files(self.dir, ext=[".cpp"])
        logging.debug(ret)
        self.assertTrue(len(ret) == 1)

        ret = get_all_files(self.dir, ext=[".go"])
        logging.debug(ret)
        self.assertTrue(len(ret) == 1)

        ret = get_all_files(self.dir, ext=[".java"])
        logging.debug(ret)
        self.assertTrue(len(ret) == 0)

        ret = get_all_files(self.dir)
        logging.debug(ret)
        self.assertTrue(len(ret) == 4)

        ret = get_all_files(self.dir, non_ext=[".go", ".java"])
        logging.debug(ret)
        self.assertTrue(len(ret) == 3)

    def test_get_all_dirs(self):
        ret = get_all_dirs(self.dir)
        logging.debug(f"{len(ret)}, {ret}")
        self.assertTrue(len(ret) == 5)

    def test_get_all_dirs_and_files(self):
        ret = get_all_dirs_and_files(self.dir)
        logging.debug(f"{len(ret)}, {ret}")
        self.assertTrue(len(ret) == 9)

    def test_get_all_ext(self):
        ret = get_all_ext(self.dir)
        self.assertTrue(len(ret) == 3)

    def test_del_file_del_empty_dir(self):
        # root_dir
        #   subdir1
        #     subdir1_1
        #        file.go
        #     file.go
        #   subdir2
        #     file.go
        #   subdir3
        #   file.go
        filename = "file.go"
        root_dir = tempfile.mkdtemp()
        logging.debug(root_dir)
        os.makedirs(root_dir, exist_ok=True)
        write_file(os.path.join(root_dir, filename), "")

        dir = os.path.join(root_dir, "subdir1")
        os.mkdir(dir)
        logging.debug(dir)
        write_file(os.path.join(dir, filename), "")

        dir = os.path.join(dir, "subdir1_1")
        os.mkdir(dir)
        logging.debug(dir)
        write_file(os.path.join(dir, filename), "")

        dir = os.path.join(root_dir, "subdir2")
        os.mkdir(dir)
        logging.debug(dir)
        write_file(os.path.join(dir, filename), "")

        dir = os.path.join(root_dir, "subdir3")
        os.mkdir(dir)
        logging.debug(dir)

        del_assign_file(root_dir, filename)
        self.assertTrue(len(get_all_files(root_dir)) == 0)

        del_empty_dir(root_dir)
        self.assertFalse(os.path.exists(root_dir))

    def test_rename_dir_files(self):
        # root_dir
        #   subdir1
        #     subdir1_1
        #        *.py
        #        *.cpp
        #        *
        root_dir = tempfile.mkdtemp()
        logging.debug(root_dir)
        os.makedirs(root_dir, exist_ok=True)

        dir = os.path.join(root_dir, "subdir1")
        os.mkdir(dir)
        logging.debug(dir)

        dir = os.path.join(dir, "subdir1_1")
        os.mkdir(dir)
        logging.debug(dir)
        tmpfd, name = tempfile.mkstemp(suffix=".cpp", dir=dir)
        os.close(tmpfd)
        logging.debug(name)

        tmpfd, name = tempfile.mkstemp(suffix=".cpp", dir=dir)
        os.close(tmpfd)
        logging.debug(name)

        dir = os.path.join(root_dir, "subdir2")
        os.mkdir(dir)
        logging.debug(dir)
        tmpfd, name = tempfile.mkstemp(dir=dir)
        os.close(tmpfd)
        logging.debug(name)

        tmpfd, name = tempfile.mkstemp(dir=dir)
        os.close(tmpfd)
        logging.debug(name)

        ret = get_all_files(root_dir)
        logging.debug(ret)
        rename_dir_files(root_dir)
        ret = get_all_files(root_dir)
        logging.debug(ret)
        self.assertTrue(os.path.isfile(os.path.join(root_dir, "subdir1/subdir1_1", "1.cpp")))
        self.assertTrue(os.path.isfile(os.path.join(root_dir, "subdir1/subdir1_1", "2.cpp")))
        self.assertTrue(os.path.isfile(os.path.join(root_dir, "subdir2", "1")))
        self.assertTrue(os.path.isfile(os.path.join(root_dir, "subdir2", "2")))

        shutil.rmtree(root_dir)


# python3 -m pytest -o log_cli=true -o log_cli_level=DEBUG py_utils/src/fs/dir_test.py
if __name__ == "__main__":
    unittest.main()
