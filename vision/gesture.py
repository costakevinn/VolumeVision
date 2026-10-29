import math

import config

THUMB_TIP = 4
INDEX_TIP = 8


def pinch(hand):
    thumb, index = hand[THUMB_TIP], hand[INDEX_TIP]
    ratio = (math.dist(thumb, index) - config.MIN_DISTANCE) / (
        config.MAX_DISTANCE - config.MIN_DISTANCE
    )
    return thumb, index, round(100 * min(max(ratio, 0), 1))