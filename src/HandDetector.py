import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands()
        self.drawing_utils = mp.solutions.drawing_utils

    def detect_hands(self):
        success, image = self.video_capture.read()

        print(success, image)


if __name__ == "__main__":
    detector = HandDetector()

    while True:
        detector.detect_hands()

