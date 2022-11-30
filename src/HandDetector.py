import cv2
import asyncio
import mediapipe as mp

from typing import Callable, Any
from src.models.Hand import Hand
from src.models.Handedness import Handedness
from src.models.Point import Point

HandLandmark = mp.solutions.hands.HandLandmark


class HandDetector:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands()
        self.drawing_utils = mp.solutions.drawing_utils

    async def detect_hands(self, on_each_hand: Callable[[Hand], Any]) -> tuple[Hand] | None:
        results = await self._get_processed_hand_results()
        multi_handedness = results.multi_handedness
        multi_hand_landmarks = results.multi_hand_landmarks

        if multi_handedness is None or multi_hand_landmarks is None:
            return

        for handedness, handLms in zip(multi_handedness, multi_hand_landmarks):
            label = handedness.classification[0].label
            hand = Hand(
                landmarks=list(map(Point.from_landmark, handLms.landmark)),
                handedness=Handedness(label))

            on_each_hand(hand)

    async def _get_processed_hand_results(self):
        success, image = self.video_capture.read()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if success:
            return results


if __name__ == "__main__":
    import tkinter as tk
    import _thread as thread

    detector = HandDetector()

    root = tk.Tk()
    canvas = tk.Canvas(root, width=900, height=700, bg='black')
    canvas.pack()


    def loop():
        width = float(canvas["width"])
        height = float(canvas["height"])

        while True:
            asyncio.run(
                detector.detect_hands(lambda hand: _draw_hand(hand, width, height))
            )


    def _draw_hand(hand, width, height):
        # canvas.delete(hand.handedness.value)
        canvas.delete('all')
        for i, (x, y, z) in enumerate(hand.landmarks):
            cx = width - int(x * width)
            cy = int(y * height)
            r = z * 20

            if cx - r <= 0 or cx + r >= width:
                continue
            if cy - r <= 0 or cy + r >= height:
                continue

            canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="yellow", outline="yellow",
                               tags=hand.handedness.value)


    thread.start_new_thread(loop, tuple())
    root.mainloop()
