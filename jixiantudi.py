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


browser = webdriver.Chrome()
browser.get('https://ui.ptlogin2.qq.com/cgi-bin/login?appid=614038002&style=9&s_url=https%3A%2F%2Fdld.qzapp.z.qq.com%2Fqpet%2Fcgi-bin%2Fphonepk%3Fcmd%3Dindex%26channel%3D0')
pre_title = browser.title
# browser.maximize_window()
acc_num = 0
f_account = open("account.txt")
for line in f_account:
    print('账号：', line.split('----')[0])
    account_ = browser.find_element_by_id('u')
    account_.clear()
    account_.send_keys(line.split('----')[0])
    browser.find_element_by_id('p').send_keys(line.split('----')[1].rstrip())
    login = browser.find_element_by_id('go')
    acc_error = False
    ip_busy = False

    login.click()
    time.sleep(1.5)  # 根据自身设备和网速而定
    cur_title = browser.title

    # 验证码||qq异常||ip频繁
    if cur_title == pre_title:
        if re.search(r'你输入的帐号或密码不正确，请重新输入。', browser.page_source) is not None:
            print('码前帐号或密码不正确')
            acc_error = True
        elif re.search(r'对不起，你的号码登录异常', browser.page_source) is not None or re.search(r'你的帐号暂时无法登录', browser.page_source) is not None:
            print('码前账号被冻结')
            acc_error = True
        elif re.search(r'当前上网环境异常，请更换网络环境或在常用设备上登录或稍后再试。', browser.page_source) is not None:
            print('码前ip频繁')
            ip_busy = True
        else:
            browser.switch_to.frame("tcaptcha_iframe")  # 切换到iframe
            time.sleep(0.5)
            drag = browser.find_element_by_id("tcaptcha_drag_thumb")
            offset = 50
            while True:
                print('滑块偏移量：', offset*4)
                try:
                    pre_src = browser.find_element_by_id('slideBg').get_property('src')
                    # print('原图片链接: ', pre_src)
                    action = ActionChains(browser)
                    action.click_and_hold(drag).perform()
                    for i in range(offset):
                        action.move_by_offset(xoffset=4, yoffset=0).perform()
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
                        offset = 50
                    else:
                        offset = offset + 4
            time.sleep(1)
            cur_title = browser.title
            if cur_title == pre_title:
                if re.search(r'你输入的帐号或密码不正确，请重新输入。', browser.page_source) is not None:
                    print('码后帐号或密码不正确')
                    acc_error = True
                elif re.search(r'对不起，你的号码登录异常', browser.page_source) is not None or re.search(r'你的帐号暂时无法登录',                                                                         browser.page_source) is not None:
                    print('码后账号被冻结')
                    acc_error = True
                elif re.search(r'当前上网环境异常，请更换网络环境或在常用设备上登录或稍后再试。', browser.page_source) is not None:
                    print('码后ip频繁')
                    ip_busy = True
    if acc_error is True:
        browser.quit()
        browser = webdriver.Chrome()
        browser.get('https://ui.ptlogin2.qq.com/cgi-bin/login?appid=614038002&style=9&s_url=https%3A%2F%2Fdld.qzapp.z.qq.com%2Fqpet%2Fcgi-bin%2Fphonepk%3Fcmd%3Dindex%26channel%3D0')
        continue
    elif ip_busy is True:
        browser.delete_all_cookies()
        time.sleep(60)
        browser.quit()
        browser = webdriver.Chrome()
        browser.get('https://ui.ptlogin2.qq.com/cgi-bin/login?appid=614038002&style=9&s_url=https%3A%2F%2Fdld.qzapp.z.qq.com%2Fqpet%2Fcgi-bin%2Fphonepk%3Fcmd%3Dindex%26channel%3D0')
        account_ = browser.find_element_by_id('u')
        account_.clear()
        account_.send_keys(line.split('----')[0])
        browser.find_element_by_id('p').send_keys(line.split('----')[1].rstrip())
        login = browser.find_element_by_id('go')
        login.click()
        time.sleep(1.5)  # 根据自身设备和网速而定
        cur_title = browser.title
        if cur_title == pre_title:
            if re.search(r'当前上网环境异常，请更换网络环境或在常用设备上登录或稍后再试。', browser.page_source) is not None:
                print('码前ip仍然频繁, 退出浏览器')
                browser.quit()
                sys.exit()
            else:
                browser.switch_to.frame("tcaptcha_iframe")  # 切换到iframe
                time.sleep(0.5)
                drag = browser.find_element_by_id("tcaptcha_drag_thumb")
                offset = 50
                while True:
                    print('滑块偏移量：', offset * 4)
                    try:
                        pre_src = browser.find_element_by_id('slideBg').get_property('src')
                        # print('原图片链接: ', pre_src)
                        action = ActionChains(browser)
                        action.click_and_hold(drag).perform()
                        for i in range(offset):
                            action.move_by_offset(xoffset=4, yoffset=0).perform()
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
                            offset = 50
                        else:
                            offset = offset + 4
                time.sleep(1)
                cur_title = browser.title
                if cur_title == pre_title:
                    print('码后ip仍然频繁, 退出浏览器')
                    browser.quit()
                    sys.exit()

    # data
    weekday = datetime.now().isoweekday()
    print('时间：', datetime.now().strftime('%Y-%m-%d %A %H:%M:%S'))
    level = re.search(r'等级:(\d+)', browser.page_source)
    if level is not None:
        level = int(level.group(1))
    else:
        print('获取等级失败')
    fighting_capacity = re.search(r'战斗力</a>:(\d+\.{0,1}\d{0,1})', browser.page_source)
    if fighting_capacity is not None:
        fighting_capacity = float(fighting_capacity.group(1))
    else:
        print('获取战斗力失败')


    try:
        browser.find_element_by_link_text("登录商店").click()
    except:
        pass
    else:
        jifen = re.search(r'我的兑换积分：(\d+)', browser.page_source)
        if jifen is not None:
            for i in range(int(jifen.group(1))):
                browser.find_elements_by_link_text("兑换")[1].click()
        else:
            print('获取积分信息失败')
        browser.find_element_by_link_text("返回大乐斗首页").click()


    # 分享
    browser.find_element_by_link_text("分享").click()
    browser.find_element_by_link_text("一键分享").click()
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 侠士客栈
    print('侠士客栈（35or40）**********')
    try:
        browser.find_element_by_link_text("侠士客栈").click()
    except:
        print('等级太低，暂未开放')
    else:
        try:
            browser.find_element_by_link_text("领取奖励").click()
            print(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
            browser.find_element_by_link_text("领取奖励").click()
            print(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
            browser.find_element_by_link_text("领取奖励").click()
            print(re.search(r'侠士客栈<br />(.*?)<br />', browser.page_source).group(1))
        except:
            print('已领取')
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 判断是否有帮派
    browser.find_element_by_link_text("我的帮派").click()
    if re.search(r'创建帮派', browser.page_source) is None:
        have_gang = True
    else:
        have_gang = False
        print('帮派：暂无')
        specify_gang = '1406288'
        browser.find_element_by_name('groups_id').send_keys(specify_gang)
        browser.find_element_by_xpath("//form/input[@value='申请加入']").click()
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 梦想之旅
    #  第四周周5用梦幻机票，5/6/7/8同理，八周一循环
    print('梦想之旅**********')
    browser.find_element_by_link_text("梦想之旅").click()
    browser.find_element_by_link_text("普通旅行").click()
    mxzl_reward = re.search(r'规则</a><br />(.*?)<br />', browser.page_source)
    if mxzl_reward is not None:
        print(mxzl_reward.group(1))
    else:
        print('请检查打印格式')
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 画卷迷踪 对应系统觉醒（有材料翻倍活动）
    print('画卷迷踪(30)**********')
    try:
        browser.find_element_by_link_text("画卷迷踪").click()
    except:
        print('等级太低，暂未开放')
    else:
        while int(re.search(r'本日免费剩余次数：(\d+)', browser.page_source).group(1)) > 0:
            browser.find_element_by_link_text("准备完成进入战斗").click()
            time.sleep(0.5)
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 群雄逐鹿 周六报名 周一到周三14:00比赛，在此之前领奖励 对应系统铭刻（4级祝福值会清零）
    print('群雄逐鹿(40)**********')
    try:
        browser.find_element_by_link_text("群雄逐鹿").click()
    except:
        print('等级太低，暂未开放')
    else:
        browser.find_element_by_link_text("报名").click()
        browser.find_element_by_link_text("领奖").click()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 勋章馆

    # 镖行天下 镖行天下对应系统专精（有活动）材料建议兑换大型和小型
    print('镖行天下(30)**********')
    try:
        browser.find_element_by_link_text("镖行天下").click()
    except:
        print('等级太低，暂未开放')
    else:
        try:
            browser.find_element_by_link_text("护送完成").click()
            browser.find_element_by_link_text("领取奖励").click()
        except:
            pass
        if int(re.search(r'剩余护送次数：(\d+)', browser.page_source).group(1)) > 0:
            browser.find_element_by_link_text("护送押镖").click()
            while True:
                biaoshi = re.search(r'当前镖师：(.*?)<br />', browser.page_source)
                if biaoshi is not None:
                    if biaoshi.group(1) != '温良恭':
                        try:
                            browser.find_element_by_link_text("刷新押镖").click()
                        except:
                            break
                    else:
                        break
                else:
                    print('未检测出当前镖师')
            browser.find_element_by_link_text("启程护送").click()
            browser.find_element_by_link_text("刷新").click()
        # pattern = r'剩余拦截次数：(\d)'
        # regex = re.compile(pattern, re.I | re.S)
        # while int(regex.search(browser.page_source).group(1)) > 0:
        #     index = -1
        #     for j in re.finditer(r'\d+\.(温良恭|吕青橙|蔡八斗).*?拦截', browser.page_source):
        #         index += 1
        #         if j.group(1) == '温良恭':
        #             browser.find_elements_by_link_text("拦截")[index].click()
        #             if re.search(r'空手而归', browser.page_source) is None:
        #                 print('拦截成功')
        #             else:
        #                 print('空手而归')
        #     browser.find_element_by_link_text("刷新").click()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 历练
    print('历练**********')
    browser.find_element_by_link_text("历练").click()
    browser.find_element_by_link_text("乐斗村").click()
    browser.find_element_by_link_text("下一页").click()
    while int(re.search(r'活力值：(\d+)', browser.page_source).group(1)) >= 10:
        browser.find_elements_by_link_text("乐斗")[-2].click()
    # experience_list = ['鹅王的试炼', '桃花剑冢', '藏剑山庄', '花果山', '程管小镇', '炎之洞窟', '黄沙漩涡',
    #                    '悲叹山丘', '回声遗迹', '狂沙台地', '玉龙雪山', '玉龙湿地', '苍莽山', '洞庭湖',
    #                    '摩云山', '踏云镇','东海龙宫', '林松城', '林松郊外', '乐斗村']
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 斗神塔
    print('斗神塔(12)**********')
    try:
        browser.find_element_by_link_text("斗神塔").click()
    except:
        print('等级太低，暂未开放')
    else:
        if int(re.search(r'今日剩余次数：(\d+)', browser.page_source).group(1)) != 0:
            try:
                browser.find_element_by_link_text("结束挑战").click()
                browser.find_element_by_link_text("取消").click()
            except:
                pass
            browser.find_element_by_link_text("自动挑战").click()
        else:
            print('今日已挑战')
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 抢地盘
    print('抢地盘(10)**********')
    try:
        browser.find_element_by_link_text("抢地盘").click()
    except:
        print('等级太低，暂未开放')
    else:
        browser.find_element_by_link_text("抢地盘记录").click()
        if re.search(r'今天', browser.page_source) is None:
            browser.back()
            max_refresh = 100
            find_shoujiang = False
            for i in range(max_refresh):
                index = -1
                for j in re.finditer(r'级(.*?)\(', browser.page_source.split('规则')[1]):
                    index += 1
                    if '守将' in j.group(1):
                        browser.find_elements_by_link_text("攻占")[index].click()
                        find_shoujiang = True
                        break
                if find_shoujiang is True:
                    break
        else:
            print('今日已抢')
            browser.back()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 重出江湖
    if level >= 25:
        print('重出江湖**********')
        browser.find_element_by_link_text("重出江湖").click()
        try:
            browser.find_elements_by_link_text("回来玩吧！")[0].click()
            browser.find_elements_by_link_text("回来玩吧！")[0].click()
            browser.find_elements_by_link_text("回来玩吧！")[0].click()
        except:
            print('无退斗好友')
        browser.find_element_by_link_text("返回大乐斗首页").click()
    else:
        print('等级小于25')


    # 踢馆 材料兑换凤凰羽毛
    print('踢馆**********')
    try:
        browser.find_element_by_link_text("踢馆").click()
    except:
        print('没有帮派')
    else:
        if weekday == 5:
            for i in range(5):
                browser.find_element_by_link_text("试练").click()
            browser.find_element_by_link_text("高倍转盘").click()
            # while int(re.search(r'生命：\d+', browser.page_source).group(1)) > 0:
            for i in range(3):
                browser.find_element_by_link_text("挑战").click()  # 挑战>=3次
        browser.find_element_by_link_text("领奖").click()  # 22:00后
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 邪神秘宝
    print('邪神秘宝**********')
    browser.find_element_by_link_text("邪神秘宝").click()
    mibao = re.findall(r'(\d+)时(\d+)分(\d+)秒后免费', browser.page_source)
    print('高级秘宝：' + mibao[0][0] + '时' + mibao[0][1] + '分' + mibao[0][2] + '秒后免费')
    print('极品秘宝：' + mibao[1][0] + '时' + mibao[1][1] + '分' + mibao[1][2] + '秒后免费')
    if mibao[0][0] == '0' and mibao[0][1] == '0' and mibao[0][2] == '0':
        browser.find_element_by_link_text("免费一次").click()
    if mibao[1][0] == '0' and mibao[1][1] == '0' and mibao[1][2] == '0':
        browser.find_element_by_link_text("免费一次").click()
    # 打印得到奖品
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 徒弟经验及每日奖励
    print('徒弟经验及每日奖励**********')
    try:
        browser.find_element_by_link_text("领取徒弟经验").click()
    except:
        print('已领取徒弟经验 or 没有徒弟')
    browser.find_element_by_link_text("每日奖励").click()
    while True:
        try:
            browser.find_element_by_link_text("领取").click()
        except:
            break
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 帮贡
    if have_gang is True:
        print('帮贡**********')
        browser.find_element_by_link_text("我的帮派").click()
        browser.find_element_by_link_text("领取").click()
        if int(re.search(r'12.\[(\d)/1\]', browser.page_source).group(1)) == 0:
            browser.back()
            browser.find_element_by_link_text("帮派守护神").click()
            browser.find_element_by_link_text("供奉守护神").click()
            page = r'第(\d+)/(\d+)页'
            gf = False
            cur_page = 1
            max_page = 1
            if re.search(page, browser.page_source) is not None:
                cur_page = int(re.search(page, browser.page_source).group(1))
            if re.search(page, browser.page_source) is not None:
                max_page = int( re.search(page, browser.page_source).group(2))
            while cur_page <= max_page:
                dan = r'<br />([\u4e00-\u9fa5].*?)\s数量：\d+.*?供奉'
                count = -1
                # 小活力药水 数量：94<a href="//dld.qzapp.z.qq.com/qpet/cgi-bin/phonepk?zapp_uin=&amp;sid=&amp;channel=0&amp;g_ut=1&amp;cmd=oblation&amp;id=3386&amp;page=1">供奉
                for i in re.finditer(dan, browser.page_source.split('供奉守护神')[1]):
                    # print(i.group(1))
                    count += 1
                    if i.group(1) == '还魂丹':
                        browser.find_elements_by_link_text("供奉")[count].click()
                        gf = True
                        break
                if gf is True:
                    print('供奉了一个还魂丹')
                    break
                cur_page += 1
                try:
                    browser.find_element_by_link_text("下页").click()
                except:
                    print('没有还魂丹了，手动供奉')
                    break
        else:
            print('已供奉')
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 武林
    print('武林**********')
    try:
        browser.find_element_by_link_text("武林").click()
    except:
        print('等级限制')
    else:
        if datetime.now().hour >= 13:
            try:
                browser.find_elements_by_link_text("随机报名")[-1].click()
            except:
                print('已报名')
            else:
                print('报名成功')
        browser.find_element_by_link_text("返回大乐斗首页").click()


    # 结拜赛
    print('结拜赛**********')
    try:
        browser.find_element_by_link_text("结拜").click()
    except:
        print('等级小于30, 无法领斗币')
    else:
        if weekday == 4:
            browser.find_element_by_link_text("助威").click()
            browser.find_element_by_link_text("30~50级").click()
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
                        print('你已经领取过本届斗币福利！')
                        break
            else:
                print('活跃度不足50，请达到后手动领取斗币')
        try:
            browser.find_element_by_link_text("返回大乐斗首页").click()
        except:
            pass

    # 关闭助手
    browser.find_element_by_link_text("好友").click()
    browser.find_element_by_link_text("助手").click()
    try:
        browser.find_element_by_link_text("取消自动使用体力药水").click()
    except:
        pass
    try:
        browser.find_element_by_link_text("取消自动使用主动经验药水").click()
    except:
        pass
    try:
        browser.find_element_by_link_text("开启自动使用神来拳套").click()
    except:
        pass
    try:
        browser.find_element_by_link_text("取消自动使用活力药水").click()
    except:
        pass
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 帮友乐斗
    if have_gang is True:
        browser.find_element_by_link_text("帮友").click()
        xia = re.findall(r'侠：.*?(已乐斗|乐斗)</a>', browser.page_source)
        print('帮派boss', xia)
        count = -1
        have_attack = 0
        for i in xia:
            count += 1
            if i == '已乐斗':
                have_attack += 1
            else:
                index = count - have_attack
                browser.find_elements_by_link_text("乐斗")[index].click()
                have_attack += 1

        tili = int(re.search(r'当前体力值：(\d+)/100', browser.page_source).group(1))
        print('当前体力值：', tili)
        if tili >= 10:
            if level >= 10 and level < 20:
                browser.find_elements_by_link_text("乐斗")[-2].click()
            elif level >= 20 and level < 30:
                browser.find_elements_by_link_text("乐斗")[-3].click()
            elif level >= 30 and level < 40:
                browser.find_elements_by_link_text("乐斗")[-4].click()
            elif level >= 40 and level < 50:
                browser.find_element_by_link_text("下页").click()
                browser.find_element_by_link_text("乐斗").click()
            browser.find_element_by_link_text("末页").click()
            count = 0
            tili_kong = False

        while int(re.search(r'当前体力值：(\d+)/100', browser.page_source).group(1)) >= 10:
            try:
                browser.find_elements_by_link_text("乐斗")[-2].click()
            except:
                browser.find_element_by_link_text("上页").click()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 许愿
    print('许愿**********')
    try:
        browser.find_element_by_link_text("许愿").click()
    except:
        print('等级未达到10级')
    else:
        try:
            browser.find_element_by_link_text("领取许愿奖励").click()
        except:
            print('已领取许愿奖励')
        try:
            browser.find_element_by_link_text("许愿").click()
            a = random.random()
            if a < 0.25:
                browser.find_element_by_link_text("向菜菜上香许愿").click()
            elif a >= 0.25 and a < 0.5:
                browser.find_element_by_link_text("向剑君上香许愿").click()
            elif a >= 0.5 and a < 0.75:
                browser.find_element_by_link_text("向月敏上香许愿").click()
            else:
                browser.find_element_by_link_text("向小王子上香许愿").click()
        except:
            print('已许愿or没拿首胜')
        browser.find_element_by_link_text("领取").click()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    # 任务
    print('任务**********')
    browser.find_element_by_link_text("任务").click()
    browser.find_element_by_link_text("一键完成任务").click()
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 分享
    print('分享**********')
    browser.find_element_by_link_text("分享").click()
    browser.find_element_by_link_text("一键分享").click()
    browser.find_element_by_link_text("返回大乐斗首页").click()

    # 活跃奖励
    try:
        browser.find_element_by_link_text("领奖").click()
    except:
        print('活跃度不足20')
    else:
        for i in range(4):
            browser.find_element_by_link_text("领取").click()
        browser.find_element_by_link_text("返回大乐斗首页").click()

    browser.find_element_by_link_text("退出").click()

browser.quit()
f_account.close()