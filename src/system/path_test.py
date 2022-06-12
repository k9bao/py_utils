import logging
import sys
import unittest
import os.path
import os


# OsPathTest https://www.runoob.com/python/python-os-path.html
class OsPathTest(unittest.TestCase):
    def test_os_path(self):
        relate_file_name = __file__
        abs_file_name = os.path.abspath(relate_file_name)
        logging.debug(f"abspath: {relate_file_name}, {abs_file_name}")
        # self.assertTrue(len(abs_file_name) > len(relate_file_name))

        name = os.path.basename(abs_file_name)
        logging.debug(f"basename:{name}")
        ret = os.path.split(abs_file_name)
        logging.debug(f"split:{ret}")
        self.assertEqual(name, ret[1])
        ret = os.path.splitdrive(abs_file_name)
        logging.debug(f"splitdrive:{ret}")
        ret = os.path.splitext(abs_file_name)
        logging.debug(f"splitext:{ret}")

        ret = os.path.dirname(abs_file_name)
        logging.debug(f"dirname:{ret}")
        ret = os.path.exists(abs_file_name)
        logging.debug(f"exists:{ret}")
        ret = os.path.lexists(abs_file_name)
        logging.debug(f"lexists:{ret}")

        ret = os.path.getatime(abs_file_name)
        logging.debug(f"getatime:{ret}")
        ret = os.path.getmtime(abs_file_name)
        logging.debug(f"getmtime:{ret}")
        ret = os.path.getctime(abs_file_name)
        logging.debug(f"getctime:{ret}")
        ret = os.path.getsize(abs_file_name)
        logging.debug(f"getsize:{ret}")
        ret = os.path.isabs(abs_file_name)
        logging.debug(f"isabs:{ret}")
        ret = os.path.isfile(abs_file_name)
        logging.debug(f"isfile:{ret}")
        ret = os.path.isdir(abs_file_name)
        logging.debug(f"isdir:{ret}")
        ret = os.path.islink(abs_file_name)
        logging.debug(f"islink:{ret}")
        ret = os.path.ismount(abs_file_name)
        logging.debug(f"ismount:{ret}")
        ret = os.path.realpath(abs_file_name)  # 软连接执行真实文件
        logging.debug(f"realpath:{ret}")
        ret = os.path.relpath(abs_file_name, "..")
        logging.debug(f"relpath:{ret}")
        ret = os.path.samefile(abs_file_name, abs_file_name)
        logging.debug(f"samefile:{ret}")

        abs_file_name2 = os.path.join(os.path.dirname(abs_file_name), "test2.txt")
        ret = os.path.commonprefix([abs_file_name, abs_file_name2])
        logging.debug(f"commonprefix:{ret}")

        test_path = "/mnt/sub1/sub2"
        ret = os.path.join(test_path, relate_file_name)
        logging.debug(f"join:{ret}")

        fp1 = os.open(abs_file_name, os.O_RDONLY)
        fp2 = os.open(abs_file_name, os.O_RDWR)
        ret = os.path.sameopenfile(fp1, fp2)
        logging.debug(f"sameopenfile:{ret}")

        stat1 = os.stat(abs_file_name)
        stat2 = os.stat(abs_file_name)
        ret = os.path.samestat(stat1, stat2)
        logging.debug(f"samestat:{ret}")

        not_normal_file = "../TEST/./test.txt"
        ret = os.path.normcase(not_normal_file)  # window下会变为小写字母
        logging.debug(f"normcase: {not_normal_file}, {ret}")
        ret = os.path.normpath(not_normal_file)
        logging.debug(f"normpath: {not_normal_file} {ret}")

        path_file_name = "~/path_test.py"
        ret = os.path.expanduser(path_file_name)
        logging.debug(f"expanduser:{ret}")

        os.environ["MY_TEST"] = test_path
        path_file_name = "${MY_TEST}/path_test.py"
        ret = os.path.expandvars(path_file_name)
        logging.debug(f"expandvars:{ret}")

        if sys.platform == "darwin":
            self.assertTrue(os.path.supports_unicode_filenames)  # 文件名是否支持unicode编码
        else:
            self.assertFalse(os.path.supports_unicode_filenames)


if __name__ == "__main__":
    unittest.main()
