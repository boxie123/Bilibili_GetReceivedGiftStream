import asyncio

from rich.panel import Panel
from rich.prompt import Prompt
from rich.tree import Tree

from src import getGift, login, up_to_date
from src.console import console
from src.live_exit import live_exit

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
            title="本程序美术资源由 [b bright_magenta]艾鸽泰尔德[/b bright_magenta] 友情提供",
            subtitle="UID 1485569",
        )
    )
    client = login.main()

    function_dict = {
        0: "退出",
        1: "生成[b green]大航海[/b green]信息记录（[b blue]xlsx[/b blue]格式）",
        2: "生成可直接导入 [b green]BiliMessenger[/b green] 使用的大航海数据列表（[b blue]csv[/b blue]格式）",
        3: "生成[b green]所有礼物流水[/b green]列表（[b blue]xlsx[/b blue]格式）",
        4: "同时生成[b yellow]上述三个[/b yellow]文件",
    }

    # 询问用户使用什么功能
    console.print("\n本程序目前拥有的功能：\n")

    function_list_tree = Tree("[b]功能列表[/b]")
    for key, values in function_dict.items():
        function_list_tree.add(f"[b][[cyan]{key}[/cyan]][/b] {values}")
    console.print(function_list_tree)

    console.print("之后会要求您输入想要查询的日期区间（[b red]闭区间[/b red]，统计结果包含开始和结束日期的礼物数据）")
    console.print("\n[i]下列所有问题直接回车将默认为 [b cyan]括号中[/b cyan] 结果[/i]")

    choice = Prompt.ask(
        "\n请输入[b blue]相应数字[/b blue]来使用相对应的功能：",
        choices=[str(key) for key in function_dict.keys()],
        default="4",
    )
    if choice == "0":
        live_exit()

    # 使用功能
    gift_info = getGift.GiftInfo(client)
    console.rule("[b]获取礼物信息", characters="=")
    asyncio.run(gift_info.main(choice))

    # 检测更新
    try:
        up_to_date.main("v0.8.3")
    except Exception:
        console.print("检测失败")

    # 防止快速退出
    console.input("\n\n按回车 [b blue]退出[/b blue] 程序\n")
    live_exit()
