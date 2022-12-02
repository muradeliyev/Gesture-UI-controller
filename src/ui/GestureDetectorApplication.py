import tkinter as tk
import _thread as thread
import asyncio

from src.ui.components.Canvas import Canvas
from src.ui.components.ItemSong import ItemSong
from src.models.Music import get_playlist
from src.music_player.MusicPlayer import MusicPlayer
from src.HandDetector import HandDetector


class GestureDetectorApplication(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Gesture Music Controller")

        self.canvas = Canvas(self, width=600, height=600, bg='black')
        self.canvas.pack(fill='both', expand=1, side='left')

        self.music_frame = tk.Frame(self)

        self.music_list = tk.Listbox(self)
        songs = list(map(lambda s: s.name, get_playlist()))

        for song in songs:
            self.music_list.insert(0, song)

        for music in get_playlist():
            item = ItemSong(self.music_frame, name=music.name, artist=music.artist)
            item.pack(side='top', fill='x', expand=1)

        self.music_frame.pack(fill='y', expand=0)


def _draw_hand(canvas, hand, width, height):
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


def loop(canvas, music_player: MusicPlayer):
    width = float(canvas["width"])
    height = float(canvas["height"])

    detector = HandDetector()

    while True:
        asyncio.run(
            detector.detect_hands(
                lambda hand: _draw_hand(canvas, hand, width, height),
                onnext=music_player.next,
                onprevious=music_player.previous
            )
        )


if __name__ == "__main__":
    app = GestureDetectorApplication()
    player = MusicPlayer()
    thread.start_new_thread(loop, (app.canvas, player))
    app.mainloop()
