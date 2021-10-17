#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:   LiPingping
# Time:     2021/10/15 11:28
# Desc:

from tkinter import *

top = Tk()

mb = Menubutton(top, text="CheckComboBox", relief=RAISED)

mb.grid()

mb.menu = Menu(mb, tearoff=0)

mb["menu"] = mb.menu

Item0 = IntVar()

Item1 = IntVar()

Item2 = IntVar()

mb.menu.add_checkbutton(label="Item0", variable=Item0)

mb.menu.add_checkbutton(label="Item1", variable=Item1)

mb.menu.add_checkbutton(label="Item2", variable=Item2)

'''This part is only for testing

def Item_test():

if Item0.get() == True:

print "Item0 True"

elif Item0.get() == False:

print "Item0 False"

else:

print Item0.get()

if Item1.get() == True:

print "Item1 True"

elif Item1.get() == False:

print "Item1 False"

else:

print Item1.get()

if Item2.get() == True:

print "Item2 True"

elif Item2.get() == False:

print "Item2 False"

else:

print Item2.get()

button1 = Button(top, text="Item True/False Test", command = Item_test)

button1.pack()

'''

mb.pack()

top.mainloop()
