from tkinter import *
from tkinter import filedialog
from win32api import GetSystemMetrics
import os
import pygame

root = Tk()
root.geometry(f"600x600+{int(GetSystemMetrics(0) / 3)}+{int(GetSystemMetrics(1) / 4)}")
root.title("Intra Player")
pygame.mixer.init()
count = 1
song_no = 0
vol = 1.0

play_img = PhotoImage(file="play-button.png")
next_img = PhotoImage(file="next-button.png")
prev_img = PhotoImage(file="prev-button.png")
pause_img = PhotoImage(file="pause-button.png")
rewind_img = PhotoImage(file="rewind.png")
head = PhotoImage(file="music_image.png")
os.chdir("D:\\Python-projects\\Music-Player\\songs")


def changedir():
    global folder
    folder = filedialog.askdirectory()
    os.chdir(folder)
    playlist.delete(0, END)
    list_song()


def list_song():
    songs = [fname for fname in os.listdir(os.getcwd()) if fname.endswith(".mp3") or fname.endswith(".mp4")]
    for i in songs:
        playlist.insert(END, i)


def music():
    global song_no
    try:
        songs = [fname for fname in os.listdir(os.getcwd()) if fname.endswith(".mp3") or fname.endswith(".mp4")]
        if song_no >= len(songs):
            song_no = 0
        elif song_no < 0:
            song_no = len(songs) - 1
        playlist.activate(song_no)
        song = songs[song_no]
        play_pause_but.config(image=pause_img)
        pygame.mixer_music.load(os.getcwd() + "\\" + song)
        pygame.mixer_music.play(loops=0)
    except IndexError:
        pass


def play():
    global count, vol
    if pygame.mixer_music.get_busy() == 1 and count == 1:
        pygame.mixer_music.unpause()
        play_pause_but.config(image=pause_img)
        count = 0
    elif count == 1:
        music()
        count = 0
    elif count == 0:
        pygame.mixer_music.pause()
        play_pause_but.config(image=play_img)
        count = 1

def next_song():
    global song_no, count
    song_no += 1
    count = 1
    music()
    pygame.mixer_music.pause()
    play_pause_but.config(image=play_img)


def prev_song():
    global song_no, count
    song_no -= 1
    count = 1

    music()
    pygame.mixer_music.pause()
    play_pause_but.config(image=play_img)


def rewind():
    pygame.mixer_music.set_pos(0)


def volume(self):
    pygame.mixer_music.set_volume(vol_scale.get() / 100)


menu = Menu(root)
menu.add_command(label="Change Folder", command=changedir)
root.config(menu=menu, bg="black")

heading = Label(root, image=head, bg="black").pack()
playlist = Listbox(root, width=54, font="None 14", selectbackground='white', selectforeground="black", relief=RAISED, )

play_pause_but = Button(root, image=play_img, borderwidth=0, activebackground="black", bg="black", command=play)
next_but = Button(root, image=next_img, borderwidth=0, activebackground="black", bg="black", command=next_song)
prev_but = Button(root, image=prev_img, borderwidth=0, activebackground="black", bg="black", command=prev_song)
rev_but = Button(root, image=rewind_img, borderwidth=0, activebackground="black", bg="black", command=rewind)
vol_scale = Scale(root, label="Volume", font="None 12", activebackground="black", troughcolor='yellow', bg="black",
                  orient=HORIZONTAL, fg="yellow",
                  length=350, width=20, command=volume)

play_pause_but.place(x=220, y=380)
playlist.pack(pady=30)
vol_scale.pack(side=BOTTOM)
next_but.place(x=320, y=380)
prev_but.place(x=110, y=380)
rev_but.place(x=410, y=380)

list_song()
pygame.mixer_music.set_volume(0.5)
vol_scale.set(50)
playlist.focus_set()
root.mainloop()
