import sys

import getGift
import login
import up_to_date
import asyncio

if __name__ == "__main__":
    # 获取用户登录状态
    client = login.bzlogin()

    # 询问用户使用什么功能
    print("\n本程序目前拥有的功能：")
    print("[0] 退出")
    print("[1] 生成大航海信息记录（xls格式）")
    print("[2] 生成可直接导入BiliMessenger使用的数据列表（csv格式）")
    print("[3] 生成所有礼物流水列表（xls格式）")
    print("[4] 同时生成上述三个文件")
    print("之后会要求您输入想要查询的日期区间（闭区间，统计结果包含开始和结束日期的礼物数据）")
    while True:
        choice = input("请输入数字来使用相对应的功能：")
        if choice not in ["0", "1", "2", "3", "4"]:
            print("无效输入，请重新尝试")
        elif choice == "0":
            sys.exit(0)
        else:
            break

    # 使用功能
    gift_info = getGift.GiftInfo(client)
    print("开始获取礼物信息...")
    asyncio.run(gift_info.main(choice))

    # 检测更新
    try:
        up_to_date.main("v0.7.2")
    except Exception:
        print("检测失败")

    # 防止快速退出
    input("\n\n按回车退出程序")
