#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:   LiPingping
# Time:     2021/10/14 16:08
# Desc:     Open mini music player.
from PIL import Image, ImageTk
import pygame
import time
import os

import eyed3
import librosa
import random

import tkinter
from tkinter.filedialog import askdirectory, LEFT, RIGHT, CENTER, askopenfilename, NW, Menu, Menubutton, RAISED, \
    MULTIPLE
# from tkinter.filedialog import *
from tkinter import ttk

# from .tests.music_player_demo1 import start, stop
# from tests import music_player_demo1

# path config.
picture_path = './download/images/rain01.jpg'
img_width, img_height = 480, 360

# musicdl init.
from musicdl.musicdl import musicdl

mlclient = musicdl.musicdl(
    config={'logfilepath': 'musicdl.log', 'savedir': 'download/music', 'search_size_per_source': 5, 'proxies': {}})
# mlclient.run_by_input(['qq', 'netease'], user_input='ai')
records = {}

from music_player import Musicplayer
mplayer = Musicplayer()

# global config.
top = tkinter.Tk()  # 窗口
top.geometry('800x400')  # 窗口大小
top.title('Openi Music Player')  # 窗口名称

pygame.init()  # 窗口初始化
curent_music_file = tkinter.StringVar()  # current playing music file
curent_picture_file = tkinter.StringVar()  # current playing picture

path_musics = ''
filenames = []

volume = tkinter.StringVar()  # 获得文件列表
# v1 = tkinter.StringVar()  # 获得文件列表
var_mode = tkinter.IntVar()  # 播放顺序
var_mode2 = tkinter.IntVar()  # 播放状态

# var_mode3 = tkinter.IntVar()  # 播放进度
play_progress = tkinter.DoubleVar()  # 播放进度
music_secs = 1


# def Listloop():
#     global var_mode2
#     print(pygame.mixer.music.get_busy(), var_mode.get())
#     if var_mode.get() == 1 and pygame.mixer.music.get_busy() == False and var_mode2.get() == 1:
#         start()
#     elif var_mode.get() == 2 and pygame.mixer.music.get_busy() == False and var_mode2.get() == 1:
#         stop()
#     elif var_mode.get() == 3 and pygame.mixer.music.get_busy() == False and var_mode2.get() == 1:
#         print(c2.get())
#         print(filenames)
#         num = filenames.index(c2.get())
#         if num < len(filenames) - 1:
#             c2.current(num + 1)
#         else:
#             c2.current(0)
#         print(c2.get())
#         start()
#     elif var_mode.get() == 4 and pygame.mixer.music.get_busy() == False and var_mode2.get() == 1:
#         print(c2.get())
#         print(filenames)
#         num = filenames.index(c2.get())
#         if num < len(filenames) - 1:
#             c2.current(num + 1)
#             print(c2.get())
#             start()
#         else:
#             stop()
#     elif var_mode.get() == 5 and pygame.mixer.music.get_busy() == False and var_mode2.get() == 1:
#         print(c2.get())
#         print(filenames)
#         num = random.randint(0, len(filenames))
#         c2.current(num)
#         print(num, c2.get())
#         start()
#     # elif var_mode3.get()==0:
#     #     var_mode3.set(1)
#     top.after(3000, Listloop)


def set_volume(v):
    # print("INFO: set volume({},{})".format(v, int(v) // 100))
    pygame.mixer.music.set_volume(int(v) / 100)


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
#     top.after(1000, showtime)

# def show_play_progress():
#     num = pygame.mixer.music.get_pos() / 1000
#     print('INFO:  progress:', num, music_secs, float(num / music_secs))
#     volume_scale_bar.set(int(num / music_secs * 100))
#     print(volume_scale_bar.get())

def start():
    # print(filename+c2.get())
    global music_secs
    var_mode2.set(1)

    music_file = os.path.join(path_musics, c2.get())
    pygame.mixer.music.load(music_file)
    if c2.get()[-4:] == '.mp3':
        music_secs = int(eyed3.load(music_file).info.time_secs)
    else:
        music_secs = 40
    print(music_secs)
    print(var_mode.get())
    pygame.mixer.music.play()
    # w3.set(0)
    # pygame.mixer.music.play()  # 停止播放
    # print("test")

    # switch to pause button
    tkinter.Button(top, text="Pause", command=pause, width=2, height=2, bg="sky blue").place(relx=0.5, rely=0.95,
                                                                                             anchor=CENTER)


def stop():
    var_mode2.set(0)
    pygame.mixer.music.stop()  # 停止播放


def pause():
    var_mode2.set(0)
    pygame.mixer.music.pause()  # 暂停

    # switch to play button
    tkinter.Button(top, text="Play", command=start, width=3, height=3, bg="sky blue").place(relx=0.5, rely=0.95,
                                                                                            anchor=CENTER)


def unpause():
    var_mode2.set(1)
    pygame.mixer.music.unpause()  # 继续播放


def mplayer_backsong():
    pass


def mplayer_nextsong():
    pass


def musicplay():
    # global filename, filenames
    global path_musics, filenames
    # seach for music files.
    path_musics = askdirectory()
    curent_music_file.set(path_musics)
    filenames = []
    for f in os.listdir(path_musics):
        filenames.append(f)
    c2['value'] = filenames
    c2.current(0)

    valores.set(filenames)

    # # lbTime = tkinter.Label(top, anchor='w')
    # # lbTime.place(x=25, y=150)


def play_selected():
    reslist = list()
    seleccion = lstbox.curselection()
    for i in seleccion:
        entrada = lstbox.get(i)
        reslist.append(entrada)
    for val in reslist:
        print(val)
    songinfos = []
    for item in reslist:
        songinfo = records.get(item[0], '')
        if songinfo:
            print(songinfo)
            print(os.path.join(songinfo['savedir'], songinfo['savename']+'.'+songinfo['ext']))
            songinfos.append(songinfo)
    mlclient.download(songinfos)
    # print(songinfos[0].keys)
    mplayer.set_config(songinfos)
    mplayer.play()

def play_all():
    songinfos = []
    songs_items = valores.get()
    for item in songs_items:
        songinfo = records.get(item[0], '')
        if songinfo:
            songinfos.append(songinfo)
    mlclient.download(songinfos)

def search_music_in_musicdl():
    global records
    keyword = search_entry.get()
    print("INFO: search keyword:{}".format(keyword))
    song_items, records = mlclient.run_by_input(['qq', 'netease'], keyword)
    valores.set(song_items)

if __name__ == '__main__':
    img_open = Image.open(picture_path, "r").resize((img_width, img_height))
    img = ImageTk.PhotoImage(img_open)

    pygame.mixer.music.set_volume(1)  # 设置音量
    # top.attributes('-alpha', 1)  # 设置透明度
    # Listloop()
    # var_mode2.set(0)
    # var_mode3.set(1)

    mb = Menubutton(top, text="File", borderwidth=1, relief="groove")
    # mb.grid()
    mb.menu = Menu(mb, tearoff=0)
    mb["menu"] = mb.menu
    mb.menu.add_command(label="Open music folder", command=musicplay)
    mb.menu.add_separator()
    mb.menu.add_command(label="Open picture folder", command=select_pictures)
    # mb.pack()
    mb.place(x=5, y=5)

    # # 选择文件
    # tkinter.Button(top, text="Open directory", command=musicplay, width=10, bg="sky blue").place(x=20, y=20)
    tkinter.Entry(top, text=curent_music_file, width=25, state='readonly').place(x=120, y=20)
    # # tkinter.Button(top, text="Open directory", command=musicplay, width=10, bg="sky blue").pack(padx=5, pady=20, side=LEFT)
    # # tkinter.Entry(top, text=curent_music_file, width=25, state='readonly').pack(padx=5, pady=20, side=LEFT)
    #
    # show music stacked list.
    c2 = ttk.Combobox(top, width=22)
    c2.pack()
    c2.place(x=120, y=90)

    # # 选择图片
    # tkinter.Button(top, text='Open pictures', command=select_pictures, width=10, bg="sky blue").place(x=20, y=55)
    e1 = tkinter.Entry(top, text=curent_picture_file, state='readonly', width=25)
    e1.place(x=120, y=55)
    l1 = tkinter.Label(top)  # 图片放置位置
    l1.place(x=320, y=0, width=480, height=360)
    l1.config(image=img)

    # search music using musicdl
    search_entry = tkinter.Entry(top, width=25, state='normal')
    search_entry.place(x=20, y=120)
    search_B1 = tkinter.Button(top, text="Search", command=search_music_in_musicdl, bg="sky blue", width=10, height=1)
    # search_B1.pack(padx=5, pady=5, side=LEFT)
    search_B1.place(x=180, y=120)

    # menu = Menu(top, tearoff=0, relief="groove")
    # menu.add_checkbutton(label="Item0", variable=volume)
    # menu.add_checkbutton(label="Item1", variable=volume)
    # menu.add_checkbutton(label="Item2", variable=volume)
    # # display the menu
    # listb = tkinter.Listbox(top)  # 创建两个列表组件
    # listb.insert(0, menu)
    # listb.pack()
    # top.config(menu=menu)

    valores = tkinter.StringVar()
    # valores.set("Carro Coche Moto Bici Triciclo Patineta Patin Patines Lancha Patrullas")

    # frame = tkinter.Frame(top, width=100, height=100)
    # frame.place(x=20, y=160)
    # frame.grid(column=0, row=0, sticky=(N, S, E, W))
    lstbox = tkinter.Listbox(top, listvariable=valores, width=40, height=9, selectmode=MULTIPLE)
    # lstbox.grid(column=0, row=0, columnspan=2)
    lstbox.place(x=20, y=180)
    btn = ttk.Button(top, text="Play", command=play_selected)
    # btn.grid(column=1, row=1)
    btn.place(x=120, y=150)

    btn = ttk.Button(top, text="Select all", command=play_all)
    # btn.grid(column=1, row=1)
    btn.place(x=20, y=150)

    # 播放设置
    # var_mode.set(1)
    # sinloop = tkinter.Radiobutton(top, variable=var_mode, value=1, text="单曲循环")
    # sinloop.place(x=20, y=100)
    # single = tkinter.Radiobutton(top, variable=var_mode, value=2, text="单曲播放")
    # single.place(x=20, y=120)
    # allloop = tkinter.Radiobutton(top, variable=var_mode, value=3, text="列表循环")
    # allloop.place(x=20, y=140)
    # allsin = tkinter.Radiobutton(top, variable=var_mode, value=4, text="顺序播放")
    # allsin.place(x=20, y=160)
    # ranloop = tkinter.Radiobutton(top, variable=var_mode, value=5, text="随机播放")
    # ranloop.place(x=20, y=180)

    # 开始，暂停，继续播放，结束播放
    tkinter.Button(top, text="Play", command=start, width=2, height=2, bg="sky blue").place(relx=0.5, rely=0.95,
                                                                                            anchor=CENTER)
    tkinter.Button(top, text="End", command=stop, width=2, height=2, bg="sky blue").place(relx=0.5, rely=0.95,
                                                                                          anchor=CENTER,
                                                                                          x=40, y=0)
    tkinter.Button(top, text="-1", command=mplayer_backsong, width=2, height=2, bg="sky blue").place(relx=0.5,
                                                                                                     rely=0.95,
                                                                                                     anchor=CENTER,
                                                                                                     x=-40, y=0)
    tkinter.Button(top, text="+1", command=mplayer_nextsong, width=2, height=2, bg="sky blue").place(relx=0.5,
                                                                                                     rely=0.95,
                                                                                                     anchor=CENTER,
                                                                                                     x=80, y=0)

    # # # 自己生成旋律
    # # e2 = tkinter.Entry(top, text='编曲名称', width=25)
    # # e2.place(x=120, y=130)
    # # e2.insert(0, '中国风')
    # # tkinter.Button(top, text="随机编曲", command=create, width=7, bg="sky blue").place(x=170, y=165)
    #
    # 音量
    volume.set(50)
    volume_scale_bar = tkinter.Scale(top, from_=0, to=100, orient="horizontal", width=3, length=100, variable=volume,
                                     command=set_volume)
    volume_scale_bar.place(x=20, y=360)
    volume_scale_bar.set(volume.get())

    # 透明度
    # # v1.set('100')
    # # w2 = tkinter.Scale(top, from_=30, to=100, orient="horizontal", length=100, variable=v1, command=screen, label="透明度")
    # # w2.place(x=180, y=290)
    # # w2.set(100)

    # 播放进度
    play_progress.set(0.0)
    play_progress_bar = tkinter.Scale(top, from_=0, to=100, orient="horizontal", width=2, length=800,
                                      variable=play_progress)
    play_progress_bar.place(x=0, y=340)
    play_progress_bar.set(play_progress.get())

    # # 时间
    # stime = tkinter.Label(top, text="", font=("Helvetica", 15))
    # stime.place(x=110, y=350)

    # showtime()
    top.mainloop()
