from ttkthemes import themed_tk as tk
from tkinter import filedialog
from mutagen.mp3 import MP3
import tkinter.messagebox
from tkinter import ttk
from tkinter import *
from pygame import *
import threading
import time
import os

mixer.init()
root = tk.ThemedTk()
root.get_themes()
root.set_theme('breeze')
root.title('Music Player')
root.iconbitmap('C:/Users/PC/PycharmProjects/Music Player/logo.ico')
root.resizable(False, False)

status = ttk.Label(root, text='No music playing...', relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

left_frame = Frame(root, padx=20)
left_frame.pack(side=LEFT)
right_frame = Frame(root).pack()
top_frame = Frame(right_frame)
top_frame.pack()
middle_frame = Frame(right_frame, relief=RAISED)
bottom_frame = Frame(right_frame, relief=RAISED)
middle_frame.pack(padx=50, pady=30)
bottom_frame.pack()
length_of_song = ttk.Label(top_frame, text='Total Length : --:--', relief=GROOVE)
length_of_current = ttk.Label(top_frame, text='Current Time : --:--', relief=GROOVE)
length_of_song.pack()
length_of_current.pack()
paused = False
loaded = False

file_box = Listbox(left_frame)
file_box.pack()

playlist = []


def open_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_listbox(filename_path)


def add_to_listbox(filename):
    filename = os.path.basename(filename_path)
    index = 0
    file_box.insert(index, filename)
    playlist.insert(index, filename_path)
    file_box.pack()
    index += 1


def pause():
    global paused
    paused = True
    mixer.music.pause()
    status['text'] = 'Song has been paused'


def stop():
    if not loaded:
        tkinter.messagebox.showerror('Error', 'A song has not been opened...')
    if loaded:
        mixer.music.stop()
        status['text'] = "No music playing..."
        length_of_song['text'] = 'Total Length : --:--'
        length_of_current['text'] = 'Current Time : --:--'


def play():
    global paused
    if paused:
        global selected_song
        selected_song = file_box.curselection()
        selected_song = int(selected_song[0])
        play_song = playlist[selected_song]
        mixer.music.unpause()
        paused = False
        song_name = os.path.basename(play_song)
        status['text'] = 'Now playing ' + song_name[:-4]
    else:
        try:
            mixer.music.stop()
            time.sleep(1)
            selected_song = file_box.curselection()
            selected_song = int(selected_song[0])
            play_song = playlist[selected_song]
            global loaded
            loaded = True
            mixer.music.load(play_song)
            mixer.music.play()
            song_name = os.path.basename(play_song)
            status['text'] = 'Now playing ' + song_name[:-4]
            show_details(play_song)
        except:
            tkinter.messagebox.showerror('Error', 'A song has not been opened...')


def show_details(play_song):
    filedata = os.path.splitext(play_song)

    if filedata[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        songsound = mixer.Sound(play_song)
        total_length = songsound.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    length_of_song['text'] = 'Total Length : ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    runtime = 0
    while runtime <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(runtime, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            length_of_current['text'] = 'Current Time : ' + timeformat
            time.sleep(1)
            runtime += 1


def contact():
    tkinter.messagebox.showinfo('Contact', 'E-Mail: arshnoman2270@gmail.com\nInstagram: @arsh_noman\nTwitter: @arsh_noman')


def about():
    tkinter.messagebox.showinfo('About', 'e')


def help_menu():
    help_window = Toplevel()
    help_window.title('Help')
    help_window.iconbitmap('C:/Users/PC/PycharmProjects/Music Player/helpico.ico')
    help_window.resizable(False, False)
    help_img = PhotoImage(file='help.png')
    l_help = Label(help_window, image=help_img)
    l_help.pack()
    help_window.mainloop()


def exit_root():
    mixer.music.stop()
    root.destroy()


def volume(val):
    vol = float(val) / 100
    mixer.music.set_volume(vol)


def rewind():
    mixer.music.rewind()
    play()


def delete():
    selected_song = file_box.curselection()
    selected_song = int(selected_song[0])
    file_box.delete(selected_song)
    playlist.pop(selected_song)

menu_bar = Menu(root)
root.config(menu=menu_bar)

btn_add = ttk.Button(left_frame, text='+ Add', command=open_file).pack(side=LEFT)
btn_remove = ttk.Button(left_frame, text='- Del', command=delete).pack(side=LEFT)
submenu1 = Menu(menu_bar, tearoff=0)
submenu2 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Settings', menu=submenu1)
submenu1.add_command(label='Exit', command=exit_root)
submenu1.add_command(label='Help', command=help_menu)
menu_bar.add_cascade(label='File', menu=submenu2)
submenu2.add_command(label='Open', command=open_file)
submenu2.add_command(label='Contact', command=contact)
submenu2.add_command(label='About', command=about)

img_rewind = PhotoImage(file='rewind.png')
img_play = PhotoImage(file='play.png')
img_stop = PhotoImage(file='stop.png')
img_pause = PhotoImage(file='pause.png')
b_play = ttk.Button(middle_frame, image=img_play, command=play)
b_pause = ttk.Button(middle_frame, image=img_pause, command=pause)
b_stop = ttk.Button(middle_frame, image=img_stop, command=stop)
b_rewind = ttk.Button(bottom_frame, image=img_rewind, command=rewind)
volume_scale = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=volume)
b_play.pack(side=LEFT, padx=5)
b_pause.pack(side=LEFT, padx=5)
b_stop.pack(side=LEFT, padx=5)
b_rewind.grid(row=0, column=0)
volume_scale.set(70)
volume_scale.grid(row=0, column=1, pady=15, padx=30)
mixer.music.set_volume(0.7)

root.protocol('WM_DELETE_WINDOW', exit_root)
root.mainloop()
