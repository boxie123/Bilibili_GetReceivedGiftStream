import datetime
import time

import getGift
import login

if __name__ == '__main__':
    # 获取用户登录状态
    session = login.bzlogin()

    # 询问用户使用什么功能
    print("\n本程序目前拥有的功能：")
    print("[0] 生成近5个月所有人的大航海积分xls表格")
    print("[1] 生成输入年份和月份的大航海信息记录（txt格式）")
    print("[2] 生成输入年份和月份的大航海信息记录（xls格式）")
    print("[3] 生成可直接导入BiliMessenger使用的数据列表（csv格式）")
    print("其中[1]、[2]和[3]会之后要求您输入想要查询的年月份")
    while True:
        choice = int(input("请输入数字来使用相对应的功能："))
        if choice not in [0, 1, 2, 3]:
            print("无效输入，请重新尝试")
        else:
            break

    # 使用功能
    print("==========================================")
    if choice == 0:
        print("开始生成大航海积分统计...")
        getGift.aige_score_calc(session)
        print("统计结果生成完成！请查看\"艾鸽积分.xls\"")
    else:
        # 询问用户要查询的年份和月份
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

        gift_info = getGift.GiftInfo(session, year, month)
        print("开始获取大航海信息...")
        if choice == 1:
            gift_info.generateTxtFile()
            print("统计结果生成完成！请查看\"{}年{}月大航海统计.txt\"".format(year, month))
        elif choice == 2:
            gift_info.generateXlsFile()
            print("统计结果生成完成！请查看\"{}年{}月大航海统计.xls\"".format(year, month))
        else:
            gift_info.generateCsvFile()
            print("统计结果生成完成！请查看\"{}年{}月大航海统计.csv\"".format(year, month))

    # 防止快速退出
    time.sleep(5)
