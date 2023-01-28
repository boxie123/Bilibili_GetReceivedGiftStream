import csv
import datetime
import sys

import httpx
import xlsxwriter
from rich.progress import track

import agent
from console import console


# 处理全部礼物数据生成字典以及{uid:name}字典
def all_info_handle(gifts_list):
    id_index = {}
    gift_result = {}
    for gift in gifts_list:
        key = str(gift["uid"])
        id_index[key] = gift["uname"]
        gift_name = gift["gift_name"]
        gift_id = gift["gift_id"]
        gold = gift["normal_gold"] / 100
        gift_num = gift["gift_num"]
        time = gift["time"]

        if key in gift_result:
            if gift_id in gift_result[key]:
                gift_result[key][gift_id]["gold"] += gold
                gift_result[key][gift_id]["gift_num"] += gift_num
                gift_result[key][gift_id]["time"].insert(0, gift["time"])
            else:
                gift_result[key][gift_id] = {
                    "gift_name": gift_name,
                    "gold": gold,
                    "gift_num": gift_num,
                    "time": [time],
                }
        else:
            gift_result[key] = {
                gift_id: {
                    "gift_name": gift_name,
                    "gold": gold,
                    "gift_num": gift_num,
                    "time": [time],
                }
            }
    return gift_result, id_index


# 处理礼物信息生成大航海字典以及{uid:name}字典
def guard_info(gifts_list):
    id_index = {}
    gift_result = {}
    for gift in gifts_list:
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


def try_int(num):
    while True:
        try:
            int_num = int(num)
            break
        except ValueError:
            console.print("\n[bold red]Warning:[/bold red] 输入错误，请输入纯数字")
            num = console.input("请重新输入：")
    return int_num


class GiftInfo:
    # 构造函数，生成特定格式的日期列表
    def __init__(self, client):
        self.cookies = client.cookies
        client.close()
        while True:
            console.rule("输入查询开始日期")
            year_begin = console.input("请输入想查询的开始[blue]年份[/blue]（四位纯数字）（直接回车默认今年）：")
            if year_begin == "":
                self.year_begin = datetime.datetime.today().year
            else:
                self.year_begin = try_int(year_begin)

            month_begin = console.input("请输入想查询的开始[blue]月份[/blue]（直接回车默认本月）：")
            if month_begin == "":
                self.month_begin = datetime.datetime.today().month
            else:
                self.month_begin = try_int(month_begin)

            day_begin = console.input("请输入想查询的开始[blue]日期[/blue]（直接回车默认今日）：")
            if day_begin == "":
                self.day_begin = datetime.datetime.today().day
            else:
                self.day_begin = try_int(day_begin)

            try:
                date_begin = datetime.date(
                    self.year_begin, self.month_begin, self.day_begin
                )
                break
            except ValueError as e:
                console.print(f"\n[bold red]Warning:[/bold red] 输入日期错误：{e}")
                console.print("请重新输入\n")

        most_early_date = datetime.date.today() - datetime.timedelta(179)
        if date_begin < most_early_date:
            console.print(
                "\n[bold red]Warning:[/bold red] b站仅提供近180天数据，可查询最早日期为：{}".format(
                    most_early_date.strftime("%Y-%m-%d")
                )
            )
            console.print("您查询的日期超出范围的部分数据将[b red]全部为0[/b red]\n")
            while True:
                choice = console.input("输入[b blue]y[/b blue]确认继续：")
                if choice == "y" or choice == "Y":
                    break

        while True:
            console.rule("输入查询末尾日期")
            year_end = console.input("请输入想查询的结束[blue]年份[/blue]（四位纯数字）（直接回车默认今年）：")
            if year_end == "":
                self.year_end = datetime.datetime.today().year
            else:
                self.year_end = try_int(year_end)

            month_end = console.input("请输入想查询的结束[blue]月份[/blue]（直接回车默认本月）：")
            if month_end == "":
                self.month_end = datetime.datetime.today().month
            else:
                self.month_end = try_int(month_end)

            day_end = console.input("请输入想查询的结束[blue]日期[/blue]（直接回车默认今日）：")
            if day_end == "":
                self.day_end = datetime.datetime.today().day
            else:
                self.day_end = try_int(day_end)

            try:
                date_end = datetime.date(self.year_end, self.month_end, self.day_end)
                break
            except ValueError as e:
                console.print(f"\n[bold red]Warning:[/bold red] 输入日期错误：{e}")
                console.print("请重新输入\n")

        if date_begin > date_end:
            console.print("\n[bold red]Warning:[/bold red] 开始日期晚于结束日期，将生成空表格\n")
            while True:
                choice = console.input("输入0确认继续：")
                if choice == "0":
                    break

        day_list_range = []
        delta = datetime.timedelta(days=1)
        while date_begin <= date_end:
            day_str = date_begin.strftime("%Y-%m-%d")
            day_list_range.append(day_str)
            date_begin += delta

        self.day_list = day_list_range
        self.name = "{}年{}月{}日至{}年{}月{}日礼物统计".format(
            self.year_begin,
            self.month_begin,
            self.day_begin,
            self.year_end,
            self.month_end,
            self.day_end,
        )

    # 获取某一段时间礼物信息
    async def getGiftInfoOneDay(self):
        url = "https://api.live.bilibili.com/xlive/revenue/v1/giftStream/getReceivedGiftStreamNextList"
        headers = {
            "User-Agent": agent.get_user_agents(),
            "Referer": "https://link.bilibili.com/p/center/index",
        }
        all_gifts_list = []
        async with httpx.AsyncClient(
            cookies=self.cookies, headers=headers
        ) as async_client:
            for date in track(self.day_list, description="正在抓取礼物信息", console=console):
                params = {
                    "limit": sys.maxsize - 1,
                    "coin_type": 0,
                    "gift_id": "",
                    "begin_time": date,
                    "uname": "",
                }
                resp = await async_client.get(url, params=params)
                all_info = resp.json()
                gifts_list = all_info["data"]["list"]
                has_more = all_info["data"]["has_more"]
                if gifts_list:
                    last_id = gifts_list[-1]["id"]
                    all_gifts_list.extend(gifts_list)

                while has_more:
                    console.print("[b red]已触发“has_more”[/b red]")
                    params = {
                        "last_id": last_id,
                        "limit": sys.maxsize - 1,
                        "coin_type": 0,
                        "gift_id": "",
                        "begin_time": date,
                        "uname": "",
                    }
                    resp = await async_client.get(url, params=params)
                    all_info = resp.json()
                    gifts_list = all_info["data"]["list"]
                    has_more = all_info["data"]["has_more"]
                    if gifts_list:
                        last_id = gifts_list[-1]["id"]
                        all_gifts_list.extend(gifts_list)

        return all_gifts_list

    # 全部礼物信息写入xlsx文件
    def xlsWrite(self, gift_result, id_index):
        with console.status(f"正在写入[b green]{self.name}.xlsx[/b green]", spinner="line"):
            wb = xlsxwriter.Workbook(self.name + ".xlsx")
            sheet = wb.add_worksheet("电池数量")
            sheet_num = wb.add_worksheet("礼物数目")
            sheet_header_list = ["ID", "UID"]
            sheet.write_row(0, 0, sheet_header_list)
            sheet_num.write_row(0, 0, sheet_header_list)

            row = 1
            gold_sum_list = [
                "SUM",
            ]
            for uid in gift_result:
                sheet.write(row, 1, uid)
                sheet.write(row, 0, id_index[uid])
                sheet_num.write(row, 1, uid)
                sheet_num.write(row, 0, id_index[uid])
                gold_sum = 0
                for gift_id in gift_result[uid]:
                    if gift_id not in sheet_header_list:
                        sheet_header_list.append(gift_id)
                        column = sheet_header_list.index(gift_id)
                        gift_name = gift_result[uid][gift_id]["gift_name"]
                        sheet.write(0, column, f"{gift_name}(id:{gift_id})")
                        sheet_num.write(0, column, f"{gift_name}(id:{gift_id})")
                    column = sheet_header_list.index(gift_id)
                    gold_temp = gift_result[uid][gift_id]["gold"]
                    sheet.write(row, column, gold_temp)
                    gold_sum += gold_temp
                    sheet_num.write(row, column, gift_result[uid][gift_id]["gift_num"])
                row += 1
                gold_sum_list.append(gold_sum)

            # 求和
            column = len(sheet_header_list)
            sheet.write_column(0, column, gold_sum_list)

            wb.close()

            console.print("[b green]{}.xlsx[/b green] 已生成！".format(self.name))

    # 根据大航海礼物信息生成xlsx统计结果
    def generateXlsFile(self, guard_dict, id_index):
        with console.status(
            f"正在写入[b green]{self.name}(大航海).xlsx[/b green]", spinner="line"
        ):
            wb = xlsxwriter.Workbook(filename=self.name + "(大航海).xlsx")

            text_wrap = wb.add_format({"text_wrap": True})
            sheet = wb.add_worksheet("上舰时间")
            sheet_header_list = ["ID", "UID", "舰长", "提督", "总督"]

            sheet.write_row(0, 0, sheet_header_list)
            sheet.set_column(1, len(sheet_header_list), 25)

            row = 1
            sheet1 = wb.add_worksheet("上舰具体数量")
            sheet1_head = ["ID", "UID", "总积分", "舰长", "提督", "总督"]
            sheet1.write_row(0, 0, sheet1_head)
            row1 = 1

            for uid in guard_dict:
                scores = (
                    len(guard_dict[uid]["舰长"])
                    + 15 * len(guard_dict[uid]["提督"])
                    + 200 * len(guard_dict[uid]["总督"])
                )
                sheet.write(row, 1, uid)
                sheet.write(row, 0, id_index[uid])
                sheet1.write(row1, 1, uid)
                sheet1.write(row1, 0, id_index[uid])
                sheet1.write(row1, 2, scores)
                for title in guard_dict[uid]:
                    all_dates = guard_dict[uid][title]
                    column1 = sheet1_head.index(title)
                    sheet1.write(row1, column1, len(all_dates))
                    if len(all_dates) == 0:
                        continue
                    column = sheet_header_list.index(title)
                    time_str = "\n".join(all_dates)
                    sheet.write(row, column, time_str, text_wrap)
                row += 1
                row1 += 1

            wb.close()

            console.print("[b green]{}(大航海).xlsx[/b green] 已生成！".format(self.name))

    # 根据礼物信息生成csv统计结果，可直接导入BiliMessenger使用
    def generateCsvFile(self, guard_dict, id_index):
        with console.status(
            f"正在写入[b green]{self.name}(大航海).csv[/b green]", spinner="line"
        ):
            csv_list = []
            for uid, gifts in guard_dict.items():
                usr_name = id_index[uid]
                gifts_name = ""
                gifts_list = ["舰长", "提督", "总督"]
                for i in gifts_list:
                    if gifts[i]:
                        gifts_name = i

                row_list = [gifts_name, uid, usr_name]
                csv_list.append(row_list)

            with open(
                self.name + "(大航海).csv", mode="w", encoding="utf-8-sig", newline=""
            ) as f:
                writer = csv.writer(f)
                writer.writerows(csv_list)

            console.print("[b green]{}(大航海).csv[/b green] 已生成！".format(self.name))

    async def main(self, choice):
        gifts_list = await self.getGiftInfoOneDay()
        if choice == "1":
            guard_dict, id_index = guard_info(gifts_list)
            self.generateXlsFile(guard_dict, id_index)
        elif choice == "2":
            guard_dict, id_index = guard_info(gifts_list)
            self.generateCsvFile(guard_dict, id_index)
        elif choice == "3":
            gift_result, id_index = all_info_handle(gifts_list)
            self.xlsWrite(gift_result, id_index)
        elif choice == "4":
            guard_dict, id_index = guard_info(gifts_list)
            self.generateXlsFile(guard_dict, id_index)
            self.generateCsvFile(guard_dict, id_index)
            gift_result, id_index = all_info_handle(gifts_list)
            self.xlsWrite(gift_result, id_index)
            console.print("\n已全部生成完成！")
