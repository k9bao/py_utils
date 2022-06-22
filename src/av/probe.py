import subprocess
import json
import re

from .av_common import audio_code_ext_map

FFPROBE_BIN = "ffprobe"


def probe(video_path):
    command = [
        FFPROBE_BIN,
        "-loglevel",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        video_path,
    ]

    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, __ = pipe.communicate()
    info = json.loads(out)
    if "format" in info and "duration" not in info["format"]:
        info["format"]["duration"] = 0
    return info


class AVProp:
    def __init__(self, url, probe=None) -> None:
        self.url = url
        self._probe = probe

    def get_probe(self):
        if not self._probe:
            self._probe = probe(self.url)
        return self._probe

    @property
    def vpx_alpha(self):
        if not hasattr(self, "_vpx_alpha"):
            self.get_probe()
            result = False
            if "streams" in self._probe:
                for s in self._probe["streams"]:
                    if s["codec_type"] == "video" and (s["codec_name"] == "vp8" or s["codec_name"] == "vp9"):
                        tags = s.get("tags", {})
                        if tags.get("alpha_mode") == "1" or tags.get("ALPHA_MODE") == "1":
                            result = True
                            break
            setattr(self, "_vpx_alpha", result)
        return self._vpx_alpha

    @property
    def audio_ext(self):
        if not hasattr(self, "_audio_ext"):
            result = ""
            self.get_probe()
            streams = self._probe.get("streams") or []
            for s in streams:
                if s["codec_type"] == "audio":
                    result = "." + (audio_code_ext_map.get(s["codec_name"]) or "mp4")
                    break
            setattr(self, "_audio_ext", result)
        return self._audio_ext

    @property
    def get_video_ext_default(self):
        if not hasattr(self, "_video_ext"):
            self.get_probe()
            if self.vpx_alpha:
                setattr(self, "_video_ext", ".webm")
            else:
                setattr(self, "_video_ext", ".mp4")
        return self._video_ext

    def video_code(self):
        self.get_probe()
        if "streams" in self._probe:
            for s in self._probe["streams"]:
                if s["codec_type"] == "video":
                    return s.get("codec_name", None)
        return ""

    def fmt_duration_sec(self):
        self.get_probe()
        if "format" in self._probe:
            if "duration" in self._probe["format"]:
                return float(self._probe["format"]["duration"])
        return 0.0

    # 0:音视频都没有, 1:只有视频(图片), 2:只有音频, 3:音视频都有
    def get_stream_type(self):
        self.get_probe()
        stream_type = 0
        if "streams" in self._probe:
            for s in self._probe["streams"]:
                if s["codec_type"] == "video":
                    stream_type |= 1
                if s["codec_type"] == "audio":
                    stream_type |= 2
        return stream_type

    def get_create_time(self):
        if not hasattr(self, "_get_create_time"):
            self.get_probe()
            result = None
            if "format" in self._probe:
                format = self._probe["format"]
                tags = format.get("tags", {})
                if tags.get("creation_time"):
                    result = tags["creation_time"]
            if result is None and "streams" in self._probe:
                for s in self._probe["streams"]:
                    tags = s.get("tags", {})
                    if tags.get("creation_time"):
                        result = tags.get("creation_time")
                        break

            setattr(self, "_get_create_time", result)
        return self._get_create_time

    # return format: 20180908_035042
    def get_create_time_format(self):
        result = "00000000_000000"
        create_time = self.get_create_time()
        if create_time:  # 2018-09-08T03:50:42.000000Z
            ll = re.split(r"[,.]", create_time)
            if len(ll) > 0:
                result = ll[0].replace("-", "").replace("T", "_").replace(":", "")  # 20180908_035042
        return result
