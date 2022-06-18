import csv
import datetime
import os
import sys

import xlwt

import agent


class GiftInfo:
    # 构造函数
    def __init__(self, session):
        self.session = session
        self.year_begin = 0
        self.month_begin = 0
        self.day_list = []
        self.day_begin = 0
        self.day_end = 0
        self.month_end = 0
        self.year_end = 0
        self.name = ""

    # 获取礼物信息，返回大航海礼物信息字典和{uid: id}字典
    def getGiftInfo(self):
        gift_result = {}
        id_index = {}
        for date in self.day_list:
            url = "https://api.live.bilibili.com/xlive/revenue/v1/giftStream/getReceivedGiftStreamNextList"
            params = {
                "limit": sys.maxsize - 1,
                "coin_type": 0,
                "gift_id": "",
                "begin_time": date,
                "uname": ""
            }
            headers = {
                "User-Agent": agent.get_user_agents(),
                "Referer": "https://link.bilibili.com/p/center/index"
            }
            all_info = self.session.get(url=url, params=params, headers=headers).json()
            gifts = all_info["data"]["list"]

            for gift in gifts:
                key = str(gift["uid"])
                id_index[key] = gift["uname"]
                if gift["gift_name"] in ("舰长", "提督", "总督"):
                    title = gift["gift_name"]
                else:
                    continue

                if key in gift_result:
                    gift_result[key][title].insert(0, gift["time"])
                else:
                    val = {"总督": [], "提督": [], "舰长": [], title: [gift["time"]]}
                    gift_result[key] = val

        return gift_result, id_index

    # 生成特定格式的日期列表
    def period_time(self):
        year_begin = input("请输入想查询的开始年份（直接回车默认今年）：")
        if year_begin == "":
            self.year_begin = datetime.datetime.today().year
        else:
            self.year_begin = int(year_begin)

        month_begin = input("请输入想查询的开始月份（直接回车默认本月）：")
        if month_begin == "":
            self.month_begin = datetime.datetime.today().month
        else:
            self.month_begin = int(month_begin)

        day_begin = input("请输入想查询的开始日期（直接回车默认今日）：")
        if day_begin == "":
            self.day_begin = datetime.datetime.today().day
        else:
            self.day_begin = int(day_begin)

        year_end = input("请输入想查询的结束年份（直接回车默认今年）：")
        if year_end == "":
            self.year_end = datetime.datetime.today().year
        else:
            self.year_end = int(year_end)

        month_end = input("请输入想查询的结束月份（直接回车默认本月）：")
        if month_end == "":
            self.month_end = datetime.datetime.today().month
        else:
            self.month_end = int(month_end)

        day_end = input("请输入想查询的结束日期（直接回车默认今日）：")
        if day_end == "":
            self.day_end = datetime.datetime.today().day
        else:
            self.day_end = int(day_end)

        date_begin = datetime.date(self.year_begin, self.month_begin, self.day_begin)
        date_end = datetime.date(self.year_end, self.month_end, self.day_end)
        day_list_range = []
        delta = datetime.timedelta(days=1)
        while date_begin <= date_end:
            day_str = date_begin.strftime('%Y-%m-%d')
            day_list_range.append(day_str)
            date_begin += delta

        self.day_list = day_list_range
        self.name = "{}年{}月{}日至{}年{}月{}日礼物统计".format(self.year_begin, self.month_begin, self.day_begin,
                                                     self.year_end, self.month_end, self.day_end)

    # 获取某一段时间礼物信息，返回礼物信息字典和{uid: id}字典
    def getGiftInfoOneDay(self):
        gift_result = {}
        id_index = {}
        for date in self.day_list:
            url = "https://api.live.bilibili.com/xlive/revenue/v1/giftStream/getReceivedGiftStreamNextList"
            params = {
                "limit": sys.maxsize - 1,
                "coin_type": 0,
                "gift_id": "",
                "begin_time": date,
                "uname": ""
            }
            headers = {
                "User-Agent": agent.get_user_agents(),
                "Referer": "https://link.bilibili.com/p/center/index"
            }

            all_info = self.session.get(url=url, params=params, headers=headers).json()
            gifts = all_info["data"]["list"]

            for gift in gifts:
                key = str(gift["uid"])
                id_index[key] = gift["uname"]
                title = gift["gift_name"]
                gold = gift["normal_gold"] / 100

                if key in gift_result:
                    if title in gift_result[key]:
                        gift_result[key][title] += gold
                    else:
                        gift_result[key][title] = gold
                else:
                    val = {title: gold}
                    gift_result[key] = val

        return gift_result, id_index

    # 写入xls文件
    def xlsWrite(self):
        gift_result, id_index = self.getGiftInfoOneDay()
        wb = xlwt.Workbook(encoding="utf-8")
        sheet = wb.add_sheet(self.name)
        sheet_header_list = ['ID', 'UID']
        row = 1

        for usr in gift_result:
            sheet.write(row, 1, usr)
            sheet.write(row, 0, id_index[usr])
            for title in gift_result[usr]:
                if title not in sheet_header_list:
                    sheet_header_list.append(title)

                column = sheet_header_list.index(title)
                sheet.write(row, column, gift_result[usr][title])

            row += 1

        for i in range(len(sheet_header_list)):
            sheet.write(0, i, sheet_header_list[i])

        wb.save(self.name + ".xls")
        print("统计结果生成完成！请查看\"{}.xls\"".format(self.name))

    # 根据大航海礼物信息生成txt统计结果
    def generateTxtFile(self):
        gift_dict, id_index = self.getGiftInfo()
        nowdir = os.getcwd()
        result_file = os.path.join(nowdir, self.name + ".txt")
        file = open(result_file, "w", encoding="utf-8")
        for usr in gift_dict:
            line = "========== " + id_index[usr] + "(" + usr + ") 的大航海 ==========\n"
            for title in gift_dict[usr]:
                all_dates = gift_dict[usr][title]
                if len(all_dates) == 0:
                    continue
                line += (title + '：\n')
                for date in all_dates:
                    line += (date + '\n')
            file.write(line + '\n')
        file.close()
        print("统计结果生成完成！请查看\"{}.txt\"".format(self.name))

    # 根据大航海礼物信息生成xls统计结果
    def generateXlsFile(self):
        gift_dict, id_index = self.getGiftInfo()
        wb = xlwt.Workbook(encoding="utf-8")
        style = xlwt.XFStyle()
        style.alignment.wrap = 1
        sheet = wb.add_sheet(self.name)
        sheet_header_list = ['ID', 'UID', '舰长', '提督', '总督']
        for i in range(len(sheet_header_list)):
            sheet.write(0, i, sheet_header_list[i])
        row = 1

        sheet1 = wb.add_sheet('积分计算')
        sheet1_head = ['ID', 'UID', '当月积分', '舰长', '提督', '总督']
        for i in range(len(sheet1_head)):
            sheet1.write(0, i, sheet1_head[i])
        row1 = 1

        for usr in gift_dict:
            sheet1.write(row1, 1, usr)
            sheet1.write(row1, 0, id_index[usr])
            scores = len(gift_dict[usr]['舰长']) + 15 * len(gift_dict[usr]['提督']) + 200 * len(gift_dict[usr]['总督'])
            sheet1.write(row1, 2, scores)
            for title in gift_dict[usr]:
                all_dates = gift_dict[usr][title]
                column1 = sheet1_head.index(title)
                sheet1.write(row1, column1, len(all_dates))
                if len(all_dates) == 0:
                    continue
                sheet.write(row, 1, usr)
                sheet.write(row, 0, id_index[usr])
                column = sheet_header_list.index(title)
                time_str = "\n".join(all_dates)
                sheet.write(row, column, time_str, style)
            row += 1
            row1 += 1
        wb.save(self.name + "(大航海).xls")
        print("统计结果生成完成！请查看\"{}(大航海).xls\"".format(self.name))

    # 根据礼物信息生成csv统计结果，可直接导入BiliMessenger使用
    def generateCsvFile(self):
        gift_dict, id_index = self.getGiftInfo()
        csv_list = []
        for uid, gifts in gift_dict.items():
            usr_name = id_index[uid]
            gifts_name = ""
            gifts_list = ["舰长", "提督", "总督"]
            for i in gifts_list:
                if gifts[i]:
                    gifts_name = i

            row_list = [gifts_name, uid, usr_name]
            csv_list.append(row_list)

        with open(self.name + "(大航海).csv", mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(csv_list)
        print("统计结果生成完成！请查看\"{}(大航海).csv\"".format(self.name))
