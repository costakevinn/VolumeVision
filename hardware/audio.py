import math

import numpy as np

import config


class Tone:
    def __init__(self):
        self.target = 0.0
        self.gain = 0.0
        self.phase = 0
        self.stream = None
        if config.AUDIO_ENABLED:
            import sounddevice as sd

            self.stream = sd.OutputStream(
                samplerate=config.SAMPLE_RATE,
                channels=1,
                dtype="float32",
                device=config.AUDIO_DEVICE,
                callback=self.callback,
            )

    def set_volume(self, volume):
        self.target = volume / 100 * config.MAX_GAIN

    def callback(self, outdata, frames, time_info, status):
        samples = self.phase + np.arange(frames)
        gains = np.linspace(self.gain, self.target, frames)
        wave = np.sin(2 * math.pi * config.TONE_HZ * samples / config.SAMPLE_RATE)
        outdata[:, 0] = gains * wave
        self.phase = (self.phase + frames) % config.SAMPLE_RATE
        self.gain = self.target

    def __enter__(self):
        if self.stream:
            self.stream.start()
        return self

    def __exit__(self, *exc):
        if self.stream:
            self.stream.stop()
            self.stream.close()