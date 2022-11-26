import tkinter as tk


class GestureDetectorApplication(tk.Tk):

    def __init__(self):
        super().__init__()

        self.canvas = tk.Canvas(self, width=400, height=500, bg='black')
        self.canvas.pack(fill='both', expand=1)

        self.mainloop()
