import tkinter as tk

from src.models.Point import Point


class Canvas(tk.Canvas):
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #
    def draw_point(self, point: Point):
        cx = self.width - int(point.x * self.width)
        cy = int(point.y * self.height)
        r = point.z * 20

        if cx - r <= 0 or cx + r >= self.width:
            return
        if cy - r <= 0 or cy + r >= self.height:
            return

        self.create_oval(cx - r, cy - r, cx + r, cy + r, fill="yellow", outline="yellow")

        if point.label:
            self.create_text(cx, cy - r - 10, fill='red', text=point.label)
