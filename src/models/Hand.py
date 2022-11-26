from src.models.Handedness import Handedness


class Hand:

    def __init__(self, landmarks: list[tuple[float, float]], handedness: Handedness):
        self.handedness = handedness
        self.landmarks = landmarks
