#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:   LiPingping
# Time:     2021/10/15 20:22
# Desc:

from tkinter import *
from tkinter import ttk

main = Tk()
main.title("Multiple Choice Listbox")
main.geometry("+50+150")
frame = ttk.Frame(main, padding=(3, 3, 12, 12))
frame.grid(column=0, row=0, sticky=(N, S, E, W))

valores = StringVar()
valores.set("Carro Coche Moto Bici Triciclo Patineta Patin Patines Lancha Patrullas")

lstbox = Listbox(frame, listvariable=valores, selectmode=MULTIPLE, width=200, height=100)
lstbox.grid(column=0, row=0, columnspan=2)

def select():
    reslist = list()
    seleccion = lstbox.curselection()
    for i in seleccion:
        entrada = lstbox.get(i)
        reslist.append(entrada)
    for val in reslist:
        print(val)

btn = ttk.Button(frame, text="Choices", command=select)
btn.grid(column=1, row=1)

main.mainloop()

