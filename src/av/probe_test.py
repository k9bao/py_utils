import unittest
import logging

from src.av.probe import AVProp


class FileTest(unittest.TestCase):
    def test_video_prop(self):
        prop = AVProp("http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4")
        # prop = VideoProp("/Users/guoxb/Documents/asset/big_buck_bunny.mp4")
        logging.debug(prop.get_probe())
        logging.debug(prop.vpx_alpha)
        logging.debug(prop.audio_ext)
        logging.debug(prop.video_ext)
        logging.debug(prop.video_code())
        logging.debug(prop.fmt_duration_sec())
        logging.debug(prop.get_stream_type())
        logging.debug(prop.get_create_time())
        self.assertFalse(prop.vpx_alpha)
        self.assertTrue(prop.audio_ext == ".m4a")
        self.assertTrue(prop.video_ext == ".mp4")
        self.assertTrue(prop.video_code() == "h264")
        self.assertTrue(prop.fmt_duration_sec() == 60.095)
        self.assertTrue(prop.get_stream_type() == 3)
        self.assertTrue(prop.get_create_time() == "2010-02-09T01:55:39.000000Z")


if __name__ == "__main__":
    unittest.main()
