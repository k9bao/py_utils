import logging

from py_utils.src.av.audio_opt import SilenceAudioSegment
from py_utils.src.av.probe import AVProp

logging.basicConfig(
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s", level=logging.DEBUG
)

if __name__ == "__main__":

    audio_path = "test.mp3"
    SilenceAudioSegment.silent(duration=1000).export(audio_path)
    prob = AVProp(audio_path)
    logging.debug(f"duration: {prob.fmt_duration_sec()}")
