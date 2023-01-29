import httpx

from .console import console


def main(now_tag):
    console.print("\n\n")
    console.rule("检测更新")
    header = {"accept": "application/vnd.github.v3+json"}
    url = (
        "https://api.github.com/repos/boxie123/Bilibili_GetReceivedGiftStream/releases"
    )
    param = {"per_page": 1, "page": 1}
    with console.status("正在检测更新（此步骤不影响上述已生成的文件，若无需检测可直接关闭程序）", spinner="line"):
        releases_info = httpx.get(
            url, headers=header, params=param, timeout=None, verify=False
        ).json()
        tag_name = releases_info[0]["tag_name"]
        if tag_name == now_tag:
            console.print("提示：当前已是最新版本")
        else:
            new_html_url = releases_info[0]["html_url"]
            console.print(
                "提示：检测到更新，当前版本[blue]{}[/blue]，最新版本[green]{}[/green]".format(
                    now_tag, tag_name
                )
            )
            console.print("\n可点击下面的链接到浏览器下载最新版本：")
            console.print(new_html_url, style=f"link {new_html_url}")


# if __name__ == "__main__":
#     main("v0.7.0")
