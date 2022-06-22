import unittest
import logging

from py_utils.src.cmd_util.cmd_utils import run_sys_command


class CmdTest(unittest.TestCase):
    def test_cmd(self):
        cmd = ["pwd"]
        logging.debug(cmd)
        result, err = run_sys_command(cmd)
        logging.debug(f"{err}, {result}")
        self.assertEqual(err, None)
        self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()
