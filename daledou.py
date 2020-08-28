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


def act_robot(id):
    if id == 0:
        act_login_gift()
    elif id == 1:
        act_guess_odd_even()
    elif id == 2:
        act_shenmo_zpan()
    elif id == 3:
        act_baby_machine()

def act_login_gift():
    try:
        browser.find_element_by_link_text("领取").click()
    except:
        log.log('登录有礼：今日已领')
    else:
        log.log('登录有礼：', re.findall(r'恭喜.*?<br />', browser.page_source))

def act_guess_odd_even():
    while True:
        a = random.random()
        if a < 0.5:
            try:
                browser.find_element_by_link_text("单数").click()
            except:
                log.log('猜单双：失败 or 已做过')
                break
            else:
                log.log('猜单：', re.findall(r'恭喜.*?<br />', browser.page_source))
        else:
            try:
                browser.find_element_by_link_text("双数").click()
            except:
                log.log('猜单双：失败 or 已做过')
                break
            else:
                log.log('猜双：', re.findall(r'恭喜.*?<br />', browser.page_source))

def act_shenmo_zpan():
    if re.search(r'免费抽奖一次', browser.page_source) is None:
        log.log('神魔转盘：今日已抽')
    else:
        browser.find_element_by_link_text("幸运抽奖").click()
        log.log('神魔转盘：', re.findall(r'恭喜.*?<br />', browser.page_source))

def act_baby_machine():
    if re.search(r'免费次数：1', browser.page_source) is None:
        log.log('开心娃娃机：今日已抓')
    else:
        browser.find_element_by_link_text("抓取一次").click()
        log.log('开心娃娃机：', re.findall(r'您抽取了.*?<br />', browser.page_source))


class LOG():
    def __init__(self, file):
        self.file = file
        self.STANDARD_HEAD = '{@inx version="1.0" encoding="UTF-8" max_item=3@}\n'
        self.LOG_BEGAN = '<log>'
        self.LOG_END = '</log>'
        self.check_exist()

    def check_exist(self):
        if os.path.exists(self.file) is False:
            print('日志文件不存在，正在创建...')
            f = open(self.file, 'w')
            f.write(self.STANDARD_HEAD)
            f.close()
            print('创建成功')

    def write(self, s):
        with open(self.file, "a+") as f:
            if s != self.LOG_BEGAN:
                f.write('\n' + s)
            else:
                f.seek(0)
                first_line = f.readline()
                # print('first_line:\n', first_line)
                content = f.read()
                # print('content:\n', content)
                max_item = 0
                try:
                    max_item = int(re.search(r'max_item=(\d+)', first_line).group(1))
                except:
                    print('文件有误，正在尝试修护文件...')
                    f.close()
                    self.respire(content)

                log_search = self.LOG_BEGAN + '.*?' + self.LOG_END
                log_search = re.compile(log_search, re.S)
                if len(re.findall(self.LOG_BEGAN, content)) >= max_item:
                    log_list = log_search.findall(content)
                    # print(log_list)
                    if len(log_list) != 0:
                        log_list.pop(0)
                    new_log = ''
                    for i in log_list:
                        new_log += i
                        new_log += '\n\n'

                    f_new = open("%s.new" % self.file, "w")
                    f_new.write(first_line + new_log + s)
                    f_new.close()
                else:
                    f.write('\n\n' + s)
        if os.path.exists("%s.new" % self.file):
            os.remove(self.file)
            os.rename("%s.new" % self.file, self.file)

    def respire(self, content):
        if os.path.exists(self.file):
            print('正在修复文件头...')
            f_respire = open("%s.respire" % self.file, 'w')
            f_respire.write(self.STANDARD_HEAD + content)
            f_respire.close()
            os.remove(self.file)
            os.rename("%s.respire" % self.file, self.file)
            print('修复成功')
        else:
            print('日志文件丢失，正在重新创建日志文件...')
            f_remake = open(self.file, 'w')
            f_remake.write(self.STANDARD_HEAD)
            f_remake.close()
            print('创建成功')

    def log(self, s, var=''):
        print(s+str(var))
        self.write(s+str(var))

class yaoshui_tili():
    def __init__(self, page, index, num):
        self.page = page
        self.index = index
        self.num = num

    def print_info(self):
        print('page: {}, index: {}, num: {}'.format(self.page, self.index, self.num))

def check_goods_num(name):
    browser.find_element_by_link_text("背包").click()
    cur_page = 1
    page_total_pattern = r'第\d+/(\d+)页'
    page_total_cpl = re.compile(page_total_pattern)
    page_total = int(page_total_cpl.search(browser.page_source).group(1))

    goods = r'</a><br />.*?>(.*?)</a>数量：(\d+)'
    goods = re.compile(goods)
    num = 0

    while cur_page <= page_total:
        for i in goods.finditer(browser.page_source.split('清理')[1]):

            if i.group(1) == name:
                print('找到了{}, 页数：{}, 数量{}'.format(name, cur_page, i.group(2)))
                num = int(i.group(2))
                break
        if num != 0:
            break
        if cur_page < page_total:
            browser.find_element_by_link_text("下页").click()
        cur_page += 1
    browser.find_element_by_link_text("返回大乐斗首页").click()
    return num

def yaoshui_tili_num(browser):
    browser.find_element_by_link_text("背包").click()
    browser.find_element_by_link_text("药水").click()
    cur_page = 1
    page_total_pattern = r'第\d+/(\d+)页'
    page_total_cpl = re.compile(page_total_pattern)
    page_total = int(page_total_cpl.search(browser.page_source).group(1))

    tili_pattern = r'([\u4e00-\u9fa5]+(?:\(\d*[\u4e00-\u9fa5]*\))?)</a>数量：(\d+)'
    tili_cpl = re.compile(tili_pattern)
    # print(re.findall(r'.*', browser.page_source))
    print(tili_cpl.findall(browser.page_source))
    tili_zhen = yaoshui_tili(-1, -1, 0)
    tili_da = yaoshui_tili(-1, -1, 0)
    tili_zhong = yaoshui_tili(-1, -1, 0)
    tili_xiao = yaoshui_tili(-1, -1, 0)
    tilis = []

    while (cur_page <= page_total):
        index = 0
        for i in tili_cpl.finditer(browser.page_source):
            if i.group(1) == '真体力(60点)':
                tili_zhen.num = int(i.group(2))
                tili_zhen.page = cur_page
                tili_zhen.index = index
            elif i.group(1) == '大体力(30点)':
                tili_da.num = int(i.group(2))
                tili_da.page = cur_page
                tili_da.index = index
            elif i.group(1) == '中体力':
                tili_zhong.num = int(i.group(2))
                tili_zhong.page = cur_page
                tili_zhong.index = index
            elif i.group(1) == '小体力(10点)':
                tili_xiao.num = int(i.group(2))
                tili_xiao.page = cur_page
                tili_xiao.index = index
            index += 1
        print('zhen{}, da{}, zhong{}, xiao{}'.format(tili_zhen.num, tili_da.num, tili_zhong.num, tili_xiao.num))
        if tili_zhen.num != 0 and tili_da.num != 0 and tili_zhong.num != 0 and tili_xiao.num != 0:
            tilis.append(tili_zhen)
            tilis.append(tili_da)
            tilis.append(tili_zhong)
            tilis.append(tili_xiao)
            break
        else:
            if (cur_page < page_total):
                browser.find_element_by_link_text("下页").click()
                cur_page += 1
            else:
                tilis.append(tili_zhen)
                tilis.append(tili_da)
                tilis.append(tili_zhong)
                tilis.append(tili_xiao)
                break
    return tilis

def yaoshui_use(browser):
    tilis = yaoshui_tili_num(browser)
    for i in tilis:
        i.print_info()
    browser.find_element_by_link_text("药水").click()
    max = 0
    tili_max = yaoshui_tili(-1, -1, 0)
    for i in tilis:
        if i.num >= max:
            max = i.num
            tili_max = i
    # 翻页到达
    # for i in range(tili_max.page - 1):
    #     browser.find_element_by_link_text("下页").click()

    # 跳转到达
    browser.find_element_by_name('jump').send_keys(tili_max.page)
    browser.find_element_by_xpath("//form/input[@value='跳到该页']").click()
    browser.find_elements_by_link_text("使用")[tili_max.index].click()

class pos_ledou():
    def __init__(self, relationship, page, index):
        self.relationship = relationship
        self.page = page
        self.index = index

    def print_info(self):
        print('relationship: {}, page: {}, index: {}'.format(self.relationship, self.page, self.index))

def ledou(tili, browser, use, pos):
    if tili >= 10:
        browser.find_elements_by_link_text("乐斗")[pos.index].click()
        state = 1
    else:
        if (use == True):
            yaoshui_use(browser)  # 去背包用药了不在乐斗界面了
            # 回到原来位置乐斗
            browser.find_element_by_link_text("乐斗").click()
            if pos.relationship != '好友':
                browser.find_element_by_link_text(pos.relationship).click()
            if pos.page >= 1:
                browser.find_element_by_name('jump').send_keys(pos.page)
                browser.find_element_by_xpath("//form/input[@value='跳到该页']").click()
            browser.find_elements_by_link_text("乐斗")[pos.index].click()
            state = 0
        else:
            state = -1
    # return state

browser = webdriver.Chrome()
browser.get('https://ui.ptlogin2.qq.com/cgi-bin/login?appid=614038002&style=9&s_url=https%3A%2F%2Fdld.qzapp.z.qq.com%2Fqpet%2Fcgi-bin%2Fphonepk%3Fcmd%3Dindex%26channel%3D0')
pre_title = browser.title
# browser.maximize_window()
f_account = open("account.txt")
for i in f_account:
    log = LOG("./log/%s" % i.split('----')[0] + '.inx')
    log.log(log.LOG_BEGAN)
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
        offset = 97
        while(True):
            log.log('滑块偏移量：', offset)
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
    # 时间
    weekday = datetime.now().isoweekday()
    log.log('时间：', datetime.now().strftime('%Y-%m-%d %A %H:%M:%S'))

    # 账号资料
    my_data = r'<.*?>(.*?)<'
    name = re.search(my_data, browser.page_source.split('侠侣</a><br />')[1]).group(1)
    browser.find_element_by_link_text(name).click()
    # 等级
    level = r'等级:(\d+)'
    level = int(re.search(level, browser.page_source).group(1))
    log.log('等级：', level)
    have_gang = True
    # 达人系统
    log.log('达人系统**********')
    browser.find_element_by_link_text("达人").click()
    daren_grade = r'当前级别：(\d+)'
    try:
        daren_grade = int(re.search(daren_grade, browser.page_source).group(1))
    except:
        daren_grade = 0
        log.log('你不是达人')
    else:
        daren_next_grade = int(re.search('下一等级：(\d+)', browser.page_source).group(1))
        daren_socre = int(re.search('达人积分：(\d+)', browser.page_source).group(1))
        daren_speed = int(re.search('成长速度：(\d+)', browser.page_source).group(1))
        daren_remain = int(re.search('剩余天数：(\d+)', browser.page_source).group(1))
        log.log('当前等级：{}，还差{}天到下一级，剩余天数；{}，'.format(daren_grade, (daren_next_grade - daren_socre) // daren_speed, daren_remain))
    browser.back()
    browser.find_element_by_link_text("门派").click()
    menpai = re.search(r'当前所属门派:([\u4e00-\u9fa5]+)', browser.page_source).group(1)
    pos_gongfeng, pos_qiecuo, pos_renwu, pos_dalao, pos_wuji, pos_xinfa= '', '', '', '', '', ''
    if menpai == '华山':
        pos_gongfeng, pos_qiecuo, pos_renwu, pos_dalao, pos_wuji, pos_xinfa = '西岳庙', '练功房', '玉泉院', '仙峪', '武器库', '思过崖'
    elif menpai == '峨眉':
        pos_gongfeng, pos_qiecuo, pos_renwu, pos_dalao, pos_wuji, pos_xinfa = '万年寺', '八叶堂', '五花堂', '金顶', '伏虎寺', '华藏寺'
    elif menpai == '无':
        log.log('门派：暂无')
    browser.find_element_by_link_text("返回大乐斗首页").click()


    # 现阶段专门收集任务种类，每天先手动完成4个任务系统（主要是乱斗和每日）
    # log.log('任务系统**********')
    # # 乱斗任务
    # browser.find_element_by_link_text("全民乱斗").click()
    # luandou = r'<br />(.*?)<a'
    # luandou_ = r'<br />(.*?)\('
    # log.log('乱斗任务：', re.findall(luandou, browser.page_source.split('刷新')[1].split('斗灵石')[0]))
    # f = open("task_luandou.txt", "a+")
    # fr = open("task_luandou.txt")
    # for i in re.findall(luandou_, browser.page_source.split('刷新')[1].split('斗灵石')[0]):
    #     enrolled = False
    #     for line in fr:
    #         if line.strip() == i:
    #             enrolled = True
    #             break
    #     fr.seek(0)
    #     if enrolled is False:
    #         f.write('\n' + i)
    # fr.close()
    # f.close()
    # browser.find_element_by_link_text("返回大乐斗首页").click()
    # # 日常任务
    # browser.find_element_by_link_text("任务").click()
    # daily = r'<br />.*?([\u4e00-\u9fa5]+).*?(替换任务|完成|已完成)'
    # #daily = r'<br />.*?([\u4e00-\u9fa5]+)</a>'
    # daily_task = re.findall(daily, browser.page_source.split('一键完成任务')[1].split('商店')[0])
    # log.log('日常任务：', daily_task)
    # f = open("task_daily.txt", "a+")
    # fr = open("task_daily.txt")
    # describe = r'任务描述：(.*?)(。|！|\()'
    # for i in daily_task:
    #     enrolled = False
    #     browser.find_element_by_link_text(i[0]).click()
    #     describe_ = re.search(describe, browser.page_source).group(1)
    #     for line in fr:
    #         if line.strip() == describe_:
    #             enrolled = True
    #             break
    #     fr.seek(0)
    #     if enrolled is False:
    #         f.write('\n' + describe_)
    #     browser.back()
    # fr.close()
    # f.close()
    # # 帮派任务
    # browser.find_element_by_link_text("帮派任务").click()
    # bprw = r'\d\.<a.*?([\u4e00-\u9fa5]+).*?([\u4e00-\u9fa5]+)'
    # gang_task = re.findall(bprw, browser.page_source)
    # log.log('帮派任务：', gang_task)
    # f = open("task_gang.txt", "a+")
    # fr = open("task_gang.txt")
    # describe = r'任务描述：(.*?)(。|！)'
    # for i in gang_task:
    #     enrolled = False
    #     browser.find_element_by_link_text(i[0]).click()
    #     describe_ = re.search(describe, browser.page_source).group(1)
    #     for line in fr:
    #         if line.strip() == describe_:
    #             enrolled = True
    #             break
    #     fr.seek(0)
    #     if enrolled is False:
    #         f.write('\n' + describe_)
    #     browser.back()
    # fr.close()
    # f.close()
    # browser.find_element_by_link_text("返回大乐斗首页").click()
    # # 门派任务
    # browser.find_element_by_link_text("门派").click()
    # browser.find_element_by_link_text(pos_renwu).click()
    # sect_task = r'委派：(.*?)\s+奖励'
    # log.log('门派任务：', re.findall(sect_task, browser.page_source))
    # f = open("task_sect.txt", "a+")
    # fr = open("task_sect.txt")
    # for i in re.findall(sect_task, browser.page_source):
    #     enrolled = False
    #     for line in fr:
    #         if line.strip() == i:
    #             enrolled = True
    #             break
    #     fr.seek(0)
    #     if enrolled is False:
    #         f.write('\n' + i)
    # fr.close()
    # f.close()
    # browser.find_element_by_link_text("返回大乐斗首页").click()
    # # req = input('是否继续?(y|else)：')
    # # if req != 'y':
    # #     browser.quit()
    # #     sys.exit()

    # 活动
    log.log('活动中心**********')
    act_list = ['登录有礼', '猜单双', '神魔转盘', '开心娃娃机']
    for i in range(len(act_list)):
        try:
            browser.find_element_by_link_text(act_list[i]).click()
        except:
            pass
        else:
            log.log(act_list[i] + '：正在进行中...')
            act_robot(i)


    # 侠士客栈
    log.log('侠士客栈**********')
    try:
        browser.find_element_by_link_text("侠士客栈").click()
    except:
        log.log('等级限制')
    else:
        try:
            browser.find_element_by_link_text("领取奖励").click()
            log.log(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
            browser.find_element_by_link_text("领取奖励").click()
            log.log(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
            browser.find_element_by_link_text("领取奖励").click()
            log.log(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
        except:
            log.log('已领取')
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 全民乱斗
    # 每周一更新竞技 周六领奖
    log.log('全民乱斗**********')
    try:
        browser.find_element_by_link_text("全民乱斗").click()
    except:
        log.log('等级限制')
    else:
        lingqu = re.findall(r'>领取', browser.page_source.split('乱斗任务')[0])
        for i in lingqu:
            browser.find_element_by_link_text("领取").click()
            log.log(re.search(r'领取成功！获得.*?<br />', browser.page_source).group().rstrip('<br />'))
        browser.find_element_by_link_text("|武林盟主").click()
        lingqu = re.findall(r'>领取', browser.page_source.split('乱斗任务')[0])
        for i in lingqu:
            browser.find_element_by_link_text("领取").click()
            log.log(re.search(r'领取成功！获得.*?<br />', browser.page_source).group().rstrip('<br />'))
        '''
        unfinished = r'<br />(.*?)\((\d+).*?奖励.*?([\u4e00-\u9fa5]+)'
        # 去完成任务
        count = -1
        lingqu = 0
        need_brush = False
        for i in re.finditer(unfinished, browser.page_source.split('刷新')[1]):
            count += 1
            print(i.group(1) + i.group(2) + i.group(3))
            if i.group(3) == '未完成':
                if i.group(1) == '报名武林大会' and datetime.now().hour >= 13:
                    browser.find_element_by_link_text("返回大乐斗首页").click()
                    browser.find_element_by_link_text("武林").click()
                    #。。。
                    browser.find_element_by_link_text("返回大乐斗首页").click()
                    lingqu += 1
                elif i.group(1) == '挑战竞技场并获得两次胜利':
                    pass
                elif i.group(1) == '挑战竞技场并获得三次胜利':
                    need_brush = True
                elif i.group(1) == '抢占他人地盘三次' :
                    print('任务：抢占他人地盘三次（要求太高，需要刷新）')
                    need_brush = True
                elif i.group(1) == '战胜4个好友或帮友,级差&lt;=10':
                    print('任务：战胜4个好友或帮友,级差<=10（难以完成，需要刷新）')
                    need_brush = True
                elif i.group(1) == '成功拦截他人镖车一次':
                    browser.find_element_by_link_text("返回大乐斗首页").click()
                    browser.find_element_by_link_text("镖行天下").click()
                    browser.find_element_by_link_text("刷新").click()
                    rob_dart = r'(\d+)\.(温良恭|吕青橙|蔡八斗)&nbsp;[\u4e00-\u9fa5]+\d+&nbsp;\d+'
                    rob_dart = re.compile(rob_dart)
                    remain_times = r'剩余拦截次数：(\d+)'
                    remain_times = re.compile(remain_times)
                    count = 0
                    while int(re.search(remain_times, browser.page_source).group(1)) > 0:
                        for i in re.finditer(rob_dart, browser.page_source):
                            if i.group(2) == '温良恭':
                                browser.find_elements_by_link_text("拦截")[int(i.group(1)) - 2].click()
                        browser.find_element_by_link_text("刷新").click()
                        count += 1
                        if count > 20:
                            print('没有找到垃圾镖车')
                            need_brush = True
                            break
                    browser.find_element_by_link_text("返回大乐斗首页").click()
                    browser.find_element_by_link_text("全民乱斗").click()
                    lingqu += 1
                else:
                    print('请系统收录未知任务：', i.group(1))
                    need_brush = True
            elif i.group(3) == '领取':
                lingqu += 1
        # 领取奖励
        for i in range(lingqu):
            browser.find_elements_by_link_text("领取")[i].click()
            print(re.search(r'领取成功！获得.*?<br />', browser.page_source).group())
        # 刷新
        print(need_brush)
        if need_brush is True:
            browser.find_element_by_link_text("刷新").click()
            try:
                if int(re.search(r'今日剩余免费次数：(\d+)', browser.page_source).group(1)) > 0:
                    browser.find_element_by_link_text("刷新").click()
            except:
                print('免费刷新次数已用完')
            browser.find_element_by_link_text("返回上一页").click()
        '''
        browser.find_element_by_link_text("返回大乐斗首页").click()


    # 武林盟主 兑换星石
    # 报名时间：1、3、5 12:00-23:55
    # 竞猜时间：2、4、6 12:00-20:55
    log.log('武林盟主**********')
    fighting_capacity = float(re.search(r'战斗力</a>:(.*?)<a', browser.page_source).group(1))
    try:
        browser.find_element_by_link_text("武林盟主").click()
    except:
        log.log('等级限制')
    else:
        if weekday == 1 or weekday == 3 or weekday == 5:
            try:
                browser.find_element_by_link_text("领取奖励").click()
                # print reward
            except:
                log.log('已经领取过竞猜奖励了')
            if datetime.now().hour >= 12:
                try:
                    if fighting_capacity >= 200 and fighting_capacity < 1000:
                        browser.find_elements_by_link_text("参与报名")[2].click()
                        log.log('报名青铜赛场成功')
                    elif fighting_capacity >= 1000 and fighting_capacity < 2000:
                        browser.find_elements_by_link_text("参与报名")[1].click()
                        log.log('报名白银赛场成功')
                    else:
                        browser.find_elements_by_link_text("参与报名")[0].click()
                        log.log('报名黄金赛场成功')
                except:
                    log.log('已经报名过了')
        elif weekday == 2 or weekday == 4 or weekday == 6:
            if datetime.now().hour >= 12:
                try:
                    browser.find_element_by_link_text("前往竞猜").click()#jingcai
                except:
                    log.log('已经竞猜过了')
                else:
                    while True:
                        try:
                            browser.find_element_by_link_text("选择").click()
                        except:
                            browser.find_element_by_link_text("确定竞猜选择").click()
                            log.log('竞猜成功')
                            break
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 判断是否有帮派
    browser.find_element_by_link_text("我的帮派").click()
    if re.search(r'你还没有申请加入任何帮派', browser.page_source) is None:
        have_gang = True
    else:
        have_gang = False
        log.log('帮派：暂无，申请加入1406288')
        browser.find_element_by_name('groups_id').send_keys('1406288')
        browser.find_element_by_xpath("//form/input[@value='申请加入']").click()
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 帮派黄金联赛 材料点斗技 别驻守
    if have_gang is True:
        log.log('帮派黄金联赛**********')
        browser.find_element_by_link_text("帮派黄金联赛").click()
        try:
            browser.find_element_by_link_text("领取帮派赛季奖励").click()
        except:
            log.log('没有帮派赛季奖励可领')
        try:
            browser.find_element_by_link_text("领取奖励").click()
            log.log(re.search(r'(恭喜您.*?)<br />', browser.page_source).group(1))
        except:
            log.log('没有轮次奖励可领')
        browser.find_element_by_link_text("返回大乐斗首页").click()


    # 帮派远征军 对应系统神匠坊，每周可以打一次
    if have_gang is True:
        log.log('帮派远征军**********')
        browser.find_element_by_link_text("帮派远征军").click()
        if weekday == 1:
            while True:
                while True:
                    try:
                        browser.find_element_by_link_text("领取奖励").click()
                    except:
                        break
                try:
                    browser.find_element_by_link_text("领取岛屿宝箱").click()
                except:
                    pass

                try:
                    browser.find_element_by_link_text("上一岛屿").click()
                except:
                    log.log('奖励已领完！')
                    break

        else:
            try:
                browser.find_element_by_link_text("领取奖励").click()
            except:
                log.log('没有节点奖励可领')
            try:
                browser.find_element_by_link_text("领取岛屿宝箱").click()
            except:
                log.log('当前岛屿宝箱不可领')
            try:
                browser.find_element_by_link_text("参战").click()
                browser.find_element_by_link_text("攻击").click()
            except:
                pass
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 帮派商会 换双属性星石
    if have_gang is True:
        log.log('帮派商会**********')
        browser.find_element_by_link_text("帮派商会").click()
        while True:
            try:
                browser.find_element_by_link_text("点击领取").click()
            except:
                break
        browser.find_element_by_link_text("兑换商店").click()
        try:
            re.search(r'已兑换', browser.page_source).group()
        except:
            count = -1
            for i in re.finditer(r'<br />(.*?\*\d+).*?兑换', browser.page_source.split('刷新兑换商品')[1]):
                count += 1
                if '狂暴石' in i.group(1) or '神愈石' in i.group(1):
                    browser.find_elements_by_link_text("兑换")[count].click()
                    log.log('成功兑换：', i.group(1))
                    print('index:', count)
                    break
        else:
            log.log('已兑换狂暴石or神愈石 or 没刷新出这两种石头')
        browser.find_element_by_link_text("返回大乐斗首页").click()


    # 问鼎天下 助威神格，积分兑换神魔残卷（对应系统神魔录，有多倍活动3级以上祝福会清零）
    # 争夺时间：1.6-6.6
    # 助威时间：6、6:00-19:30
    if have_gang is True:
        log.log('问鼎天下**********')
        try:
            browser.find_element_by_link_text("问鼎天下").click()
        except:
            log.log('等级限制')
        else:
            if weekday >= 1 and weekday <= 5:
                browser.find_element_by_link_text("资源点争夺").click()
                browser.find_element_by_link_text("领取奖励").click()
                if datetime.now().hour < 9:
                    try:
                        browser.find_element_by_link_text("放弃").click()
                    except:
                        pass
                argue_times = r'剩余抢占次数：(\d+)'
                for i in range(int(re.search(argue_times, browser.page_source).group(1)) - 1):
                    browser.find_element_by_link_text("攻占").click()
                browser.find_elements_by_link_text("攻占")[-1].click()
            elif weekday == 6:
                browser.find_element_by_link_text("区域淘汰赛").click()
                area_list = ['北寒', '南荒', '东海', '西泽']
                shenge_exist = False
                for i in area_list:
                    browser.find_element_by_link_text(i).click()
                    try:
                        browser.find_element_by_link_text("神ㄨ阁丶").click()
                        log.log('助威神阁成功！')
                        shenge_exist = True
                        break
                    except:
                        continue
                if shenge_exist is False:
                    log.log('神阁帮不在区域赛16强，请手动助威或检查程序是否错误！')
            else:
                browser.find_element_by_link_text("冠军排名赛").click()
                try:
                    browser.find_element_by_link_text("北寒冠军神ㄨ阁丶").click()
                    log.log('助威神阁成功')
                except:
                    log.log('不存在"北寒冠军神ㄨ阁丶"的链接！')
            browser.find_element_by_link_text("返回大乐斗首页").click()

    # 梦想之旅
    #  第四周周5用梦幻机票，5/6/7/8同理，八周一循环
    log.log('梦想之旅**********')
    browser.find_element_by_link_text("梦想之旅").click()
    browser.find_element_by_link_text("普通旅行").click()
    log.log(re.search(r'规则</a><br />(.*?)<br />', browser.page_source).group(1))
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 会武 助威无脑丐帮，兑换真黄金卷轴
    # 1-3试炼 4助威丐帮
    log.log('六门会武**********')
    if menpai != '无' and level >= 40:
        browser.find_element_by_link_text("会武").click()
        trial_list = ['初级试炼场', '中级试炼场', '高级试炼场']
        no_challenge = r'星期一~三：.*?([\u4e00-\u9fa5]+).*?([\u4e00-\u9fa5]+)'
        if weekday >= 1 and weekday <= 3:   # 优先从高级试炼场尝试
            # 应该先去看挑战记录打没打
            browser.find_element_by_link_text("挑战记录").click()
            challenge_time = re.search(r'时间：(.*?)\s', browser.page_source).group(1)
            if datetime.now().strftime('%Y-%m-%d') == challenge_time:
                log.log('今日已挑战')
            else:
                browser.back()
                for i in trial_list:
                    try:
                        browser.find_element_by_link_text(i).click()
                    except:
                        log.log("%s：已通过" % i)
                    else:
                        while True:
                            try:
                                browser.find_element_by_link_text('挑战').click()
                            except:
                                break
        elif weekday == 4:
            browser.find_element_by_link_text("冠军助威").click()
            try:
                browser.find_elements_by_link_text("助威")[3].click()
            except:
                log.log('已助威过丐帮')
        elif weekday == 5:
            log.log('六门会武进行中，请周末来领取奖励')
        else:
            browser.find_element_by_link_text("领奖").click()
            try:
                browser.find_element_by_link_text("领取").click()
            except:
                log.log(re.search(r'领奖.*?<br />(.*?)<br />', browser.page_source).group(1))

            else:
                log.log('领取成功')
        browser.find_element_by_link_text("返回大乐斗首页").click()
    else:
        log.log('无门派或等级小于40')


    # 门派邀请赛 v
    log.log('门派邀请赛**********')
    if menpai != '无' and level >= 40:
        browser.find_element_by_link_text("门派邀请赛").click()
        if weekday == 1 or weekday == 2:
            browser.find_element_by_link_text("排行榜").click()
            try:
                browser.find_element_by_link_text("领取奖励").click()
                log.log(re.search(r'规则</a><br />(.*?)<br />', browser.page_source).group(1))
            except:
                log.log('已领取过段位奖励')
                browser.back()
            try:
                browser.find_element_by_link_text("组队报名").click()
                browser.find_element_by_link_text("允许队友邀请好友").click()
            except:
                log.log('已组队')
            else:
                log.log("报名成功")
        else:
            pre_times = 0
            while int(re.search(r'剩余挑战次数：(\d+)', browser.page_source).group(1)) > 0 and int(re.search(r'剩余挑战次数：(\d+)', browser.page_source).group(1)) != pre_times:
                pre_times = int(re.search(r'剩余挑战次数：(\d+)', browser.page_source).group(1))
                browser.find_element_by_link_text("开始挑战").click()
            if int(re.search(r'剩余挑战次数：(\d+)', browser.page_source).group(1)) == pre_times:
                if pre_times == 0:
                    log.log('已打满10次!')
                else:
                    log.log('门派战书不足!')
            if weekday == 7:
                # 先看看材料够不够下一周
                browser.find_element_by_link_text("返回大乐斗首页").click()
                sect_book = check_goods_num('门派战书')
                sect_high_fragrance = check_goods_num('门派高香')
                browser.find_element_by_link_text("门派邀请赛").click()
                browser.find_element_by_link_text("商店").click()
                duihuan = r'--(.*?)--.*?兑换'
                count = -1
                for i in re.finditer(duihuan, browser.page_source):
                    count += 1
                    if i.group(1) == '门派高香':
                        if sect_high_fragrance < 7:
                            log.log('门派高香应兑换索引：', count)
                            for j in range(7):
                                browser.find_elements_by_link_text("兑换")[count].click()
                    elif i.group(1) == '门派战书':
                        if sect_book < 32:
                            log.log('门派战书应兑换索引：', count)
                            for j in range(3):
                                browser.find_elements_by_link_text("兑换10个")[count].click()
                            for j in range(2):
                                browser.find_elements_by_link_text("兑换")[count].click()
                log.log('已确保下周的门派材料充足！')
        browser.find_element_by_link_text("返回大乐斗首页").click()
    else:
        log.log('无门派或等级小于40')


    # 门派；
    log.log('门派**********')
    if menpai != '无':
        browser.find_element_by_link_text("门派").click()
        browser.find_element_by_link_text(pos_gongfeng).click()
        try:
            browser.find_element_by_link_text("点燃").click()
            browser.find_element_by_link_text("点燃").click()
        except:
            log.log('香炉全已点燃')
        browser.find_element_by_link_text("返回门派首页").click()
        browser.find_element_by_link_text(pos_qiecuo).click()
        browser.find_element_by_link_text("进入木桩训练").click()
        browser.find_element_by_link_text("进入同门切磋").click()
        browser.find_element_by_link_text("进入同门切磋").click()
        browser.find_element_by_link_text("返回门派首页").click()
        browser.find_element_by_link_text(pos_dalao).click()
        for i in range(len(browser.find_elements_by_link_text("切磋"))):
            browser.find_elements_by_link_text("切磋")[i].click()
        browser.find_element_by_link_text("返回门派首页").click()
        browser.find_element_by_link_text(pos_wuji).click()
        browser.find_element_by_link_text("返回门派首页").click()
        browser.find_element_by_link_text(pos_xinfa).click()
        browser.find_element_by_link_text("返回门派首页").click()
        browser.find_element_by_link_text(pos_renwu).click()
        while True:
            try:
                browser.find_element_by_link_text("完成").click()
                log.log(re.search(r'(恭喜您.*?)<br />', browser.page_source).group(1))
            except:
                break
        # 打印未完成任务委派：查看一名同门成员的资料&nbsp;&nbsp;奖励：门贡20<br />
        unfinished = r'委派：([\u4e00-\u9fa5]+).*?奖励：门贡\d+.*?([\u4e00-\u9fa5]+)'
        for i in re.finditer(unfinished, browser.page_source):
            if i.group(2) != '已完成':
                log.log('未完成任务：', i.group(1))
        browser.find_element_by_link_text("返回大乐斗首页").click()
    else:
        log.log('无门派')


    # 画卷迷踪 对应系统觉醒（有材料翻倍活动）
    log.log('画卷迷踪**********')
    try:
        browser.find_element_by_link_text("画卷迷踪").click()
    except:
        log.log('等级太低，暂未开放')
    else:
        pro_list = [0, 1, 2, 2, 0]
        if int(re.search(r'本日免费剩余次数：(\d+)', browser.page_source).group(1)) > 0:
            highest_level = int(re.search(r'我的最高记录：(\d+)', browser.page_source).group(1))
            current_level = int(re.search(r'当前所在关卡：(\d+)', browser.page_source).group(1))
            for i in range(highest_level - current_level - 4):
                browser.find_element_by_link_text("准备完成进入战斗").click()
                if int(re.search(r'本日免费剩余次数：(\d+)', browser.page_source).group(1)) == 0:
                    break
            while True:
                if int(re.search(r'本日免费剩余次数：(\d+)', browser.page_source).group(1)) == 0:
                    break
                try:
                    browser.find_elements_by_link_text("选择")[pro_list[-1]].click()
                except:
                    log.log('不用buff加成了')
                browser.find_element_by_link_text("准备完成进入战斗").click()
                if len(pro_list) != 0:
                    pro_list.pop()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 群雄逐鹿 周六报名 周一到周三14:00比赛，在此之前领奖励 对应系统铭刻（4级祝福值会清零）
    log.log('群雄逐鹿**********')
    try:
        browser.find_element_by_link_text("群雄逐鹿").click()
    except:
        log.log('等级太低，暂未开放')
    else:
        browser.find_element_by_link_text("报名").click()
        browser.find_element_by_link_text("领奖").click()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 幻境（现阶段吃药试试）对应系统星盘，优先兑换玛瑙石和翡翠石。
    # print('幻境(吃药)**********')
    # browser.find_element_by_link_text("幻境").click()
    # browser.find_element_by_link_text("返回大乐斗首页").click()
    # browser.find_element_by_link_text("幻境").click()
    # if int(re.search(r'挑战次数：(\d)', browser.page_source).group(1)) > 0:
    #     browser.find_element_by_link_text("乐斗村").click()
    #     while len(re.findall(r'挑战已结束，请重新开始挑战。', browser.page_source)) == 0:
    #         browser.find_element_by_link_text("乐斗").click()
    # browser.find_element_by_link_text("返回大乐斗首页").click()

    # 勋章馆

    # # 镖行天下 镖行天下对应系统专精（有活动）材料建议兑换大型和小型
    # print('镖行天下**********')
    # browser.find_element_by_link_text("镖行天下").click()
    # try:
    #     browser.find_element_by_link_text("护送完成").click()
    #     browser.find_element_by_link_text("领取奖励").click()
    # except:
    #     pass
    # if int(re.search(r'剩余护送次数：(\d+)', browser.page_source).group(1)) > 0:
    #     browser.find_element_by_link_text("护送押镖").click()
    #     browser.find_element_by_link_text("刷新押镖").click()
    #     browser.find_element_by_link_text("启程护送").click()
    #     browser.find_element_by_link_text("刷新").click()
    # pattern = r'剩余拦截次数：(\d)'
    # regex = re.compile(pattern, re.I | re.S)
    # while(True):
    #     for i in range(len(browser.find_elements_by_link_text("拦截"))):
    #         if int(regex.search(browser.page_source).group(1)) == 0:
    #             break
    #         browser.find_elements_by_link_text("拦截")[i].click()
    #     if int(regex.search(browser.page_source).group(1)) > 0:
    #         browser.find_element_by_link_text("刷新").click()
    #     else:
    #         break
    # browser.find_element_by_link_text("返回大乐斗首页").click()


    # 历练
    log.log('历练**********')
    browser.find_element_by_link_text("历练").click()
    experience_dict = {'玉龙雪山': '象仙', '玉龙湿地': '嗜血鬼王', '苍莽山': '马大王', '洞庭湖': '大鹏', '摩云山': '宋姜', '踏云镇': '霹雳头领', '东海龙宫': '夜叉元帅', '林松城': '虾兵头目', '林松郊外': '凶尸', '乐斗村': '山贼头领'}
    for k, v in experience_dict.items():
        try:
            browser.find_element_by_link_text(k).click()
        except:
            continue
        else:
            try:
                browser.find_element_by_link_text("下一页").click()
            except:
                pass
            else:
                for i in range(3):
                    browser.find_elements_by_link_text("乐斗")[-1].click()
                break

    # browser.find_element_by_link_text("玉龙雪山").click()
    # browser.find_element_by_link_text("下一页").click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    # browser.find_element_by_link_text("返回世界场景").click()
    #
    # browser.find_element_by_link_text("玉龙湿地").click()
    # browser.find_element_by_link_text("下一页").click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    # browser.find_element_by_link_text("返回世界场景").click()
    #
    # browser.find_element_by_link_text("苍莽山").click()
    # browser.find_element_by_link_text("下一页").click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    # browser.find_elements_by_link_text("乐斗")[9].click()
    browser.find_element_by_link_text("返回大乐斗首页").click()


    # 斗神塔
    browser.find_element_by_link_text("分享").click()
    browser.find_element_by_link_text("一键分享").click()
    have_share = int(re.search(r'今日分享次数：(\d+)', browser.page_source).group(1))
    total_share = int(re.search(r'今日分享次数：\d+/(\d+)', browser.page_source).group(1))
    browser.find_element_by_link_text("返回大乐斗首页").click()
    log.log('斗神塔**********')
    browser.find_element_by_link_text("斗神塔").click()
    if int(re.search(r'今日剩余次数：(\d+)', browser.page_source).group(1)) != 0:
        try:
            browser.find_element_by_link_text("结束挑战").click()
            browser.find_element_by_link_text("取消").click()
        except:
            pass
        browser.find_element_by_link_text("自动挑战").click()
        # tower_cd = int(re.search(r'战斗剩余时间：(\d+)', browser.page_source).group(1))
        # for i in range(total_share - have_share):
        #     browser.find_element_by_link_text("返回大乐斗首页").click()
        #     browser.find_element_by_link_text("分享").click()
        #     browser.find_element_by_link_text("一键分享").click()
        #     browser.find_element_by_link_text("返回大乐斗首页").click()
        #     time.sleep(tower_cd * 10)
        #     browser.find_element_by_link_text("斗神塔").click()
    else:
        log.log('今日已挑战')
    browser.find_element_by_link_text("返回大乐斗首页").click()


    # 抢地盘
    # log.log('抢地盘**********')
    # browser.find_element_by_link_text("抢地盘").click()
    # browser.find_element_by_link_text("抢地盘记录").click()
    # if re.search(r'今天', browser.page_source) is None:
    #     browser.back()
    #     browser.find_elements_by_link_text("使用")[0].click()
    #     browser.find_elements_by_link_text("使用")[1].click()
    #     browser.find_elements_by_link_text("使用")[2].click()
    #     pattern = r'守(\d+)次'
    #     regex = re.compile(pattern)
    #     no5 = True
    #     while(no5):
    #         count = -1
    #         browser.find_element_by_link_text("刷新地盘").click()
    #         for i in regex.finditer(browser.page_source):
    #             count += 1
    #             if int(i.group(1)) == 0:
    #                 browser.find_elements_by_link_text("攻占")[count].click()
    #                 no5 = False
    #                 break
    # else:
    #     log.log('今日已抢')
    #     browser.back()
    # browser.find_element_by_link_text("返回大乐斗首页").click()


    # 重出江湖
    log.log('重出江湖**********')
    try:
        browser.find_element_by_link_text("重出江湖").click()
    except:
        log.log('无重出江湖功能')
    else:
        try:
            browser.find_elements_by_link_text("回来玩吧！")[0].click()
            browser.find_elements_by_link_text("回来玩吧！")[1].click()
            browser.find_elements_by_link_text("回来玩吧！")[2].click()
        except:
            pass
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # # 十二宫
    # log.log('十二宫**********')
    # browser.find_element_by_link_text("十二宫").click()
    # xinggong = re.findall(r'([\u4e00-\u9fa5]+宫).*?扫荡', browser.page_source)[-1]
    # browser.find_element_by_link_text(xinggong).click()
    # if len(re.findall(r'你不幸被怪物干掉了', browser.page_source)) == 0:
    #     count = 0
    #     while True:
    #         if len(re.findall(r'你不幸被怪物干掉了', browser.page_source)) == 0:
    #             try:
    #                 browser.find_element_by_link_text("挑战").click()
    #                 log.log(re.findall(r'(获得了.*?)<br />', browser.page_source))
    #             except:
    #                 log.log('挑战次数不足')
    #                 break
    #         else:
    #             count += 1
    #             if count <= 1:
    #                 log.log('你不幸被怪物干掉了')
    #                 log.log('开始复活...')
    #                 browser.find_element_by_link_text("复活").click()
    #                 browser.find_elements_by_link_text("选择")[2].click()
    #                 browser.find_element_by_link_text("确认复活").click()
    #             else:
    #                 log.log('你不幸又被怪物干掉了')
    #                 break
    # else:
    #     log.log('今日已挑战')
    # browser.find_element_by_link_text("返回大乐斗首页").click()

    # 竞技场 河图洛书每天都要兑换上限10个
    log.log('竞技场**********')
    try:
        browser.find_element_by_link_text("竞技场").click()
    except:
        log.log('等级太低，暂未开放')
    else:
        while True:
            try:
                browser.find_element_by_link_text("免费挑战").click()
            except:
                log.log('不在赛季或免费次数用完')
                try:
                    browser.find_element_by_link_text("领取奖励").click()
                except:
                    log.log('已领取奖励')
                break
        browser.find_element_by_link_text("竞技点商店").click()
        browser.find_elements_by_link_text("兑换10个")[-1].click()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 踢馆 材料兑换凤凰羽毛
    if have_gang is True:
        log.log('踢馆**********')
        browser.find_element_by_link_text("踢馆").click()
        if weekday == 5:
            for i in range(5):
                browser.find_element_by_link_text("试练").click()
            browser.find_element_by_link_text("高倍转盘").click()
            # 可以吃药3次
            for i in range(3):
                browser.find_element_by_link_text("挑战").click() # 挑战>=3次
            print('可能还可以挑战')
        browser.find_element_by_link_text("领奖").click() #22后
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 掠夺 材料推荐先兑换上古玉镯，其次潜能果实
    if have_gang is True:
        log.log('掠夺**********')
        browser.find_element_by_link_text("掠夺").click()
        if weekday == 2:
            browser.find_element_by_link_text("掠夺").click()
            browser.find_elements_by_link_text("掠夺")[-1].click()
            ###
        elif weekday == 3:
            try:
                browser.find_element_by_link_text("领取胜负奖励").click()
            except:
                pass
        else:
            log.log('星期二和星期三再来')
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 矿洞 兑换奔流气息，神秘精华
    if have_gang is True:
        log.log('矿洞**********')
        browser.find_element_by_link_text("矿洞").click()
        try:
            browser.find_element_by_link_text("领取奖励").click()
        except:
            pass
        try:
            browser.find_element_by_link_text("挑战").click()
            log.log(re.search(r'你挑战.*?。', browser.page_source).group())
        except:
            log.log('矿洞未开启')
        else:
            while int(re.search(r'剩余次数：(\d)', browser.page_source).group(1)) > 0:
                try:
                    browser.find_element_by_link_text("挑战").click()
                    log.log(re.search(r'你挑战.*?。', browser.page_source).group())
                except:
                    break
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 邪神秘宝
    log.log('邪神秘宝**********')
    browser.find_element_by_link_text("邪神秘宝").click()
    mibao = re.findall(r'(\d+)时(\d+)分(\d+)秒后免费', browser.page_source)
    log.log('高级秘宝：' + mibao[0][0] + '时' + mibao[0][1] + '分' + mibao[0][2] + '秒后免费')
    log.log('极品秘宝：' + mibao[1][0] + '时' + mibao[1][1] + '分' + mibao[1][2] + '秒后免费')
    if mibao[0][0] == '0' and mibao[0][1] == '0' and mibao[0][2] == '0':
        browser.find_element_by_link_text("免费一次").click()
    if mibao[1][0] == '0' and mibao[1][1] == '0' and mibao[1][2] == '0':
        browser.find_element_by_link_text("免费一次").click()
    # 打印得到奖品
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 巅峰之战对应系统五行（有活动）
    if level >= 40:
        log.log('巅峰之战进行中**********')
        browser.find_element_by_link_text("巅峰之战进行中").click()
        if weekday == 1:
            try:
                browser.find_element_by_link_text("随机加入").click()
            except:
                log.log('已报名')
            else:
                browser.find_element_by_link_text("确定").click()
            browser.find_element_by_link_text("领奖").click()
        if weekday >= 3:
            log.log('请手动战斗')
        browser.find_element_by_link_text("返回大乐斗首页").click()


    # 徒弟经验及每日奖励
    log.log('徒弟经验及每日奖励**********')
    try:
        browser.find_element_by_link_text("领取徒弟经验").click()
    except:
        log.log('已领取徒弟经验 or 没有徒弟')
    browser.find_element_by_link_text("每日奖励").click()
    while True:
        try:
            browser.find_element_by_link_text("领取").click()
        except:
            break
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 经脉(活动升)
    # 我的帮派：领取活跃贡献、供奉、帮战、帮修


    # 帮派祭坛 兑换奥秘元素
    # browser.find_element_by_link_text("帮派祭坛").click()
    # if weekday == 1:
    #     browser.find_element_by_link_text("领取奖励").click()
    # while int(re.search(r'剩余次数：(\d+)', browser.page_source).group(1)) > 0:
    #     browser.find_element_by_link_text("转动轮盘").click()
    #     try:
    #         browser.find_elements_by_link_text("选择")[1].click()
    # browser.find_element_by_link_text("返回大乐斗首页").click()

    # 帮贡
    if have_gang is True:
        log.log('帮贡**********')
        browser.find_element_by_link_text("我的帮派").click()
        browser.find_element_by_link_text("领取").click()
        if int(re.search(r'12.\[(\d)/1\]', browser.page_source).group(1)) == 0:
            browser.back()
            browser.find_element_by_link_text("帮派守护神").click()
            browser.find_element_by_link_text("供奉守护神").click()
            page = r'第(\d+)/(\d+)页'
            gf = False
            while int(re.search(page, browser.page_source).group(1)) <= int(re.search(page, browser.page_source).group(2)):
                dan = r'<br />([\u4e00-\u9fa5].*?)\s数量：\d+.*?供奉'
                count = -1
                #小活力药水 数量：94<a href="//dld.qzapp.z.qq.com/qpet/cgi-bin/phonepk?zapp_uin=&amp;sid=&amp;channel=0&amp;g_ut=1&amp;cmd=oblation&amp;id=3386&amp;page=1">供奉
                for i in re.finditer(dan, browser.page_source.split('供奉守护神')[1]):
                    #print(i.group(1))
                    count += 1
                    if i.group(1) == '还魂丹':
                        browser.find_elements_by_link_text("供奉")[count].click()
                        gf = True
                        break
                if gf is True:
                    log.log('供奉了一个还魂丹')
                    break
                try:
                    browser.find_element_by_link_text("下页").click()
                except:
                    log.log('没有还魂丹了')
                    log.log('手动供奉')
                    break
        else:
            log.log('已供奉')
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 武林
    log.log('武林**********')
    browser.find_element_by_link_text("武林").click()
    if datetime.now().hour >= 13:
        try:
            browser.find_elements_by_link_text("随机报名")[-1].click()
        except:
            log.log('已报名')
        else:
            log.log('报名成功')
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 侠侣赛
    log.log('侠侣赛**********')
    try:
        browser.find_elements_by_link_text("侠侣")[1].click()
    except:
        print('等级不足或没有情侣')
    else:
        if weekday == 2 and datetime.now().hour >= 13:
            try:
                browser.find_elements_by_link_text("报名")[3].click()
            except:
                log.log('已报名')
            else:
                log.log('报名成功')
        browser.find_element_by_link_text("返回大乐斗首页").click()


    # 结拜赛
    log.log('结拜赛**********')
    try:
        browser.find_element_by_link_text("结拜").click()
    except:
        log.log('无结拜或有人等级不足30')
    else:
        if weekday == 1:
            try:
                browser.find_elements_by_link_text("报名")[-1].click()
            except:
                log.log('已报名')
        if weekday == 4:
            browser.find_element_by_link_text("助威").click()
            browser.find_element_by_link_text("无限制").click()
            browser.find_element_by_link_text("助威").click()
            browser.find_element_by_link_text("确定").click()
        elif weekday == 6:
            browser.find_element_by_link_text("助威").click()
            browser.find_element_by_link_text("领奖").click()
            # 条件：达到50活跃
            browser.find_element_by_link_text("返回大乐斗首页").click()
            if int(re.search(r'今日活跃度</a>:(\d+)', browser.page_source).group(1)) >= 50:
                browser.find_element_by_link_text("结拜").click()
                browser.find_element_by_link_text("领斗币").click()
                grade_list = ['无限制', '91~110级', '71~90级', '51~70级', '30~50级']
                for i in grade_list:
                    try:
                        browser.find_element_by_link_text(i).click()
                    except:
                        pass
                    else:
                        browser.find_element_by_link_text("领斗币").click()
                        for j in range(len(browser.find_elements_by_link_text("领斗币"))):
                            browser.find_elements_by_link_text("领斗币")[j].click()
                            if re.search(r'你已经领取过本届斗币福利！', browser.page_source) is not None:
                                break
                    if re.search(r'你已经领取过本届斗币福利！', browser.page_source) is not None:
                        log.log('你已经领取过本届斗币福利！')
                        break
            else:
                log.log('活跃度不足50，请达到后手动领取斗币')
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 乐斗侠侣（度数不够怎么打）
    # browser.find_element_by_link_text("侠侣").click()
    # browser.find_element_by_link_text("夫妻").click()
    # if int(re.search(r'亲密度：(\d+)', browser.page_source).group(1)) >= 1000:
    #     browser.find_elements_by_link_text("乐斗")[0].click()

    # 乐斗其他好友
    # log.log('乐斗**********')
    # browser.find_element_by_link_text("好友").click()
    # tili_pattern = r'当前体力值：(\d+)/100'
    # tili_cpl = re.compile(tili_pattern)
    # print('当前体力值：', int(re.search(tili_cpl, browser.page_source).group(1)))
    # # 帮派boss
    # browser.find_element_by_link_text("帮友").click()
    # xia_pattern = r'侠：.*?(已乐斗|乐斗)</a>'
    # xia = re.findall(xia_pattern, browser.page_source)
    # log.log('帮派boss', xia)
    # count = -1
    # have_attack = 0
    # for i in xia:
    #     count += 1
    #     if i == '已乐斗':
    #         have_attack += 1
    #     else:
    #         index = count - have_attack
    #         ledou(100, browser, False, pos_ledou("帮派", 1, index))
    #         have_attack += 1
    # log.log('帮派boss已乐斗')
    # # 好友boss
    # browser.find_element_by_link_text("好友").click()
    # browser.find_element_by_name('jump').send_keys('1')
    # browser.find_element_by_xpath("//form/input[@value='跳到该页']").click()
    # xia_pattern = r'侠：.*?(已乐斗|乐斗)</a>'
    # xia = re.findall(xia_pattern, browser.page_source)
    # log.log('好友boss', xia)
    # count = -1
    # have_attack = 0
    # for i in xia:
    #     count += 1
    #     if i == '已乐斗':
    #         have_attack += 1
    #     else:
    #         index = count - have_attack
    #         ledou(int(re.search(tili_cpl, browser.page_source).group(1)) - 30, browser, False, pos_ledou("好友", 1, index))
    #         have_attack += 1
    # log.log('好友boss已乐斗')
    # # 定位神拳玩家
    # shenquan = r'\d+：.*?(已乐斗|乐斗)</a>.*?</a>(神拳)?<br />'
    # shenquan_cpl = re.compile(shenquan)
    # page = 1
    # max_page = r'第\d+/(\d+)页'
    # max_page = int(re.search(max_page, browser.page_source).group(1))
    # while page <= max_page:
    #     print('page:', page)
    #     print('乐斗&神拳：', shenquan_cpl.findall(browser.page_source))
    #     have_attack = 0
    #     index = -1
    #     for i in shenquan_cpl.finditer(browser.page_source):
    #         if i.group(1) == '乐斗':
    #             index += 1
    #         if i.group(2) == '神拳' and i.group(1) == '乐斗':
    #             ledou(int(re.search(tili_cpl, browser.page_source).group(1)) - 30, browser, False, pos_ledou("好友", page, index-have_attack))
    #             have_attack += 1
    #     if int(re.search(tili_cpl, browser.page_source).group(1)) - 30 < 10:
    #         break
    #     if page != max_page:
    #         browser.find_element_by_link_text("下页").click()
    #     page += 1
    #
    # # 再去找帮友把剩下的体力用完
    # browser.find_element_by_link_text("帮友").click()
    # browser.find_element_by_link_text("下页").click()
    # sqby = r'级.*?(已乐斗|乐斗)</a>(神拳)?<br />'
    # sqby = re.compile(sqby)
    # page = 2
    # max_page = r'第\d+/(\d+)页'
    # max_page = int(re.search(max_page, browser.page_source).group(1))
    # while page <= max_page:
    #     have_attack = 0
    #     index = -1
    #     for i in sqby.finditer(browser.page_source):
    #         if i.group(1) == '乐斗':
    #             index += 1
    #         if i.group(2) == '神拳' and i.group(1) == '乐斗':
    #             ledou(int(re.search(tili_cpl, browser.page_source).group(1)) - 30, browser, False, pos_ledou("帮友", page, index-have_attack))
    #             have_attack += 1
    #     if int(re.search(tili_cpl, browser.page_source).group(1)) - 30 < 10:
    #         break
    #     if page != max_page:
    #         browser.find_element_by_link_text("下页").click()
    #     page += 1
    # browser.find_element_by_link_text("返回大乐斗首页").click()
    #
    # # 许愿
    # log.log('许愿**********')
    # browser.find_element_by_link_text("许愿").click()
    # try:
    #     browser.find_element_by_link_text("领取许愿奖励").click()
    # except:
    #     log.log('已领取许愿奖励')
    # try:
    #     browser.find_element_by_link_text("许愿").click()
    #     a = random.random()
    #     if (a < 0.25):
    #         browser.find_element_by_link_text("向菜菜上香许愿").click()
    #     elif (a >= 0.25 and a < 0.5):
    #         browser.find_element_by_link_text("向剑君上香许愿").click()
    #     elif (a >= 0.5 and a < 0.75):
    #         browser.find_element_by_link_text("向月敏上香许愿").click()
    #     else:
    #         browser.find_element_by_link_text("向小王子上香许愿").click()
    # except:
    #     log.log('已许愿or没拿首胜')
    # browser.find_element_by_link_text("领取").click()
    # browser.find_element_by_link_text("返回大乐斗首页").click()

    # 分享
    log.log('分享**********')
    browser.find_element_by_link_text("分享").click()
    browser.find_element_by_link_text("一键分享").click()
    browser.find_element_by_link_text("返回大乐斗首页").click()
    browser.find_element_by_link_text("退出").click()

    log.log(log.LOG_END)
browser.quit()
f_account.close()