import os
import time
import win32gui
import win32api
import win32con
from ctypes import *
from pykeyboard import PyKeyboard
from pymouse import PyMouse

# 实例化PyKeyboard和PyMouse
m = PyMouse()
k = PyKeyboard()

friend = '2505190276'

def QQ_login():
    f_account = open("acc.txt")
    for i in f_account:
        # 打开qq
        os.startfile(r'D:\Tencent\QQ\Bin\QQScLauncher.exe')
        # 获取窗口的句柄
        time.sleep(2)
        # 获取窗口的句柄
        handle = win32gui.FindWindow(None, 'QQ')
        time.sleep(1)


        loginid = win32gui.GetWindowPlacement(handle)
        # print(loginid, loginid[4][0])
        k.press_key(k.shift_key)
        k.tap_key(k.tab_key)
        time.sleep(0.5)
        k.release_key(k.shift_key)
        k.type_string(i.split('----')[0])
        time.sleep(0.2)
        k.tap_key(k.tab_key)
        # for i in range(16):
        #     k.tap_key(k.backspace_key)
        k.type_string(i.split('----')[1].rstrip())
        time.sleep(0.2)
        k.tap_key(k.enter_key)

        time.sleep(5)
        handle = win32gui.FindWindow(None, 'QQ')
        loginedid = win32gui.GetWindowPlacement(handle)
        # print(loginedid)



        if loginedid[4] == loginid[4]:
            print('需拖动验证码')
        # friend = input('请输入你要加的号：')
        # time.sleep(0.5)
        # m.move(loginedid[4][0] + 148, loginedid[4][1] + 120)
        # time.sleep(0.5)
        # m.click(loginedid[4][0] + 148, loginedid[4][1] + 120)

        k.type_string(friend)
        time.sleep(1)
        m.click(loginedid[4][0] + 148, loginedid[4][1] + 252)
        time.sleep(1)
        k.tap_key(k.enter_key, n=3, interval=0.5)
        time.sleep(0.5)
        # m.click(loginedid[4][0] + 269, loginedid[4][1] + 16)



if __name__ == '__main__':
    QQ_login()