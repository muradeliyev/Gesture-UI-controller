from typing import Optional

PLAYLIST_PATH = "../../assets/songs"


class Music:
    def __init__(self, name: str, path: str, filename: str, liked: bool = False):
        self.name = name
        self.path = path
        self.filename = filename
        self.liked = liked

        self.previous = None
        self.next = None


_musics = [
    Music(
        name="Who's in your head?",
        path=f"{PLAYLIST_PATH}/jonas-brothers-whos-in-your-head.mp3",
        filename="jonas-brothers-whos-in-your-head.mp3",
        liked=False
    ),
    Music(
        name="Cool for the summer",
        path=f"{PLAYLIST_PATH}/demi-lovato-cool-for-the-summer.mp3",
        filename="demi-lovato-cool-for-the-summer.mp3",
        liked=True
    )
]


def get_playlist() -> list[Music]:
    playlist = list()

    for i, music in enumerate(_musics):
        if i != 0:
            music.previous = _musics[i - 1]
        if i != len(_musics) - 1:
            music.next = _musics[i + 1]
        playlist.append(music)

    return playlist
