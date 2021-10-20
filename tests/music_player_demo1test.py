#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:   LiPingping
# Time:     2021/10/14 14:47
# Desc:     Music player copied from: https://www.pythonf.cn/read/123250

import tkinter
from PIL import Image, ImageTk
import pygame
import time
import os
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import ttk
import eyed3
import librosa
import random

# import 旋律生成 as cmusic
# import melody_generation as cmusic
top = tkinter.Tk()  # 窗口
top.geometry('800x400')  # 窗口大小
top.title('Openi Music Player')  # 窗口名称

pygame.init()  # 窗口初始化
file = tkinter.StringVar()  # 获得文件列表
# files = tkinter.StringVar()  # 获得文件列表
filename = tkinter.StringVar()
filenames = []
v = tkinter.StringVar()  # 获得文件列表
# v1 = tkinter.StringVar()  # 获得文件列表
var_mode = tkinter.IntVar()  # 播放顺序
var_mode2 = tkinter.IntVar()  # 播放状态
# var_mode3 = tkinter.IntVar()  # 播放进度
# v2 = tkinter.DoubleVar()  # 播放进度
# longt = 1


def search():  # 搜索文件
    # file_=askopenfilename()
    file_ = askdirectory()
    return file_

#
# def voice(t):  # 音量
#     t = int(t)
#     pygame.mixer.music.set_volume(t / 100)  # 设置音量
#
#
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
#

def musicplay():
    global filename, filenames
    f = search()  # 选择文件夹
    # print(f)
    filename = f
    file.set(f)
    f = os.listdir(f)
    filenames = []
    for fname in f:
        fp = os.path.join(fname)
        filenames.append(fp)
    c2['value'] = filenames
    c2.current(0)
    # lbTime = tkinter.Label(top, anchor='w')
    # lbTime.place(x=25, y=150)

#
# def start():
#     # print(filename+c2.get())
#     global longt
#     var_mode2.set(1)
#     print(filename + '/' + c2.get())
#     pygame.mixer.music.load(filename + '/' + c2.get())
#     # longt=int(librosa.get_duration(filename=filename+'/'+c2.get()))
#     if c2.get()[-4:] == '.mp3':
#         longt = eyed3.load(filename + '/' + c2.get())
#         longt = int(longt.info.time_secs)
#     else:
#         longt = 39
#     print(longt)
#     print(var_mode.get())
#     pygame.mixer.music.play()
#     # w3.set(0)
#     # pygame.mixer.music.play()  # 停止播放
#
#
# def stop():
#     var_mode2.set(0)
#     pygame.mixer.music.stop()  # 停止播放
#
#
# def pause():
#     var_mode2.set(0)
#     pygame.mixer.music.pause()  # 暂停
#
#
# def unpause():
#     var_mode2.set(1)
#     pygame.mixer.music.unpause()  # 继续播放
#
#
# def picture():  # 保存的路径不能有中文，若需要中文则吧/换成\
#     path_s = askopenfilename()
#     files.set(path_s)
#     img_open = Image.open(e1.get())
#     img = ImageTk.PhotoImage(img_open)
#     l1.config(image=img)
#     l1.image = img
#
#
# # def create():
# #     top = tkinter.Toplevel()
# #     top.title('使用提示')
# #     top.geometry("400x400")
# #     t = "关于照片，新建一个存放图片的文件，用英文命名，然后存里面的图片也用英文命名。关于音乐: 新建一个名字叫音乐的文件，把歌曲添加到该文件夹。"
# #     msg = tkinter.Message(top, text=t)
# #     msg.config(font=('times', 24, 'italic'))
# #     msg.place(x=0, y=0)
#
# def gettime():
#     t = time.strftime('%H%M%S')
#     s = int(t[0:2])
#     d = int(t[2:4])
#     f = int(t[4:6])
#     g = s * 60 * 60 + d * 60 + f
#     return g
#
#
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
#
#
# def create():
#     # cmusic.creatmusic(filename+'/'+e1.get())
#     # f=os.listdir(filename)
#     # filenames=[]
#     # for fname in f:
#     #     fp=os.path.join(fname)
#     #     filenames.append(fp)
#     # c2['value'] = filenames
#     pass
#
#
# # def lenth(v2):
# #     global var_mode2,var_mode3
# #     var_mode2.set(1)
# #     print(v2)
# #     var_mode3.set(int(v2) / 100)
# #     print(var_mode3.get())
# # pygame.mixer.music.play(0,num*longt)
# # print('hi',pygame.mixer.music.get_busy(),var_mode3.get())
#
# # def jindu():
# #     num=pygame.mixer.music.get_pos()
# #     print('jindu',num)
# #     w3.set(num/longt)
# #     print(w3.get())
# #     top.after(1000,jindu)

if __name__ == "__main__":
    # errmsg = 'Error!'
    img_open = Image.open('/home/lee/Pictures/Screenshot from 2021-09-08 11-51-57.png')
    img = ImageTk.PhotoImage(img_open)
    pygame.mixer.music.set_volume(1)  # 设置音量
    # top.attributes('-alpha', 1)  # 设置透明度
    # Listloop()
    # var_mode2.set(0)
    # var_mode3.set(1)
    # 选择文件
    tkinter.Button(top, text="选择文件夹", command=musicplay, width=10, bg="sky blue").place(x=20, y=20)
    tkinter.Entry(top, text=file, width=25, state='readonly').place(x=120, y=20)

    c2 = ttk.Combobox(top, width=22)
    c2.pack()
    c2.place(x=120, y=90)
    # # 选择图片
    # tkinter.Button(top, text='选择图片', command=picture, width=10, bg="sky blue").place(x=20, y=55)
    # e1 = tkinter.Entry(top, text=files, state='readonly', width=25)
    # e1.place(x=120, y=55)
    # l1 = tkinter.Label(top)  # 图片放置位置
    # l1.place(x=320, y=0)
    # l1.config(image=img)
    # l1.image = img
    # # 播放设置
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
    # # 开始，暂停，继续播放，结束播放
    # tkinter.Button(top, text="开始播放", command=start, width=7, bg="sky blue").place(x=100, y=225)
    # tkinter.Button(top, text="暂停播放", command=pause, width=7, bg="sky blue").place(x=170, y=245)
    # tkinter.Button(top, text="继续播放", command=unpause, width=7, bg="sky blue").place(x=170, y=205)
    # tkinter.Button(top, text="结束播放", command=stop, width=7, bg="sky blue").place(x=240, y=225)
    # # 自己生成旋律
    # e2 = tkinter.Entry(top, text='编曲名称', width=25)
    # e2.place(x=120, y=130)
    # e2.insert(0, '中国风')
    # tkinter.Button(top, text="随机编曲", command=create, width=7, bg="sky blue").place(x=170, y=165)
    #
    # # 音量
    # v.set('100')
    # w1 = tkinter.Scale(top, from_=0, to=100, orient="horizontal", length=100, variable=v, command=voice, label="音量")
    # w1.place(x=20, y=290)
    # w1.set(100)
    # # 透明度
    # v1.set('100')
    # w2 = tkinter.Scale(top, from_=30, to=100, orient="horizontal", length=100, variable=v1, command=screen, label="透明度")
    # w2.place(x=180, y=290)
    # w2.set(100)
    # # 播放进度
    # v2.set(0.0)
    # w3 = tkinter.Scale(top, from_=0, to=100, orient="horizontal", width=10, length=475, variable=v2)
    # w3.place(x=320, y=360)
    # w3.set(0)
    # # 时间
    # stime = tkinter.Label(top, text="", font=("Helvetica", 15))
    # stime.place(x=110, y=350)
    # showtime()
    top.mainloop()
