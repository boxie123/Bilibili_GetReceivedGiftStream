import time

import getGift
import login

if __name__ == '__main__':
    # 获取用户登录状态
    session = login.bzlogin()

    # 询问用户使用什么功能
    print("\n本程序目前拥有的功能：")
    print("[1] 生成大航海信息记录（txt格式）")
    print("[2] 生成大航海信息记录（xls格式）")
    print("[3] 生成可直接导入BiliMessenger使用的数据列表（csv格式）")
    print("[4] 生成所有礼物流水列表（xls格式）")
    print("之后会要求您输入想要查询的日期区间（闭区间，统计结果包含开始和结束日期的礼物数据）")
    while True:
        choice = int(input("请输入数字来使用相对应的功能："))
        if choice not in [1, 2, 3, 4]:
            print("无效输入，请重新尝试")
        else:
            break

    # 使用功能
    print("==========================================")

    gift_info = getGift.GiftInfo(session)
    gift_info.period_time()
    print("开始获取礼物信息...")
    if choice == 1:
        gift_info.generateTxtFile()
    elif choice == 2:
        gift_info.generateXlsFile()
    elif choice == 3:
        gift_info.generateCsvFile()
    else:
        gift_info.xlsWrite()

    # 防止快速退出
    time.sleep(5)
