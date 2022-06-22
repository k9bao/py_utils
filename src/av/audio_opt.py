import os
import shutil
import logging

from pydub import AudioSegment

from py_utils.src.cmd_util.cmd_utils import run_sys_command


FFMPEG_BIN = "ffmpeg"
SOUNDSTRETCH_BIN = "soundstretch"


class SilenceAudioSegment(AudioSegment):
    @classmethod
    def silent(cls, duration=1000, sample_width=2, frame_rate=44100, channels=2):
        frames = int(frame_rate * (duration / 1000)) // 2
        data = b"\0" * sample_width * channels * frames
        return cls(data, sample_width=sample_width, frame_rate=frame_rate, channels=channels)


class AudioProcessor:
    def __init__(self):
        pass

    @staticmethod
    def convert_2_wav(in_file, out_file):
        command = [FFMPEG_BIN, "-y", "-loglevel", "error", "-i", f"{in_file}", "-f", "wav", out_file]
        run_sys_command(command)
        return out_file

    @staticmethod
    def convert_2_mp3(in_file, out_file):
        command = [FFMPEG_BIN, "-y", "-loglevel", "error", "-i", in_file, "-c:a", "libmp3lame", "-q:a", "2", out_file]
        run_sys_command(command)

    @staticmethod
    def soundstretch_process(file, pitch, tempo=None, rate=None, bpm=None, quick=None, naa=None, speech=None):
        """
        输入音频文件(及各种效果参数)，输出mp3文件
        tempo=n : Change sound tempo by n percents  (n=-95..+5000 %)
        pitch=n : Change sound pitch by n semitones (n=-60..+60 semitones)
        rate=n  : Change sound rate by n percents   (n=-95..+5000 %)
        bpm=n   : Detect the BPM rate of sound and adjust tempo to meet 'n' BPMs.
                    If '=n' is omitted, just detects the BPM rate.
        quick   : Use quicker tempo change algorithm (gain speed, lose quality)
        naa     : Don't use anti-alias filtering (gain speed, lose quality)
        speech  : Tune algorithm for speech processing (default is for music)
        """
        if pitch and (pitch < -95 or pitch > 5000):
            logging.error(f"pitch para is error,{pitch} should in（-95,50000)", stack_info=True)
            return file

        (path_file, ext) = os.path.splitext(file)
        wav_file = path_file + ".wav"
        wav_file_out = path_file + "_soundtouch.wav"
        mp3_file_out = path_file + "_soundtouch.mp3"
        if not file.endswith("wav"):
            AudioProcessor.convert_2_wav(file, wav_file)
        else:
            wav_file = file

        command = [SOUNDSTRETCH_BIN, wav_file, wav_file_out]
        if pitch is not None:
            command.append(f"-pitch={pitch}")
        if tempo is not None:
            command.append(f"-tempo={tempo}")
        if rate is not None:
            command.append(f"-rate={rate}")
        if bpm is not None:
            command.append(f"-bpm={bpm}")
        if quick is not None:
            command.append(f"-quick={quick}")
        if naa is not None:
            command.append(f"-naa={naa}")
        if speech is not None:
            command.append(f"-speech={speech}")
        if len(command) == 3:
            shutil.move(file, mp3_file_out)
        else:
            logging.debug(command)
            run_sys_command(command)
            AudioProcessor.convert_2_mp3(wav_file_out, mp3_file_out)
        return mp3_file_out
