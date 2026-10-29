import time

import cv2

import config
from display import overlay
from display.window import Window
from hardware.audio import Tone
from hardware.cam import Camera
from vision.detector import HandDetector
from vision.gesture import pinch


def main():
    camera = Camera()
    detector = HandDetector()
    window = Window()
    previous = time.perf_counter()

    try:
        with Tone() as tone:
            while (frame := camera.read()) is not None:
                scale = config.FRAME_WIDTH / frame.shape[1]
                frame = cv2.flip(cv2.resize(frame, None, fx=scale, fy=scale), 1)

                volume = 0
                for hand in detector.detect(frame):
                    thumb, index, volume = pinch(hand)
                    overlay.draw_hand(frame, hand)
                    overlay.draw_pinch(frame, thumb, index)

                tone.set_volume(volume)
                overlay.draw_volume(frame, volume)

                now = time.perf_counter()
                overlay.draw_fps(frame, 1 / (now - previous))
                previous = now

                if not window.show(frame):
                    break
    finally:
        detector.close()
        camera.release()
        window.close()


if __name__ == "__main__":
    main()