import cv2
import numpy as np

GREEN, RED, YELLOW, MAGENTA = (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255)
FONT = cv2.FONT_HERSHEY_SIMPLEX
CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17),
)  # fmt: skip


def draw_hand(frame, points):
    for a, b in CONNECTIONS:
        cv2.line(frame, points[a], points[b], GREEN, 2)
    for point in points:
        cv2.circle(frame, point, 4, RED, -1)


def draw_pinch(frame, thumb, index):
    cv2.line(frame, thumb, index, YELLOW, 3)
    cv2.circle(frame, thumb, 10, YELLOW, -1)
    cv2.circle(frame, index, 10, YELLOW, -1)


def draw_volume(frame, volume):
    top = int(np.interp(volume, [0, 100], [250, 90]))
    cv2.rectangle(frame, (30, 90), (60, 250), GREEN, 2)
    cv2.rectangle(frame, (30, top), (60, 250), GREEN, -1)
    cv2.putText(frame, f"{volume}%", (20, 275), FONT, 0.7, GREEN, 2)


def draw_fps(frame, fps):
    cv2.putText(frame, f"FPS: {int(fps)}", (20, 70), FONT, 1, MAGENTA, 2)