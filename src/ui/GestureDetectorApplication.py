import tkinter as tk
import _thread as thread

from src.ui.components.Canvas import Canvas


class GestureDetectorApplication(tk.Tk):

    def __init__(self):
        super().__init__()

        self.canvas = Canvas(self, width=400, height=500, bg='black')
        self.canvas.pack(fill='both', expand=1)

        self.mainloop()

    def start_with_new_thread(self, func):
        while True:
            thread.start_new_thread(func, tuple())
