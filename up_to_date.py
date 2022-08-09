import httpx


def main(now_tag):
    print("\n\n开始检测更新")
    header = {"accept": "application/vnd.github.v3+json"}
    url = "https://api.github.com/repos/boxie123/Bilibili_GetReceivedGiftStream/releases"
    param = {"per_page": 1, "page": 1}
    releases_info = httpx.get(url, headers=header, params=param).json()
    tag_name = releases_info[0]["tag_name"]
    if tag_name == now_tag:
        print("提示：当前已是最新版本")
    else:
        new_html_url = releases_info[0]["html_url"]
        print("提示：检测到更新，当前版本{}，最新版本{}".format(now_tag, tag_name))
        print("请复制以下链接到浏览器下载最新版本：{}".format(new_html_url))
