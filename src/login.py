import http.cookiejar as cookielib
import json
import os
import tempfile
import tkinter
import tkinter.font

import httpx
import qrcode
from PIL.ImageTk import PhotoImage

from . import agent
from .console import console

API = {
    "qrcode": {
        "get_qrcode_and_token": {
            "url": "https://passport.bilibili.com/x/passport-login/web/qrcode/generate",
            "method": "GET",
            "verify": False,
            "comment": "请求二维码及登录密钥",
        },
        "get_events": {
            "url": "https://passport.bilibili.com/x/passport-login/web/qrcode/poll",
            "method": "GET",
            "verify": False,
            "data": {"qrcode_key": "str: 登陆密钥"},
            "comment": "获取最新信息",
        },
    }
}

headers = {
    "User-Agent": agent.get_user_agents(),
    "Referer": "https://www.bilibili.com/",
}
headerss = {
    "User-Agent": agent.get_user_agents(),
    "Host": "passport.bilibili.com",
    "Referer": "https://passport.bilibili.com/login",
}

# ----------------------------------------------------------------
# 二维码登录
# ----------------------------------------------------------------

photo = None  # 图片的全局变量
client = httpx.Client(verify=False)
login_key = ""
qrcode_image = None
is_destroy = False
id_ = 0  # 事件 id,用于取消 after 绑定


def islogin():
    """检查登陆是否有效

    Returns:
        client: httpx.Client
    """
    global client
    try:
        client.cookies.jar.load(ignore_discard=True)
    except Exception:
        console.print("[b green]bzcookies[/b green] 载入失败")
    loginurl = client.get(
        "https://api.bilibili.com/x/web-interface/nav", headers=headers
    ).json()
    if loginurl["code"] == 0:
        console.print(
            "Cookies值有效，[b blue]{}[/b blue]，已登录！".format(loginurl["data"]["uname"])
        )
        return client, True
    else:
        console.print("Cookies值已经失效，[blue]已弹出二维码[/blue]，请重新扫码登录！")
        return client, False


def make_qrcode(url) -> str:
    qr = qrcode.QRCode()
    qr.add_data(url)
    img = qr.make_image()
    img.save(os.path.join(tempfile.gettempdir(), "qrcode.png"))
    return os.path.join(tempfile.gettempdir(), "qrcode.png")


def login_with_qrcode():
    """通过二维码登陆

    Raises:
        Exception: 登陆失败
    """

    global photo
    global login_key, qrcode_image
    global id_
    global client

    root = tkinter.Tk()
    root.title("扫码登录")
    qrcode_image = update_qrcode()
    photo = PhotoImage(file=qrcode_image)
    qrcode_label = tkinter.Label(root, image=photo, width=500, height=500)
    qrcode_label.pack()
    big_font = tkinter.font.Font(root, size=25)
    log = tkinter.Label(root, text="二维码未失效，请扫码！", font=big_font, fg="red")
    log.pack()

    def update_events():
        global id_
        global is_destroy, client
        events_api = API["qrcode"]["get_events"]
        try:
            events = client.get(
                events_api["url"],
                params={"qrcode_key": login_key},
                headers=headerss,
            ).json()
        except json.decoder.JSONDecodeError:
            console.print("[b green]更新状态失败[/b green] 正在重试")
            id_ = root.after(500, update_events)
            root.update()
            return
        if "code" in events.keys() and events["code"] == -412:
            raise Exception(events["message"])
        if events["data"]["code"] == 86101:
            log.configure(text="二维码未失效，请扫码！", fg="red", font=big_font)
        elif events["data"]["code"] == 86090:
            log.configure(text="已扫码，请确认！", fg="orange", font=big_font)
        elif events["data"]["code"] == 86038:
            update_qrcode()
            log.configure(text="二维码已刷新，请重新扫码", fg="blue", font=big_font)
        elif isinstance(events["data"], dict):
            url = events["data"]["url"]
            client.get(url, headers=headers)
            client.cookies.jar.save()

            log.configure(text="登入成功！", fg="green", font=big_font)

            root.after(2000, destroy)
        id_ = root.after(2000, update_events)
        root.update()

    def destroy():
        global id_
        root.after_cancel(id_)  # type: ignore
        root.destroy()

    root.after(500, update_events)
    root.mainloop()
    root.after_cancel(id_)  # type: ignore


def update_qrcode() -> str:
    """更新二维码

    Returns:
        str: 二维码
    """
    global login_key, qrcode_image, client
    api = API["qrcode"]["get_qrcode_and_token"]
    qrcode_login_data = json.loads(client.get(api["url"], headers=headers).text)["data"]
    login_key = qrcode_login_data["qrcode_key"]
    qrcode = qrcode_login_data["url"]
    qrcode_image = make_qrcode(qrcode)
    return qrcode_image


def main():
    global client

    nowdir = os.getcwd()
    result_file = os.path.join(nowdir, "bzcookies")
    if not os.path.exists(result_file):
        try:
            with open(result_file, "w") as f:
                f.write("")
        except PermissionError as e:
            console.print("当前所在文件夹无写入权限，请将本程序移至其他文件夹再打开")
            console.print(e)
            console.input("\n按回车退出程序")
    client.cookies = cookielib.LWPCookieJar(filename=result_file)
    while True:
        client, status = islogin()
        if not status:
            login_with_qrcode()
        if status:
            return client


# if __name__ == "__main__":
#     main()
