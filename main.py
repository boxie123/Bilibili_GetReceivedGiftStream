import asyncio
import sys

from rich.panel import Panel
from rich.prompt import Prompt
from rich.tree import Tree

from src import (
    getGift,
    login,
    up_to_date,
)
from src.console import console

if __name__ == "__main__":
    # 获取用户登录状态
    console.print(
        Panel.fit(
            r"""
   ,---,           ,---,   ,----..        ,---,. 
  '  .' \       ,`--.' |  /   /   \     ,'  .' | 
 /  ;    '.     |   :  : |   :     :  ,---.'   | 
:  :       \    :   |  ' .   |  ;. /  |   |   .' 
:  |   /\   \   |   :  | .   ; /--`   :   :  |-, 
|  :  ' ;.   :  '   '  ; ;   | ;  __  :   |  ;/| 
|  |  ;/  \   \ |   |  | |   : |.' .' |   :   .' 
'  :  | \  \ ,' '   :  ; .   | '_.' : |   |  |-, 
|  |  '  '--'   |   |  ' '   ; : \  | '   :  ;/| 
|  :  :         '   :  | '   | '/  .' |   |    \ 
|  | ,'         ;   |.'  |   :    /   |   :   .' 
`--''           '---'     \   \ .'    |   | ,'   
                           `---`      `----'     
    """,
            title="本程序图标由 [b bright_magenta]艾鸽泰尔德[/b bright_magenta] 友情赞助",
            subtitle="UID 1485569",
        )
    )
    client = login.main()

    # 询问用户使用什么功能
    console.print("\n本程序目前拥有的功能：\n")
    function_list = Tree("[b]功能列表[/b]")
    function_list.add("[[b blue]0[/b blue]] 退出")
    function_list.add(
        "[[b blue]1[/b blue]] 生成[b green]大航海[/b green]信息记录（[b blue]xlsx[/b blue]格式）"
    )
    function_list.add(
        "[[b blue]2[/b blue]] 生成可直接导入 [b green]BiliMessenger[/b green] 使用的大航海数据列表（[b blue]csv[/b blue]格式）"
    )
    function_list.add(
        "[[b blue]3[/b blue]] 生成[b green]所有礼物流水[/b green]列表（[b blue]xlsx[/b blue]格式）"
    )
    function_list.add("[[b blue]4[/b blue]] 同时生成[b yellow]上述三个[/b yellow]文件")
    console.print(function_list)
    console.print("之后会要求您输入想要查询的日期区间（[b red]闭区间[/b red]，统计结果包含开始和结束日期的礼物数据）")

    choice = Prompt.ask(
        "\n请输入[b blue]相应数字[/b blue]来使用相对应的功能：",
        choices=["0", "1", "2", "3", "4"],
        default="4",
    )
    if choice == "0":
        sys.exit(0)

    # 使用功能
    gift_info = getGift.GiftInfo(client)
    console.rule("获取礼物信息")
    asyncio.run(gift_info.main(choice))

    # 检测更新
    try:
        up_to_date.main("v0.8.2")
    except Exception:
        console.print("检测失败")

    # 防止快速退出
    console.input("\n\n感谢使用，按回车[blue]退出[/blue]程序")
