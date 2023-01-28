# -*- coding: utf-8 -*-
import http.cookiejar as cookielib
import os
import time
from io import BytesIO
from threading import Thread

import qrcode
import httpx
from PIL import Image
from rich.live import Live

import agent
from console import console


headers = {
    "User-Agent": agent.get_user_agents(),
    "Referer": "https://www.bilibili.com/",
}
headerss = {
    "User-Agent": agent.get_user_agents(),
    "Host": "passport.bilibili.com",
    "Referer": "https://passport.bilibili.com/login",
}


class showpng(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(BytesIO(self.data))
        img.show()


def islogin(client):
    try:
        client.cookies.jar.load(ignore_discard=True)
    except Exception as e:
        console.print(e)
    loginurl = client.get(
        "https://api.bilibili.com/x/web-interface/nav", headers=headers
    ).json()
    if loginurl["code"] == 0:
        console.print(
            "Cookies值有效，[b blue]{}[/b blue]，已登录！".format(loginurl["data"]["uname"])
        )
        return client, True
    else:
        console.print("Cookies值已经失效，[blue]已使用默认图片打开方式弹出二维码[/blue]，请重新扫码登录！")
        return client, False


def bzlogin():
    nowdir = os.getcwd()
    result_file = os.path.join(nowdir, "bzcookies.txt")
    if not os.path.exists(result_file):
        with open(result_file, "w") as f:
            f.write("")
    client = httpx.Client(verify=False)
    client.cookies = cookielib.LWPCookieJar(filename=result_file)
    client, status = islogin(client)
    if not status:
        getlogin = client.get(
            "https://passport.bilibili.com/qrcode/getLoginUrl", headers=headers
        ).json()
        loginurl = httpx.get(getlogin["data"]["url"], headers=headers).url
        oauthKey = getlogin["data"]["oauthKey"]
        qr = qrcode.QRCode()
        qr.add_data(loginurl)
        img = qr.make_image()
        a = BytesIO()
        img.save(a, "png")
        png = a.getvalue()
        a.close()
        t = showpng(png)
        t.start()
        tokenurl = "https://passport.bilibili.com/qrcode/getLoginInfo"
        status_qrcode = ""
        with Live(
            f"二维码状态为：[b green]{status_qrcode}[/b green]",
            console=console,
            refresh_per_second=2,
        ) as live:
            while 1:
                qrcodedata = client.post(
                    tokenurl,
                    data={"oauthKey": oauthKey, "gourl": "https://www.bilibili.com/"},
                    headers=headerss,
                ).json()
                # console.print(qrcodedata)
                if "-4" in str(qrcodedata["data"]):
                    status_qrcode = "二维码未失效，请扫码！"
                elif "-5" in str(qrcodedata["data"]):
                    status_qrcode = "已扫码，请确认！"
                elif "-2" in str(qrcodedata["data"]):
                    status_qrcode = "二维码已失效，请重新运行！"
                elif "True" in str(qrcodedata["status"]):
                    status_qrcode = "已确认，登入成功！"
                    client.get(qrcodedata["data"]["url"], headers=headers)
                    break
                else:
                    console.print("其他：", qrcodedata)

                live.update(f"二维码状态为：[b green]{status_qrcode}[/b green]")
                time.sleep(2)

        client.cookies.jar.save()

    return client
