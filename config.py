import os
from pathlib import Path

import yaml

_file = yaml.safe_load((Path(__file__).parent / "config.yaml").read_text())

CAMERA_SOURCE = os.environ.get("CAMERA_SOURCE", "0")
AUDIO_DEVICE = os.environ.get("AUDIO_DEVICE") or None

MODEL_PATH = _file["model"]
FRAME_WIDTH = _file["frame_width"]
WINDOW = _file["window"]["mode"]
WINDOW_PORT = _file["window"]["port"]
MIN_DISTANCE = _file["distance"]["min"]
MAX_DISTANCE = _file["distance"]["max"]
TONE_HZ = _file["tone"]["hz"]
MAX_GAIN = _file["tone"]["max_gain"]
SAMPLE_RATE = _file["tone"]["sample_rate"]
AUDIO_ENABLED = _file["audio"]["enabled"]