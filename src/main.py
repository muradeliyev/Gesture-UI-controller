import cv2
import mediapipe as mp

import tkinter as tk
import _thread as thread

HandLandmark = mp.solutions.hands.HandLandmark

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


def loop():
    global canvas

    while True:
        success, image = cap.read()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        # checking whether a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:  # working with each hand
                for id, lm in enumerate(handLms.landmark):
                    # h, w, c = image.shape
                    w = float(canvas["width"])
                    h = float(canvas["height"])
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cx = w - cx

                    # canvas.delete('all')
                    if id == HandLandmark.INDEX_FINGER_TIP:
                        canvas.delete("pinky")
                        canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="yellow", outline="yellow", tags="pinky")
                    if id == HandLandmark.THUMB_TIP:
                        canvas.delete("thumb")
                        canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="pink", outline="pink", tags="thumb")

                # mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)


        # cv2.imshow("Output", image)
        # cv2.waitKey(1)


root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.pack(fill="both", expand=True)

# tk.Button(
#     root,
#     text="Start",
#     command=lambda: )
# ).pack(fill="both", expand=True)

thread.start_new_thread(loop, tuple())

root.mainloop()
