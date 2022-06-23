import getGift
import login
import up_to_date
import asyncio

if __name__ == '__main__':
    # 获取用户登录状态
    cookies = login.bzlogin()

    # 询问用户使用什么功能
    print("\n本程序目前拥有的功能：")
    print("[1] 生成大航海信息记录（xls格式）")
    print("[2] 生成可直接导入BiliMessenger使用的数据列表（csv格式）")
    print("[3] 生成所有礼物流水列表（xls格式）")
    print("[4] 同时生成上述三个文件")
    print("之后会要求您输入想要查询的日期区间（闭区间，统计结果包含开始和结束日期的礼物数据）")
    while True:
        choice = int(input("请输入数字来使用相对应的功能："))
        if choice not in [1, 2, 3, 4]:
            print("无效输入，请重新尝试")
        else:
            break

    # 使用功能
    print("==========================================")

    gift_info = getGift.GiftInfo(cookies)
    gift_info.period_time()
    print("开始获取礼物信息...")
    if choice == 1:
        asyncio.run(gift_info.generateXlsFile())
    elif choice == 2:
        asyncio.run(gift_info.generateCsvFile())
    elif choice == 3:
        asyncio.run(gift_info.xlsWrite())
    elif choice == 4:
        asyncio.run(gift_info.run_all())

    # 检测更新
    up_to_date.main("v0.6.2")

    # 防止快速退出
    input("\n\n按回车退出程序")
