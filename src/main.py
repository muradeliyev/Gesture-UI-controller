import cv2

from ui.GestureDetectorApplication import GestureDetectorApplication

import mediapipe as mp
import tkinter as tk
import _thread as thread

HandLandmark = mp.solutions.hands.HandLandmark

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


def loop(canvas: tk.Canvas):
    while True:
        success, image = cap.read()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        width = float(canvas["width"])
        height = float(canvas["height"])

        # checking whether a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:  # working with each hand
                for i, landmark in enumerate(handLms.landmark):
                    # h, w, c = image.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    cx = width - cx

                    # canvas.delete('all')
                    if i == HandLandmark.INDEX_FINGER_TIP:
                        canvas.delete("pinky")
                        canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="yellow", outline="yellow",
                                           tags="pinky")
                    if i == HandLandmark.THUMB_TIP:
                        canvas.delete("thumb")
                        canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="pink", outline="pink",
                                           tags="thumb")


root = GestureDetectorApplication()

thread.start_new_thread(loop, tuple())
