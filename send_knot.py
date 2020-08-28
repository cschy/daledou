# coding:utf-8
# import requests # 中文[\u4e00-\u9fa5]+
# from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import ActionChains

import time
from datetime import datetime
import re
import random
import os
import sys
from autoqq import *

# QQ_login()

browser = webdriver.Chrome()
browser.get('https://ui.ptlogin2.qq.com/cgi-bin/login?appid=614038002&style=9&s_url=https%3A%2F%2Fdld.qzapp.z.qq.com%2Fqpet%2Fcgi-bin%2Fphonepk%3Fcmd%3Dindex%26channel%3D0')
pre_title = browser.title
# browser.maximize_window()
f_account = open("acc.txt")
for i in f_account:
    print('账号：', i.split('----')[0])
    account_ = browser.find_element_by_id('u')
    account_.clear()
    account_.send_keys(i.split('----')[0])
    browser.find_element_by_id('p').send_keys(i.split('----')[1].rstrip())
    login = browser.find_element_by_id('go')
    login.click()
    time.sleep(1.5)    # 根据自身设备和网速而定
    cur_title = browser.title

    # 该死的验证码或者服务器出错
    if cur_title == pre_title:
        # if 服务器出错
        try:
            browser.find_element_by_id("tcaptcha_iframe")
        except:
            log.log('当前上网环境异常，请更换网络环境或在常用设备上登录或稍后再试。')
            try:
                browser.find_element_by_id('go').click()
            except:
                log.log('卡住了, 正在退出系统。。。')
                browser.quit()
                sys.exit()
        browser.switch_to.frame("tcaptcha_iframe")  # 切换到iframe
        time.sleep(0.5)
        drag = browser.find_element_by_id("tcaptcha_drag_thumb")
        offset = 98
        while(True):
            try:
                pre_src = browser.find_element_by_id('slideBg').get_property('src')
                # print('原图片链接: ', pre_src)
                action = ActionChains(browser)
                action.click_and_hold(drag).perform()
                for i in range(offset):
                    action.move_by_offset(xoffset=2, yoffset=0).perform()
                    action.reset_actions()
                time.sleep(0.5)
                action.release().perform()
                time.sleep(2)
                error_note = browser.find_element_by_id('tcaptcha_note')
            except:
                break
            else:
                cur_src = browser.find_element_by_id('slideBg').get_property('src')
                # print('当前图片链接: ', cur_src)
                if cur_src != pre_src:  # 若换图则重置偏移量
                    offset = 95
                else:
                    offset = offset + 6

    time.sleep(1)
    try:
        browser.find_element_by_link_text("爱の同心结").click()
    except:
        print('无同心结活动')
        browser.quit()
        f_account.close()
        sys.exit()
    browser.find_element_by_link_text("赠送").click()
    index = -1
    send_success = False
    for i in re.finditer(r'uin=(\d+)\">赠送', browser.page_source):
        index += 1
        if friend == i.group(1):
            browser.find_elements_by_link_text("赠送")[index].click()
            print('赠送成功')
            send_success = True
            break
    if send_success is False:
        print('没有好友：', friend)
    browser.find_element_by_link_text("返回大乐斗首页").click()
    browser.find_element_by_link_text("退出").click()
browser.quit()
f_account.close()