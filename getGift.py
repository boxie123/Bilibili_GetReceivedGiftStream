import calendar
import datetime
import os
import sys
import xlwt
import agent


class GiftInfo:
    # 构造函数
    def __init__(self, session, year, month):
        self.session = session
        self.year = year
        self.month = month
        self.day_list = []

        day_num = calendar.monthrange(year, month)[1]
        for i in range(day_num):
            day_str = "{}-{:0>2d}-{:0>2d}".format(year, month, i + 1)
            self.day_list.append(day_str)


    # 获取单月份礼物信息，返回礼物信息字典和{uid: id}字典
    def getGiftInfo(self):
        gift_result = {}
        id_index = {}
        for date in self.day_list:
            url="https://api.live.bilibili.com/xlive/revenue/v1/giftStream/getReceivedGiftStreamNextList"
            params={
                "limit": sys.maxsize - 1,
                "coin_type": 0,
                "gift_id": "",
                "begin_time": date,
                "uname": ""
            }
            headers={
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


    # 根据礼物信息生成txt统计结果
    def generateTxtFile(self):
        gift_dict, id_index = self.getGiftInfo()
        nowdir = os.getcwd()
        result_file = os.path.join(nowdir, "{}年{}月大航海统计.txt".format(self.year, self.month))
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


    # 根据礼物信息生成xls统计结果
    def generateXlsFile(self):
        gift_dict, id_index = self.getGiftInfo()
        wb = xlwt.Workbook()
        name = "{}年{}月大航海统计".format(self.year, self.month)
        sheet = wb.add_sheet(name)
        sheet_header_list = ['ID', 'UID', '大航海类型', '时间']
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
                column = sheet1_head.index(title)
                sheet1.write(row1, column, len(all_dates))
                if len(all_dates) == 0:
                    continue
                for date in all_dates:
                    sheet.write(row, 1, usr)
                    sheet.write(row, 0, id_index[usr])
                    sheet.write(row, 2, title)
                    sheet.write(row, 3, date)
                    row += 1
            row1 += 1
        wb.save(name + ".xls")



# 专门给鸽宝的统计迄今为止舰长积分
def aige_score_calc(session):
    now_year = datetime.datetime.today().year
    now_month = datetime.datetime.today().month
    score_dict = {}
    id_index_total = {}
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
            temp_gift_info = GiftInfo(session, year, month)
            gift_dict, id_index = temp_gift_info.getGiftInfo()
            id_index_total.update(id_index)

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
    sheet.write(0, 0, "ID")
    sheet.write(0, 1, "UID")
    for i in range(len(date_str_list)):
        sheet.write(0, i + 2, date_str_list[i])

    row = 1
    for usr in score_dict:
        sheet.write(row, 1, usr)
        sheet.write(row, 0, id_index_total[usr])
        for i in range(len(date_str_list)):
            if date_str_list[i] in score_dict[usr]:
                sheet.write(row, i + 2, score_dict[usr][date_str_list[i]])
            else:
                sheet.write(row, i + 2, 0)
        row += 1
    wb.save("艾鸽积分.xls")
