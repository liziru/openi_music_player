#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:   LiPingping
# Time:     2021/10/19 17:01
# Desc:

from threading import Thread
import time

def sayhi(name):
    time.sleep(2)
    print('%s say hello' %name)
if __name__ == '__main__':
    t=Thread(target=sayhi,args=('egon',))
    t.start()
    # t.join()
    print('主线程')
    print(t.is_alive())
    '''
    egon say hello
    主线程
    False
    '''