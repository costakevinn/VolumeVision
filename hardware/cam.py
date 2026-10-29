import cv2

import config


class Camera:
    def __init__(self):
        source = config.CAMERA_SOURCE
        self.capture = cv2.VideoCapture(int(source) if source.isdigit() else source)
        if not self.capture.isOpened():
            raise SystemExit(f"Cannot open camera source: {source}")
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def read(self):
        ok, frame = self.capture.read()
        return frame if ok else None

    def release(self):
        self.capture.release()