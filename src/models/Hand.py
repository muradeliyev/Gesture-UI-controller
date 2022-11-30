from src.models.Handedness import Handedness
from src.models.Point import Point


class Hand:
    def __init__(self, landmarks: list[Point], handedness: Handedness):
        self.handedness = handedness
        self.landmarks = landmarks
