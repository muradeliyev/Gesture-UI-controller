import pygame

from enum import Enum
from src.models.Music import Music, get_playlist
import time


def current_milli_time():
    return round(time.time() * 1000)


class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.time = current_milli_time()

        self.playlist = get_playlist()
        self.state = MusicPlayerState.IDLE
        self.loop = True
        self.current_music_index = -1

    def play(self, music: Music):
        pygame.mixer.music.load(music.path)
        pygame.mixer.music.play()

        self.state = MusicPlayerState.PLAYING

    def stop(self):
        pygame.mixer.music.stop()

        self.state = MusicPlayerState.STOPPED

    def pause(self):
        pygame.mixer.music.pause()

        self.state = MusicPlayerState.PAUSED

    def resume(self):
        pygame.mixer.music.unpause()

        self.state = MusicPlayerState.RESUMED

    def next(self):
        if not self.can_do_action() or self.current_music_index == self.count() - 1 and not self.loop:
            return

        if self.loop and self.current_music_index == self.count() - 1:
            self.current_music_index = 0
        else:
            self.current_music_index += 1

        print(self.current_music_index)
        next_music = self.playlist[self.current_music_index]
        self.play(next_music)

    def previous(self):
        if not self.can_do_action() or self.current_music_index == -1:
            return
        if self.current_music_index == 0 and self.loop:
            self.current_music_index = self.count() - 1
        else:
            self.current_music_index -= 1

        print(self.current_music_index)

        previous_music = self.playlist[self.current_music_index]
        self.play(previous_music)

    def count(self):
        return len(self.playlist)

    def can_do_action(self) -> bool:
        current = current_milli_time()
        diff = current - self.time
        self.time = current
        print(diff)
        return diff > 3000


class MusicPlayerState(Enum):
    PLAYING = "playing"
    STOPPED = "stopped"
    PAUSED = "paused"
    RESUMED = "resumed"
    IDLE = "idle"


if __name__ == "__main__":
    from src.models.Music import get_playlist
    import tkinter as tk

    root = tk.Tk()

    player = MusicPlayer()
    m = get_playlist()[0]
    tk.Button(root, text="play", command=lambda: player.play(m)).pack()
    tk.Button(root, text="pause", command=lambda: player.pause()).pack()
    tk.Button(root, text="resume", command=lambda: player.resume()).pack()
    tk.Button(root, text="stop", command=lambda: player.stop()).pack()
    tk.Button(root, text="previous", command=lambda: player.previous()).pack()
    tk.Button(root, text="next", command=lambda: player.next()).pack()

    root.mainloop()
