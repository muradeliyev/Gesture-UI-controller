import cv2
import asyncio
import mediapipe as mp

from typing import Callable, Any, Type
from src.models.Hand import Hand
from src.models.Handedness import Handedness
from src.models.Point import Point
from src.models.UIEvent import UIEvent

HandLandmark = mp.solutions.hands.HandLandmark


class HandDetector:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands()
        self.drawing_utils = mp.solutions.drawing_utils

    async def detect_hands(self, on_each_hand: Callable[[Hand], Any],
                           onnext, onprevious) -> tuple[Hand] | None:
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

            event = self.get_event(hand)
            if event is UIEvent.Next:
                onnext()
            elif event is UIEvent.Previous:
                onprevious()

    def get_event(self, hand) -> UIEvent:
        landmarks = hand.landmarks

        index_finger_tip = landmarks[Hand.INDEX_FINGER_TIP]
        index_finger_mcp = landmarks[Hand.INDEX_FINGER_MCP]
        thumb_tip = landmarks[Hand.THUMB_TIP]

        if hand.handedness == Handedness.LEFT and abs(
                index_finger_mcp.y - index_finger_tip.y) <= 20 and thumb_tip.y < index_finger_mcp.y and index_finger_tip.x > index_finger_mcp.x:
            return UIEvent.Previous
        elif hand.handedness == Handedness.RIGHT and abs(
                index_finger_mcp.y - index_finger_tip.y) <= 20 and index_finger_mcp.y > thumb_tip.y and index_finger_tip.x < index_finger_mcp.x:
            return UIEvent.Next

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
