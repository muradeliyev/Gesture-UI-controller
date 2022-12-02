from tkinter import Frame, Label
from PIL import ImageTk, Image


def get_liked_icon():
    return ImageTk.PhotoImage(
        Image.open('C:/Users/hp/Desktop/Dersler/Image processing/Project/assets/images/icon_liked.png')\
            .resize((24, 24), Image.ANTIALIAS)
    )


def get_unliked_icon():
    return ImageTk.PhotoImage(
        Image.open('C:/Users/hp/Desktop/Dersler/Image processing/Project/assets/images/icon_unliked.png') \
            .resize((24, 24), Image.ANTIALIAS)
    )


class ItemSong(Frame):

    def __init__(self, master, name: str, artist: str):
        super().__init__(master)

        self.name = Label(self, text=name, font='Helvetica 12 bold', justify='left')
        self.artist = Label(self, text=artist, font='Helvetica 10', justify='left')
        self.icon_like = Label(self, image=get_unliked_icon())

        self.name.grid(row=1, column=1, sticky='w')
        self.artist.grid(row=2, column=1, sticky='w')
        self.icon_like.grid(row=1, column=2, columnspan=2)

        self._playing = False
        self._is_liked = False

        self.configure(
            padx=8,
            pady=8
        )

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, playing: bool):
        if playing:
            self.configure(background='green')
        else:
            self.configure(background='transparent')
        self._playing = playing

    @property
    def is_liked(self):
        return self._is_liked

    @is_liked.setter
    def is_liked(self, liked: bool):
        if liked:
            self.icon_like.configure(image=get_liked_icon())
        else:
            self.icon_like.configure(image=get_unliked_icon())
        self._is_liked = liked
