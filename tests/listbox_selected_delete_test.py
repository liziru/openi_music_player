#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:   LiPingping
# Time:     2021/10/15 20:19
# Desc:

'''1、当Radiobutton和Checkbutton设置的按钮数不够用的时候，选择用Listbox组件。
2、当创建一个Listbox组件时，他是空的。所以首先做的事情就是往里边添加n行文本。
使用insert方法，insert(第一个参数是索引号（0，END），第二个参数是所插入的字符串)。
'''
from tkinter import *

root = Tk()
theLB = Listbox(root)  # 这里还有一个selectmode选项，默认是BROWSE（单选,拖动鼠标或方向键可以改变选项），
# 还有SINGLE（纯粹单选），
# MULTIPLE（多选）
# EXTENDED(多选，但要按住shifu或者ctrl)
theLB.pack()
for item in ['貂蝉', '西施', '王昭君', '杨玉环']:
    theLB.insert(END, item)  # 为什么用END作为索引号？
    # 因为每迭代一次就要加到该数后边，其实就是最后一项END

theButton = Button(root, text='删除', command=lambda x=theLB: x.delete(ACTIVE))
# 有插入就有删除，呵呵！~ command返回一个函数。lambda 后边的是函数名，等号后边是参数，
# 再一个等号后边是返回值（return）。相当于
'''def x(theLB):
    return x.delete(ACTIVE)'''

theButton.pack()
mainloop()
