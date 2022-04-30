import calendar
import datetime
import os
import sys

import xlwt

import agent


def get_header():
    headers = {"User-Agent": agent.get_user_agents(),
               "Referer": "https://link.bilibili.com/p/center/index"}
    return headers


def get_date_list(year, month):
    day_num = calendar.monthrange(year, month)[1]
    day_list = []
    for i in range(day_num):
        day_str = "{}-{:0>2d}-{:0>2d}".format(year, month, i + 1)
        day_list.append(day_str)
    return day_list


def year_month():
    year = input("请输入想查询的年份（直接回车默认今年）：")
    if year == "":
        year = datetime.datetime.today().year
    else:
        year = int(year)

    month = input("请输入想查询的月份（直接回车默认本月）：")
    if month == "":
        month = datetime.datetime.today().month
    else:
        month = int(month)

    return year, month


def gift_get(session, year, month):
    date_list = get_date_list(year, month)
    result = {}
    for date in date_list:
        all_info = session.get(
            url="https://api.live.bilibili.com/xlive/revenue/v1/giftStream/getReceivedGiftStreamNextList",
            params={
                "limit": sys.maxsize - 1,
                "coin_type": 0,
                "gift_id": "",
                "begin_time": date,
                "uname": ""
            },
            headers=get_header()
        ).json()

        gifts = all_info["data"]["list"]
        gift_num = len(gifts)

        for i in range(gift_num):
            key = gifts[i]["uname"] + " (" + str(gifts[i]["uid"]) + ")"
            if gifts[i]["gift_name"] in ("舰长", "提督", "总督"):
                title = gifts[i]["gift_name"]
            else:
                continue

            if key in result:
                result[key][title].insert(0, gifts[i]["time"])
            else:
                val = {"总督": [], "提督": [], "舰长": [], title: [gifts[i]["time"]]}
                result[key] = val
    return result


def generate_gift_file(session):
    year, month = year_month()
    result_dict = gift_get(session, year, month)
    gift_file_xls(result_dict)
    aige_score_calc(session)
    nowdir = os.getcwd()
    result_file = os.path.join(nowdir, "统计结果.txt")
    file = open(result_file, "w", encoding="utf-8")
    for usr in result_dict:
        line = "========== " + usr + " 的大航海 ==========\n"
        for title in result_dict[usr]:
            all_dates = result_dict[usr][title]
            if len(all_dates) == 0:
                continue
            line += (title + '：\n')
            for date in all_dates:
                line += (date + '\n')
        file.write(line + '\n')
    file.close()


def gift_file_xls(gift_dict):
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('大航海统计')
    sheet.write(0, 0, 'ID')
    sheet.write(0, 1, '大航海类型')
    sheet.write(0, 2, '时间')
    row = 1
    sheet1 = wb.add_sheet('积分计算')
    sheet1_head = ['ID', '当月积分', '舰长', '提督', '总督']
    for i in range(len(sheet1_head)):
        sheet1.write(0, i, sheet1_head[i])
    row1 = 1
    for usr in gift_dict:
        sheet.write(row, 0, usr)
        sheet1.write(row1, 0, usr)
        scores = len(gift_dict[usr]['舰长']) + 15 * len(gift_dict[usr]['提督']) + 200 * len(gift_dict[usr]['总督'])
        sheet1.write(row1, 1, scores)
        for title in gift_dict[usr]:
            all_dates = gift_dict[usr][title]
            column = sheet1_head.index(title)
            sheet1.write(row1, column, len(all_dates))
            if len(all_dates) == 0:
                continue
            sheet.write(row, 1, title)
            for date in all_dates:
                sheet.write(row, 2, date)
                row += 1
        row1 += 1
    wb.save("大航海统计.xls")


def aige_score_calc(session):
    now_year = datetime.datetime.today().year
    now_month = datetime.datetime.today().month
    score_dict = {}
    date_str_list = []
    for year in range(2021, now_year + 1):
        if year == 2021:
            begin_month = 9
            end_month = 12
        else:
            begin_month = 1
            end_month = now_month

        for month in range(begin_month, end_month + 1):
            date_str = "-".join((str(year), str(month)))
            date_str_list.append(date_str)
            gift_dict = gift_get(session, year, month)
            for usr, value in gift_dict.items():
                scores = len(gift_dict[usr]['舰长']) + \
                         15 * len(gift_dict[usr]['提督']) + \
                         200 * len(gift_dict[usr]['总督'])

                if usr in score_dict:
                    score_dict[usr][date_str] = scores
                else:
                    score_dict[usr] = {date_str: scores}

    wb = xlwt.Workbook()
    sheet = wb.add_sheet('艾鸽积分')

    for i in range(len(date_str_list)):
        sheet.write(0, i + 1, date_str_list[i])

    row = 1
    for usr in score_dict:
        sheet.write(row, 0, usr)
        for i in range(len(date_str_list)):
            if date_str_list[i] in score_dict[usr]:
                sheet.write(row, i + 1, score_dict[usr][date_str_list[i]])
            else:
                sheet.write(row, i + 1, 0)
        row += 1

    wb.save("艾鸽积分.xls")
