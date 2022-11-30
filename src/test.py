import tkinter as tk
import asyncio


def draw(event):
    global canvas
    r = 20
    x1 = event.x - r
    y1 = event.y - r
    x2 = event.x + r
    y2 = event.y + r
    canvas.delete('all')
    canvas.create_oval(x1, y1, x2, y2, fill='green', outline='green')


root = tk.Tk()

canvas = tk.Canvas(root, width=500, height=500, bg='black')
canvas.pack()

canvas.bind('<Motion>', draw)

root.mainloop()
