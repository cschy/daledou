# -*- coding: utf-8 -*-
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from datetime import datetime
import re
import random

def get_track(distance):
    """
    根据偏移量获取移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 0
    while current < distance:
        if current < mid:
            # 加速度为正2
            a = 2
        else:
            # 加速度为负3
            a = -1
        # 初速度v0
        v0 = v
        # 当前速度v = v0 + at
        v = v0 + a * t
        # 移动距离x = v0t + 1/2 * a * t^2
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track

browser = webdriver.Chrome()
browser.get('http://dld.qzapp.z.qq.com')
pre_title = browser.title
browser.maximize_window()
browser.find_element_by_id('u').send_keys('账号')
browser.find_element_by_id('p').send_keys('密码')
login = browser.find_element_by_id('go')
login.click()
time.sleep(1.5) #2s不响应
cur_title = browser.title
while(cur_title == pre_title):
    try:
        login.click()
        time.sleep(1.5) #2s不响应
        cur_title = browser.title
    except:
        login.click()
        time.sleep(1.5)  # 2s不响应
        cur_title = browser.title

# 该死的验证码
if cur_title == pre_title:
    browser.switch_to.frame("tcaptcha_iframe")  # 切换到iframe
    drag = browser.find_element_by_id("tcaptcha_drag_thumb")
    # track = get_track(185)
    # print(track)
    offset = 95
    while(True):
        print(offset)
        try:
            pre_src = browser.find_element_by_id('slideBg').get_property('src')
            #print('presrc: ', pre_src)
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
            #print('cursrc: ', cur_src)
            if cur_src != pre_src:#换图了偏移也重置
                offset = 95
            else:
                offset = offset + 2


class yaoshui_tili():
    def __init__(self, page, index, num):
        self.page = page
        self.index = index
        self.num = num
    def print_info(self):
        print('page: {}, index: {}, num: {}'.format(self.page, self.index, self.num))

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

    #跳转到达
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
            yaoshui_use(browser) #去背包用药了不在乐斗界面了
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
    #return state

# 时间
weekday = datetime.now().isoweekday()
hour = datetime.now().hour
minute = datetime.now().minute
print('星期{} {}:{}'.format(weekday, hour, minute))

# 侠士客栈
print('侠士客栈**********')
browser.find_element_by_link_text("侠士客栈").click()
try:
    browser.find_element_by_link_text("领取奖励").click()
    print(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
    browser.find_element_by_link_text("领取奖励").click()
    print(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
    browser.find_element_by_link_text("领取奖励").click()
    print(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
except:
    print('客栈奖励已领取')
browser.find_element_by_link_text("返回大乐斗首页").click()


# 会武
# 1-3试炼 4助威丐帮
print('六门会武**********')
browser.find_element_by_link_text("会武").click()#下周一研究
if weekday >= 1 and weekday <= 3:
    pass
    #browser.find_element_by_link_text("挑战").click()
elif weekday == 4:
    browser.find_element_by_link_text("冠军助威").click()
elif weekday == 5:
    print('六门会武进行中，请周末来领取奖励')
else:
    browser.find_element_by_link_text("领奖").click()
    try:
        browser.find_element_by_link_text("领取").click()
    except:
        print(re.search(r'(贵门派.*?)<br />', browser.page_source).group(1))
        print(re.search(r'(你助威的门派.*?)<br />', browser.page_source).group(1))
browser.find_element_by_link_text("返回大乐斗首页").click()
# try:
#     browser.find_elements_by_link_text("挑战")[-1].click()#怎么做确保不用试炼书
#     while True:
#         try:
#             browser.find_element_by_link_text("挑战").click()
#         except:
#             break
# except:
#     print('不是星期一到星期三')

# 门派
print('门派**********')
browser.find_element_by_link_text("乐斗").click()
browser.find_element_by_link_text("侠侣").click()
# 先尝试查看资料和乐斗门派(徒弟)
for i in re.finditer(r'徒.*?>(.*?)</a>', browser.page_source):
    browser.find_element_by_link_text(i.group(1)).click()
    try:
        browser.find_element_by_link_text("和Ta乐斗").click()
        browser.find_element_by_link_text("侠侣").click()
    except:
        browser.back()
browser.find_element_by_link_text("返回大乐斗首页").click()
browser.find_element_by_link_text("门派").click()
browser.find_element_by_link_text("万年寺").click()
try:
    browser.find_element_by_link_text("点燃").click()
    print(re.search(r'(您.*?)<br />', browser.page_source).group(1))
    browser.find_element_by_link_text("点燃").click()
    print(re.search(r'(您.*?)<br />', browser.page_source).group(1))
except:
    print('香炉全已点燃')
browser.find_element_by_link_text("返回门派首页").click()
browser.find_element_by_link_text("八叶堂").click()
browser.find_element_by_link_text("进入木桩训练").click()
browser.find_element_by_link_text("进入同门切磋").click()
browser.find_element_by_link_text("返回门派首页").click()
browser.find_element_by_link_text("金顶").click()
for i in range(len(browser.find_elements_by_link_text("切磋"))):
    browser.find_elements_by_link_text("切磋")[i].click()
browser.find_element_by_link_text("返回门派首页").click()
browser.find_element_by_link_text("五花堂").click()
while True:
    try:
        browser.find_element_by_link_text("完成").click()
        print(re.search(r'(恭喜您.*?)<br />', browser.page_source).group(1))
    except:
        break
# 打印未完成任务委派：查看一名同门成员的资料&nbsp;&nbsp;奖励：门贡20<br />
unfinished = r'委派：([\u4e00-\u9fa5]+).*?奖励：门贡\d+.*?([\u4e00-\u9fa5]+)'
for i in re.finditer(unfinished, browser.page_source):
    if i.group(2) != '已完成':
        print('未完成任务：', i.group(1))
browser.find_element_by_link_text("返回门派首页").click()
browser.find_element_by_link_text("八叶堂").click()
browser.find_element_by_link_text("进入门派邀请赛").click()
# 门派邀请赛
print('门派邀请赛**********')
if weekday == 1 or weekday == 2:
    ###
    print("已报名")
else:
    while int(re.search(r'剩余挑战次数：(\d+)', browser.page_source).group(1)) > 0:
        browser.find_element_by_link_text("开始挑战").click()
    print('10次已打满')
browser.find_element_by_link_text("返回大乐斗首页").click()

# 武林盟主
# 报名时间：1、3、5 12:00-23:55
# 竞猜时间：2、4、6 12:00-20:55
print('武林盟主**********')
browser.find_element_by_link_text("武林盟主").click()
if weekday % 2 != 0 and weekday != 7:
    if hour >= 12:
        try:
            browser.find_elements_by_link_text("参与报名")[2].click()
        except:
            print('已报名青铜赛场')
elif weekday % 2 == 0:
    if hour >= 12:
        try:
            browser.find_elements_by_link_text("参与报名")[2].click()#jingcai
        except:
            print('已竞猜')
# browser.find_element_by_link_text("领取奖励").click()
# try:
#
# except:
#     print('已报名武林盟主')
browser.find_element_by_link_text("返回大乐斗首页").click()

# 全民乱斗
# 每周一更新竞技
print('全民乱斗**********')
# 任务可能出现：
# 挑战竞技场并获得三次胜利(0/3)
# 战胜4个好友或帮友,级差<=10(0/4)
# 报名武林大会(0/1)
# 成功拦截他人镖车一次(0/1)
# 抢占他人地盘三次(0/3)
# 挑战竞技场并获得两次胜利(0/2)

# # 任务派遣中心 *****
# print('任务派遣中心**********')
# browser.find_element_by_link_text("任务派遣中心").click()
# cur_task = r'[\u4e00-\u9fa5]+-([A-Z]).*?剩余时间：(\d+)时(\d+)分'
# cur_task = re.compile(cur_task)
# print('cur_task', cur_task.findall(browser.page_source))
# # print(re.findall(r'.*', browser.page_source))
# index = -1
# received = 0
# for i in cur_task.finditer(browser.page_source):
#     index += 1
#     if int(i.group(2)) == 0 and int(i.group(3)) == 0:
#         browser.find_elements_by_link_text("查看")[index-received].click()
#         browser.find_element_by_link_text("领取奖励").click()
#         received += 1
#
# task = r'[\u4e00-\u9fa5]+-([A-Z]).*?所需时间：\d+小时.*?>接受</a>'
# task = re.compile(task)
# print('task', task.findall(browser.page_source))
# grade = ['B', 'A', 'S']
# count = 0
# brush = True
# brush_count = 0
# while count < len(task.findall(browser.page_source)):
#     index = -1
#     exist = False
#     result = task.findall(browser.page_source)
#     for i in result:
#         index += 1
#         if i == grade[-1]:
#             exist = True
#             browser.find_elements_by_link_text("接受")[index].click()
#             browser.find_element_by_link_text("快速委派").click()
#             try:
#                 browser.find_element_by_link_text("开始任务").click()
#                 result = task.findall(browser.page_source)
#                 brush = False
#                 index = 0
#             except:
#                 print("佣兵不足")
#                 # 查看上面有没有此等级的任务正在做，若有则可以等待上面完成而不用刷新
#                 for j in cur_task.findall(browser.page_source):
#                     if i == j[0] and brush is True:
#                         brush = False
#                 browser.find_element_by_link_text("返回大乐斗首页").click()
#                 browser.find_element_by_link_text("任务派遣中心").click()
#     count += 1
#     grade.pop()
# print('刷新：', brush)
# #if brush is True:# 最多刷新3次
# browser.find_element_by_link_text("返回大乐斗首页").click()


# 帮派黄金联赛
print('帮派黄金联赛**********')
browser.find_element_by_link_text("帮派黄金联赛").click()

try:
    browser.find_element_by_link_text("领取帮派赛季奖励").click()
except:
    print('没有奖励可领')
try:
    browser.find_element_by_link_text("领取奖励").click()
    print(re.search(r'(恭喜您.*?)<br />', browser.page_source).group(1))
except:
    print('没有奖励可领')
try:
    browser.find_element_by_link_text("参与防守").click()
except:
    print('已参与防守')
browser.find_element_by_link_text("返回大乐斗首页").click()

# 帮派远征军
print('帮派远征军**********')
browser.find_element_by_link_text("帮派远征军").click()
try:
    browser.find_element_by_link_text("领取奖励").click()
except:
    print('没有节点奖励可领')
browser.find_element_by_link_text("参战").click()
browser.find_element_by_link_text("攻击").click()
browser.find_element_by_link_text("返回大乐斗首页").click()

# 问鼎天下
# 争夺时间：1.6-6.6
# 助威时间：6、6:00-19:30
print('问鼎天下**********')
browser.find_element_by_link_text("问鼎天下").click()
if weekday >= 1 and weekday <= 5:
    browser.find_element_by_link_text("资源点争夺").click()
    browser.find_element_by_link_text("领取奖励").click()
    argue_times = r'剩余抢占次数：(\d+)'
    print('剩余抢占次数：', re.search(argue_times, browser.page_source).group(1))
    while int(re.search(argue_times, browser.page_source).group(1)) > 2:
        browser.find_element_by_link_text("攻占").click()
        print('剩余抢占次数：', re.search(argue_times, browser.page_source).group(1))
if weekday == 6:
    area_list = ['北寒', '南荒', '东海', '西泽']
    shenge_exist = False
    for i in area_list:
        browser.find_element_by_link_text(i).click()
        try:
            browser.find_element_by_link_text("神ㄨ阁丶").click()
            shenge_exist = True
            break
        except:
            continue
    if shenge_exist is False:
        print('神阁帮不在区域赛16强，请重新助威')
browser.find_element_by_link_text("返回大乐斗首页").click()

# 梦想之旅
#  第四周周5用梦幻机票，5/6/7/8同理，八周一循环
print('梦想之旅**********')
browser.find_element_by_link_text("梦想之旅").click()
browser.find_element_by_link_text("普通旅行").click()
print(re.search(r'规则</a><br />(.*?)<br />', browser.page_source).group(1))
if int(re.search(r'梦幻机票：(\d+)', browser.page_source).group(1)) != 0:
    count = -1
    for i in re.finditer(r'[\u4e00-\u9fa5]+\s(已去过|未去过)', browser.page_source):
        count += 1
        if i.group(1) == '未去过':
            browser.find_element_by_link_text("梦幻旅行").click()
            browser.find_elements_by_link_text("去这里")[count].click()
            break
browser.find_element_by_link_text("返回大乐斗首页").click()


# 画卷迷踪
print('画卷迷踪**********')
pro_list = [1,1,2,3,3]
browser.find_element_by_link_text("画卷迷踪").click()
if int(re.search(r'本日免费剩余次数：(\d+)', browser.page_source).group(1)) > 0:
    while True:
        try:
            browser.find_elements_by_link_text("选择")[pro_list[-1]].click()
        except:
            print('不用buff加成了')
        browser.find_element_by_link_text("准备完成进入战斗").click()
        if len(pro_list) != 0:
            pro_list.pop()
        if len(re.findall('弱爆了', browser.page_source)) != 0:
            break
browser.find_element_by_link_text("返回大乐斗首页").click()

# 群雄逐鹿 周六报名 周一到周三14:00比赛，在此之前领奖励

# 幻境（现阶段吃药试试）
print('幻境(吃药)**********')
# browser.find_element_by_link_text("幻境").click()
# browser.find_element_by_link_text("返回飘渺幻境").click()
# browser.find_element_by_link_text("乐斗村").click()
# browser.find_element_by_link_text("乐斗").click()
# browser.find_element_by_link_text("返回大乐斗首页").click()

# 勋章馆

# 镖行天下
print('镖行天下**********')
browser.find_element_by_link_text("镖行天下").click()
try:
    browser.find_element_by_link_text("护送完成").click()
    browser.find_element_by_link_text("领取奖励").click()
except:
    pass
if int(re.search(r'剩余护送次数：(\d+)', browser.page_source).group(1)) > 0:
    browser.find_element_by_link_text("护送押镖").click()
    browser.find_element_by_link_text("刷新押镖").click()
    browser.find_element_by_link_text("启程护送").click()
    browser.find_element_by_link_text("刷新").click()
pattern = r'剩余拦截次数：(\d)'
regex = re.compile(pattern, re.I | re.S)
while(True):
    for i in range(len(browser.find_elements_by_link_text("拦截"))):
        if int(regex.search(browser.page_source).group(1)) == 0:
            break
        browser.find_elements_by_link_text("拦截")[i].click()
    if int(regex.search(browser.page_source).group(1)) > 0:
        browser.find_element_by_link_text("刷新").click()
    else:
        break
browser.find_element_by_link_text("返回大乐斗首页").click()


# 历练
print('历练**********')
browser.find_element_by_link_text("历练").click()
browser.find_element_by_link_text("摩云山").click()
browser.find_element_by_link_text("下一页").click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_element_by_link_text("返回世界场景").click()

browser.find_element_by_link_text("苍莽山").click()
browser.find_element_by_link_text("下一页").click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_element_by_link_text("返回世界场景").click()

browser.find_element_by_link_text("玉龙湿地").click()
browser.find_element_by_link_text("下一页").click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_elements_by_link_text("乐斗")[9].click()
browser.find_element_by_link_text("返回大乐斗首页").click()


# 斗神塔
print('斗神塔**********')
browser.find_element_by_link_text("斗神塔").click()
if int(re.search(r'今日剩余次数：(\d+)', browser.page_source).group(1)) != 0:
    browser.find_element_by_link_text("结束挑战").click()
    browser.find_element_by_link_text("取消").click()
    browser.find_element_by_link_text("自动挑战").click()
else:
    print('今日已挑战')
browser.find_element_by_link_text("返回大乐斗首页").click()

# 抢地盘
print('抢地盘**********')
browser.find_element_by_link_text("抢地盘").click()
browser.find_element_by_link_text("抢地盘记录").click()
if re.search(r'今天', browser.page_source) is None:
    browser.find_element_by_link_text("返回抢地盘").click()
    browser.find_elements_by_link_text("使用")[0].click()
    browser.find_elements_by_link_text("使用")[1].click()
    browser.find_elements_by_link_text("使用")[2].click()
    browser.find_element_by_link_text("70级以下").click()
    pattern = r'守(\d+)次'
    regex = re.compile(pattern)
    no5 = True
    while(no5):
        count = -1
        browser.find_element_by_link_text("刷新地盘").click()
        for i in regex.finditer(browser.page_source):
            count += 1
            if int(i.group(1)) == 0:
                browser.find_elements_by_link_text("攻占")[count].click()
                no5 = False
                break
    print(re.search(r'你主动与.*?。', browser.page_source).group())
else:
    print('今日已抢')
browser.find_element_by_link_text("返回大乐斗首页").click()


# 重出江湖
print('重出江湖**********')
browser.find_element_by_link_text("重出江湖").click()
browser.find_elements_by_link_text("回来玩吧！")[0].click()
browser.find_elements_by_link_text("回来玩吧！")[1].click()
browser.find_elements_by_link_text("回来玩吧！")[2].click()
browser.find_element_by_link_text("返回大乐斗首页").click()

# 十二宫
print('十二宫**********')
browser.find_element_by_link_text("十二宫").click()
xinggong = re.findall(r'([\u4e00-\u9fa5]+宫).*?扫荡', browser.page_source)[-1]
browser.find_element_by_link_text(xinggong).click()
if len(re.findall(r'你不幸被怪物干掉了', browser.page_source)) == 0:
    count = 0
    while True:
        if len(re.findall(r'你不幸被怪物干掉了', browser.page_source)) == 0:
            try:
                browser.find_element_by_link_text("挑战").click()
                print(re.findall(r'(获得了.*?)<br />', browser.page_source))
            except:
                print('挑战次数不足！')
                break
        else:
            count += 1
            if count <= 1:
                print('你不幸被怪物干掉了')
                print('开始复活...')
                browser.find_element_by_link_text("复活").click()
                browser.find_elements_by_link_text("选择")[2].click()
                browser.find_element_by_link_text("确认复活").click()
            else:
                print('你不幸又被怪物干掉了')
                break
else:
    print('今日已挑战')
browser.find_element_by_link_text("返回大乐斗首页").click()

# 竞技场
print('竞技场**********')
browser.find_element_by_link_text("竞技场").click()
try:
    browser.find_element_by_link_text("开始挑战").click()
except:
    print('赛季已结束')
browser.find_element_by_link_text("返回大乐斗首页").click()

# 踢馆
print('踢馆**********')
browser.find_element_by_link_text("踢馆").click()
if weekday == 5:
    for i in range(5):
        browser.find_element_by_link_text("试练").click()
    browser.find_element_by_link_text("高倍转盘").click()
    for i in range(3):
        browser.find_element_by_link_text("挑战").click() #挑战>=3次
browser.find_element_by_link_text("领奖").click() #22后
browser.find_element_by_link_text("返回大乐斗首页").click()

# 掠夺
print('掠夺**********')
browser.find_element_by_link_text("掠夺").click()
if weekday == 2:
    browser.find_element_by_link_text("掠夺").click()
    ###
elif weekday == 3:
    browser.find_element_by_link_text("领取奖励").click()
    browser.find_element_by_link_text("部署").click()
    browser.find_element_by_link_text("加入").click()
else:
    print('星期二和星期三再来')
browser.find_element_by_link_text("返回大乐斗首页").click()

# 矿洞
print('矿洞**********')
browser.find_element_by_link_text("矿洞").click()
try:
    browser.find_element_by_link_text("领取奖励").click()
except:
    pass
for i in range(3):
    browser.find_element_by_link_text("挑战").click()
    print(re.findall(r'你挑战.*?。', browser.page_source))
browser.find_element_by_link_text("返回大乐斗首页").click()

# 邪神秘宝
print('邪神秘宝**********')
browser.find_element_by_link_text("邪神秘宝").click()
mibao = re.findall(r'(\d+)时(\d+)分(\d+)秒后免费', browser.page_source)
print('高级秘宝：' + mibao[0][0] + '时' + mibao[0][1] + '分' + mibao[0][2] + '秒后免费')
print('极品秘宝：' + mibao[1][0] + '时' + mibao[1][1] + '分' + mibao[1][2] + '秒后免费')
if mibao[0][0] == 0 and mibao[0][1] == 0 and mibao[0][2] == 0:
    browser.find_elements_by_link_text("抽奖一次")[0].click()
if mibao[1][0] == 0 and mibao[1][1] == 0 and mibao[1][2] == 0:
    browser.find_elements_by_link_text("抽奖一次")[1].click()
# 打印得到奖品
browser.find_element_by_link_text("返回大乐斗首页").click()

# 徒弟经验及每日奖励
try:
    browser.find_element_by_link_text("领取徒弟经验").click()
except:
    pass
browser.find_element_by_link_text("每日奖励").click()
try:
    browser.find_element_by_link_text("领取").click()
    browser.find_element_by_link_text("领取").click()
except:
    pass
browser.find_element_by_link_text("返回大乐斗首页").click()


# 乐斗
print('乐斗**********')
browser.find_element_by_link_text("好友").click()
tili_pattern = r'当前体力值：(\d+)/100'
tili_cpl = re.compile(tili_pattern)
print('当前体力值：', int(re.search(tili_cpl, browser.page_source).group(1)))
# # 侠侣
# browser.find_element_by_link_text("侠侣").click()
# while(True):
#     try:
#         ledou(int(re.search(tili_cpl, browser.page_source).group(1)), browser, True, pos_ledou("侠侣", 0, 0))
#     except:
#         print('侠侣已乐斗')
#         break
# 帮派boss
browser.find_element_by_link_text("帮友").click()
xia_pattern = r'侠：.*?(已乐斗|乐斗)</a>'
xia = re.findall(xia_pattern, browser.page_source)
print('帮派boss', xia)
count = -1
have_attack = 0
for i in xia:
    count += 1
    if i == '已乐斗':
        have_attack += 1
    else:
        index = count - have_attack
        ledou(int(re.search(tili_cpl, browser.page_source).group(1)), browser, True, pos_ledou("帮派", 1, index))
        have_attack += 1
print('帮派boss已乐斗')
# 好友boss
browser.find_element_by_link_text("好友").click()
browser.find_element_by_link_text("上页").click()
xia_pattern = r'侠：.*?(已乐斗|乐斗)</a>'
xia = re.findall(xia_pattern, browser.page_source)
print('好友boss', xia)
count = -1
have_attack = 0
for i in xia:
    count += 1
    if i == '已乐斗':
        have_attack += 1
    else:
        index = count - have_attack
        ledou(int(re.search(tili_cpl, browser.page_source).group(1)), browser, True, pos_ledou("好友", 1, index))
        have_attack += 1
print('好友boss已乐斗')
# 定位神拳玩家
shenquan = r'\d+：.*?(已乐斗|乐斗)</a>.*?</a>(神拳)?<br />'
shenquan_cpl = re.compile(shenquan)
page = 1
max_page = r'第\d+/(\d+)页'
max_page = int(re.search(max_page, browser.page_source).group(1))
while page <= max_page:
    print('page:', page)
    print('乐斗&神拳：', shenquan_cpl.findall(browser.page_source))
    have_attack = 0
    index = -1
    for i in shenquan_cpl.finditer(browser.page_source):
        if i.group(1) == '乐斗':
            index += 1
        if i.group(2) == '神拳' and i.group(1) == '乐斗':
            ledou(int(re.search(tili_cpl, browser.page_source).group(1)), browser, False, pos_ledou("好友", page, index-have_attack))
            have_attack += 1
    if int(re.search(tili_cpl, browser.page_source).group(1)) < 10:
        break
    if page != max_page:
        browser.find_element_by_link_text("下页").click()
    page += 1

# 再去找帮友把剩下的体力用完
browser.find_element_by_link_text("帮友").click()
browser.find_element_by_link_text("下页").click()
sqby = r'级.*?(已乐斗|乐斗)</a>(神拳)?<br />'
sqby = re.compile(sqby)
page = 2
max_page = r'第\d+/(\d+)页'
max_page = int(re.search(max_page, browser.page_source).group(1))
while page <= max_page:
    have_attack = 0
    index = -1
    for i in sqby.finditer(browser.page_source):
        if i.group(1) == '乐斗':
            index += 1
        if i.group(2) == '神拳' and i.group(1) == '乐斗':
            ledou(int(re.search(tili_cpl, browser.page_source).group(1)), browser, False, pos_ledou("帮友", page, index-have_attack))
            have_attack += 1
    if int(re.search(tili_cpl, browser.page_source).group(1)) < 10:
        break
    if page != max_page:
        browser.find_element_by_link_text("下页").click()
    page += 1
browser.find_element_by_link_text("返回大乐斗首页").click()

# 许愿
browser.find_element_by_link_text("许愿").click()
try:
    browser.find_element_by_link_text("领取许愿奖励").click()
except:
    print('已领取许愿奖励')
try:
    browser.find_element_by_link_text("许愿").click()
    a = random.random()
    if (a < 0.25):
        browser.find_element_by_link_text("向菜菜上香许愿").click()
    elif (a >= 0.25 and a < 0.5):
        browser.find_element_by_link_text("向剑君上香许愿").click()
    elif (a >= 0.5 and a < 0.75):
        browser.find_element_by_link_text("向月敏上香许愿").click()
    else:
        browser.find_element_by_link_text("向小王子上香许愿").click()
except:
    print('已许愿')
browser.find_element_by_link_text("领取").click()
browser.find_element_by_link_text("返回大乐斗首页").click()


# 经脉

# 武林
# 侠侣
# 结拜
# 帮战
# 帮修
# 帮贡

# 任务
browser.find_element_by_link_text("任务").click()
browser.find_element_by_link_text("一键完成任务").click()
browser.find_element_by_link_text("返回大乐斗首页").click()

# 分享
browser.find_element_by_link_text("分享").click()
browser.find_element_by_link_text("一键分享").click()
browser.find_element_by_link_text("返回大乐斗首页").click()

## 帮派祭坛 应该放在任务完成后
# browser.find_element_by_link_text("帮派祭坛").click()
# if weekday == 1:
#     browser.find_element_by_link_text("领取奖励").click()
# while int(re.search(r'剩余次数：(\d+)', browser.page_source).group(1)) > 0:
#     browser.find_element_by_link_text("转动轮盘").click()
#     try:
#         browser.find_elements_by_link_text("选择")[1].click()
# browser.find_element_by_link_text("返回大乐斗首页").click()

# 帮派商会 放在后面好一点
print('帮派商会**********')
browser.find_element_by_link_text("帮派商会").click()
while True:
    try:
        browser.find_element_by_link_text("点击领取").click()
    except:
        break
browser.find_element_by_link_text("返回大乐斗首页").click()


# 帮贡
print('帮贡**********')
browser.find_element_by_link_text("我的帮派").click()
browser.find_element_by_link_text("领取").click()
if int(re.search(r'12.\[(\d)/1\]', browser.page_source).group(1)) == 0:
    browser.back()
    browser.find_element_by_link_text("帮派守护神").click()
    browser.find_element_by_link_text("供奉守护神").click()
    page = r'第(\d+)/(\d+)页'
    while int(re.search(page, browser.page_source).group(1)) <= int(re.search(page, browser.page_source).group(2)):
        dan = r'([\u4e00-\u9fa5]+)\s数量：\d+.*?供奉'
        count = -1
        #小活力药水 数量：94<a href="//dld.qzapp.z.qq.com/qpet/cgi-bin/phonepk?zapp_uin=&amp;sid=&amp;channel=0&amp;g_ut=1&amp;cmd=oblation&amp;id=3386&amp;page=1">供奉
        for i in re.finditer(dan, browser.page_source):
            count += 1
            if i.group(1) == '还魂丹':
                browser.find_elements_by_link_text("供奉")[count].click()
                break
        try:
            browser.find_element_by_link_text("下页").click()
        except:
            print('没有还魂丹了')
            print('手动供奉')
            break
else:
    print('已供奉')


# 结拜


# browser.quit()
