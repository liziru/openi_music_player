#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:   LiPingping
# Time:     2021/10/14
# Desc:     Open mini music player.

# import eyed3
# import librosa
# import random
import os
import glob
import json
import time
import pygame
import tkinter
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory, LEFT, RIGHT, CENTER, askopenfilename, NW, Menu, Menubutton, RAISED, \
    MULTIPLE, N, S, E, W
from tkinter import ttk
# from tkinter.filedialog import *

# from .tests.music_player_demo1 import start, stop
# from tests import music_player_demo1
from Musicplayer import Musicplayer

# path config.
picture_path = '/home/lee/Desktop/workspace/tests/open_project/openi_music_player/download/images/rain01.jpg'
img_width, img_height = 480, 360

# Musicplayer init.
mplayer = Musicplayer()

# global config.
root = tkinter.Tk()  # 窗口
root.geometry('800x400')  # 窗口大小
root.title('Openi Music Player')  # 窗口名称

pygame.init()  # 窗口初始化

# curent_music_file = tkinter.StringVar()  # current playing music file
# curent_picture_file = tkinter.StringVar()  # current playing picture

def set_volume(v):
    ''' Set volume to v.'''
    # print("INFO: set volume({},{})".format(v, int(v) // 100))
    mplayer.set_volume(v)

def select_pictures():
    path_s = askopenfilename()
    curent_picture_file.set(path_s)
    img_open = Image.open(e1.get())
    img = ImageTk.PhotoImage(img_open)
    l1.config(image=img)
    l1.image = img


# def showtime():  # 显示时间
#     c = time.strftime("%H:%M:%S")
#     stime.configure(text=c)
#
#     num = pygame.mixer.music.get_pos() / 1000
#     print('jindu', num, longt, float(num / longt))
#     w3.set(int(num / longt * 100))
#     print(w3.get())
#
#     root.after(1000, showtime)

def show_play_progress():
    ''' Show playing progress. '''
    sec = pygame.mixer.music.get_pos() / 1000
    dur_secs = mplayer.get_cursong_duration()
    play_progress_bar["to"] = dur_secs
    play_progress_bar.set(sec)
    print('INFO:  playing progress:', sec, dur_secs, float(sec / (dur_secs + 1e-7)))


def set_play_progress(v):
    '''Set playing progress. '''
    # pygame.mixer.music.set_pos(v)
    print("WARNING: unsupported now.")


def open_musicdir_prepare_songinfo(music_dir):
    '''Prepare songinfo from json file.'''
    song_records = {}
    json_list = glob.glob(os.path.join(music_dir, "*.json"))
    assert len(json_list) != 0, "No json found."
    idx = 0
    for i, js in enumerate(json_list):
        with open(js, "r") as fpr:
            song_json = json.loads(fpr.read())
            song_records.update({str(idx): song_json})
            idx += 1
    mplayer.search_records = song_records
    songinfos = mplayer.get_songinfo_by_records(song_records)
    song_items = mplayer.get_showitems_by_songinfos(songinfos)
    return song_items


def musicplay():
    # seach for music files.
    musics_dir = askdirectory()
    # curent_music_file.set(path_musics)
    song_items = open_musicdir_prepare_songinfo(musics_dir)
    valores.set(song_items)


def mplayer_start_playing():
    ''' Start playing songs of playlist.'''

    mplayer.play()

    global btn_pause
    # switch to pause button
    btn_pause = tkinter.Button(root, text="Pause", command=mplayer_pause_playing, width=btn_play["width"],
                               height=btn_play["height"],
                               bg="sky blue")
    btn_pause.place(relx=0.5, rely=0.95, anchor=CENTER)
    btn_play.destroy()


def mplayer_pause_playing():
    ''' Pause playing.'''

    # pygame.mixer.music.pause()  # 暂停
    mplayer.pause()

    global btn_play
    # switch to play button
    btn_play = tkinter.Button(root, text="Play", command=mplayer_start_playing, width=btn_pause["width"],
                              height=btn_pause["height"], bg="sky blue")
    btn_play.place(relx=0.5, rely=0.95, anchor=CENTER)
    btn_pause.destroy()


def mplayer_stop():
    ''' Stop playing and empty playlist.'''
    mplayer.stop()


def mplayer_backsong():
    mplayer.play_last_song()


def mplayer_nextsong():
    mplayer.play_next_song()


def mplayer_add_songs_to_playlist():
    idxs = []
    seleccion = lstbox.curselection()
    for i in seleccion:
        idxs.append(lstbox.get(i)[0])

    mplayer.add_songs_to_playlist(idxs)


def mplayer_add_all_to_playlist():
    idxs = []
    songs_items = valores.get()
    for item in songs_items:
        idxs.append(item[0])
    mplayer.add_songs_to_playlist(idxs)


def mplayer_search_musics():
    keyword = search_entry.get()
    print("INFO: search keyword:{}".format(keyword))
    song_items = mplayer.musicdl_search(keyword)
    valores.set(song_items)


def refresh():
    ''' Refresh ui.'''
    playlist_items, cur_play_index = mplayer.get_playlist()
    if len(playlist_items) != 0:
        cbox_showlist['value'] = playlist_items
        cbox_showlist.current(cur_play_index)

    show_play_progress()
    root.after(3000, refresh)


if __name__ == '__main__':
    # img_open = Image.open(picture_path, "r").resize((img_width, img_height))
    img_open = Image.open(picture_path, "r")
    img = ImageTk.PhotoImage(img_open)

    root.attributes('-alpha', 1)  # 设置透明度

    mb = Menubutton(root, text="File", borderwidth=1, relief="groove")
    mb.menu = Menu(mb, tearoff=0)
    mb["menu"] = mb.menu
    mb.menu.add_command(label="Open music folder", command=musicplay)
    mb.menu.add_separator()
    mb.menu.add_command(label="Open picture folder", command=select_pictures)
    # mb.place(x=5, y=5)
    # mb.place(relx=0.1, rely=0.1)
    mb.grid(row=0, column=0, sticky=N + W, padx=1, pady=1, columnspan=1, rowspan=1)

    # # 选择文件
    # tkinter.Button(root, text="Open directory", command=musicplay, width=10, bg="sky blue").place(x=20, y=20)
    # tkinter.Entry(root, text=curent_music_file, width=25, state='readonly').place(x=120, y=20)
    # # tkinter.Button(root, text="Open directory", command=musicplay, width=10, bg="sky blue").pack(padx=5, pady=20, side=LEFT)
    # # tkinter.Entry(root, text=curent_music_file, width=25, state='readonly').pack(padx=5, pady=20, side=LEFT)

    # show music stacked list.
    cbox_showlist = ttk.Combobox(root, width=20)
    cbox_showlist.place(relx=0.5, rely=0.95, anchor=CENTER, x=200, y=0)
    # cbox_showlist.grid(row=1)

    # # 选择图片
    # tkinter.Button(root, text='Open pictures', command=select_pictures, width=10, bg="sky blue").place(x=20, y=55)
    # e1 = tkinter.Entry(root, text=curent_picture_file, state='readonly', width=25)
    # e1.place(x=120, y=55)
    l1 = tkinter.Label(root)  # 图片放置位置
    l1.config(image=img)
    l1.grid(row=0, column=3, columnspan=2, rowspan=4, sticky=N + E, padx=1, pady=1)
    # l1.place(x=320, y=0, width=480, height=360)

    # search music using musicdl
    search_entry = tkinter.Entry(root, textvariable=tkinter.StringVar(root, value="Ed Sheeran"), width=25,
                                 state='normal')
    # search_entry.place(x=20, y=120)
    search_entry.grid(row=1, column=0, columnspan=2, rowspan=1, sticky=N + W, padx=1, pady=1)
    search_B1 = tkinter.Button(root, text="Search", command=mplayer_search_musics, bg="sky blue", width=10, height=1)
    # search_B1.pack(padx=5, pady=5, side=LEFT)
    # search_B1.place(x=180, y=120)
    search_B1.grid(row=1, column=2, columnspan=1, rowspan=1, sticky=N + W, padx=1, pady=1)

    # menu = Menu(root, tearoff=0, relief="groove")
    # menu.add_checkbutton(label="Item0", variable=volume)
    # menu.add_checkbutton(label="Item1", variable=volume)
    # menu.add_checkbutton(label="Item2", variable=volume)
    # # display the menu
    # listb = tkinter.Listbox(root)  # 创建两个列表组件
    # listb.insert(0, menu)
    # listb.pack()
    # root.config(menu=menu)

    valores = tkinter.StringVar()
    # valores.set("Carro Coche Moto Bici Triciclo Patineta Patin Patines Lancha Patrullas")

    # frame = tkinter.Frame(root, width=100, height=100)
    # frame.place(x=20, y=160)
    # frame.grid(column=0, row=0, sticky=(N, S, E, W))
    lstbox = tkinter.Listbox(root, listvariable=valores, width=40, height=18, selectmode=MULTIPLE)
    lstbox.grid(row=2, column=0, rowspan=3, columnspan=3, sticky=N + W, padx=1, pady=1)
    # lstbox.place(x=20, y=180)
    btn_add = ttk.Button(root, text="Add", command=mplayer_add_songs_to_playlist)
    btn_add.grid(row=5, column=0, sticky=N + W, padx=1, pady=1)
    # btn_add.place(x=120, y=150)

    btn_addall = ttk.Button(root, text="Add all", command=mplayer_add_all_to_playlist)
    btn_addall.grid(row=5, column=2, sticky=N + W, padx=1, pady=1)
    # btn_addall.place(x=20, y=150)

    # 播放设置
    # var_mode.set(1)
    # sinloop = tkinter.Radiobutton(root, variable=var_mode, value=1, text="单曲循环")
    # sinloop.place(x=20, y=100)
    # single = tkinter.Radiobutton(root, variable=var_mode, value=2, text="单曲播放")
    # single.place(x=20, y=120)
    # allloop = tkinter.Radiobutton(root, variable=var_mode, value=3, text="列表循环")
    # allloop.place(x=20, y=140)
    # allsin = tkinter.Radiobutton(root, variable=var_mode, value=4, text="顺序播放")
    # allsin.place(x=20, y=160)
    # ranloop = tkinter.Radiobutton(root, variable=var_mode, value=5, text="随机播放")
    # ranloop.place(x=20, y=180)

    # 开始，暂停，继续播放，结束播放
    btn_play = tkinter.Button(root, text="Play", command=mplayer_start_playing, width=2, height=2, bg="sky blue")
    btn_play.place(relx=0.5, rely=0.95, anchor=CENTER)
    # btn_play.grid(row=7, column=5)
    btn_stop = tkinter.Button(root, text="Stop", command=mplayer_stop, width=2, height=2, bg="sky blue")
    btn_stop.place(relx=0.5, rely=0.95, anchor=CENTER, x=40, y=0)
    # btn_stop.grid(row=7, column=6)
    btn_back = tkinter.Button(root, text="-1", command=mplayer_backsong, width=2, height=2, bg="sky blue")
    btn_back.place(relx=0.5, rely=0.95, anchor=CENTER, x=-40, y=0)
    # btn_back.grid(row=7, column=4)
    btn_next = tkinter.Button(root, text="+1", command=mplayer_nextsong, width=2, height=2, bg="sky blue")
    btn_next.place(relx=0.5, rely=0.95, anchor=CENTER, x=80, y=0)
    # btn_next.grid(row=7, column=7)

    # # 自己生成旋律
    # # e2 = tkinter.Entry(root, text='编曲名称', width=25)
    # # e2.place(x=120, y=130)
    # # e2.insert(0, '中国风')
    # # tkinter.Button(root, text="随机编曲", command=create, width=7, bg="sky blue").place(x=170, y=165)
    #
    # 音量
    volume = tkinter.StringVar()  # 获得文件列表
    volume.set(12)
    volume_scale_bar = tkinter.Scale(root, from_=0, to=100, orient="horizontal", width=3, length=100, variable=volume,
                                     command=set_volume)
    volume_scale_bar.place(x=20, y=360)
    # volume_scale_bar.set(volume.get())

    # 透明度
    # # v1.set('100')
    # # w2 = tkinter.Scale(root, from_=30, to=100, orient="horizontal", length=100, variable=v1, command=screen, label="透明度")
    # # w2.place(x=180, y=290)
    # # w2.set(100)

    # 播放进度
    play_progress = tkinter.DoubleVar()  # 播放进度
    play_progress.set(0.0)
    play_progress_bar = tkinter.Scale(root, from_=0, to=100, orient="horizontal", width=2, length=800,
                                      variable=play_progress, command=set_play_progress)
    # play_progress_bar.set(play_progress.get())
    play_progress_bar.place(x=0, y=340)

    # # 时间
    # stime = tkinter.Label(root, text="", font=("Helvetica", 15))
    # stime.place(x=110, y=350)
    # showtime()

    root.after(3000, refresh)
    root.mainloop()
