import unittest
import logging
import os.path
import os

from src.av.audio_opt import AudioProcessor, SilenceAudioSegment
from src.av.probe import AVProp


class SilenceAudioSegmentTest(unittest.TestCase):
    def test_gen_slient_audio(self):
        audio_path = "test.mp3"
        SilenceAudioSegment.silent(duration=5000 * 2).export(audio_path)
        prob = AVProp(audio_path)
        logging.debug(f"duration: {prob.fmt_duration_sec()}")
        self.assertTrue(os.path.getsize(audio_path) > 0)
        self.assertTrue(prob.fmt_duration_sec() > 4)
        os.remove(audio_path)


class AudioProcessorTest(unittest.TestCase):
    def test_convert(self):
        audio_path = "test.mp3"
        SilenceAudioSegment.silent(duration=5000 * 2).export(audio_path)
        prob = AVProp(audio_path)
        logging.debug(f"duration: {prob.fmt_duration_sec()}")
        self.assertTrue(os.path.getsize(audio_path) > 0)
        self.assertTrue(prob.fmt_duration_sec() > 4)

        wav_file_path = "test.wav"
        AudioProcessor.convert_2_wav(audio_path, wav_file_path)
        prob_wav = AVProp(wav_file_path)
        logging.debug(f"duration: {prob_wav.fmt_duration_sec()}, {prob_wav.audio_ext}")
        self.assertTrue(os.path.getsize(wav_file_path) > 0)
        self.assertTrue(prob_wav.fmt_duration_sec() > 4)
        self.assertTrue(prob_wav.audio_ext == ".wav")

        mp3_file_path = "test_new.mp3"
        AudioProcessor.convert_2_mp3(wav_file_path, mp3_file_path)
        prob_mp3 = AVProp(mp3_file_path)
        logging.debug(f"duration: {prob_mp3.fmt_duration_sec()}, {prob_mp3.audio_ext}")
        self.assertTrue(os.path.getsize(wav_file_path) > 0)
        self.assertTrue(int(prob_mp3.fmt_duration_sec()) == int(prob.fmt_duration_sec()))
        self.assertTrue(prob_mp3.audio_ext == ".mp3")

        os.remove(audio_path)
        os.remove(wav_file_path)
        os.remove(mp3_file_path)


if __name__ == "__main__":
    unittest.main()
