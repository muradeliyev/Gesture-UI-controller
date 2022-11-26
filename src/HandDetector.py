import cv2
import mediapipe as mp

from typing import Optional
from src.models.Hand import Hand


class HandDetector:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands()
        self.drawing_utils = mp.solutions.drawing_utils

    def detect_hands(self) -> Optional[tuple[Hand, Hand]]:
        success, image = self.video_capture.read()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        multi_handedness = results.multi_handedness
        multi_hand_landmarks = results.multi_hand_landmarks

        if multi_handedness is None or multi_hand_landmarks is None:
            return None

        for handedness, landmarks in zip(multi_handedness, multi_hand_landmarks):
            label = handedness.classification[0].label

        # handedness = results.multi_handedness[0].classification[0].label

        # x = results.multi_hand_landmarks
        # if x:
        #     for c in x:
        #         print(c.landmark[2])
        #     print('-----------------------')


if __name__ == "__main__":
    detector = HandDetector()

    while True:
        detector.detect_hands()
