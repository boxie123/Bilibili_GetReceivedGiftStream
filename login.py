# -*- coding: utf-8 -*-
import http.cookiejar as cookielib
import os
import time
from io import BytesIO
from threading import Thread

import qrcode
import httpx
from PIL import Image

import agent


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
        print(e)
    loginurl = client.get(
        "https://api.bilibili.com/x/web-interface/nav", headers=headers
    ).json()
    if loginurl["code"] == 0:
        print("Cookies值有效，", loginurl["data"]["uname"], "，已登录！")
        return client, True
    else:
        print("Cookies值已经失效，请重新扫码登录！")
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
        while 1:
            qrcodedata = client.post(
                tokenurl,
                data={"oauthKey": oauthKey, "gourl": "https://www.bilibili.com/"},
                headers=headerss,
            ).json()
            print(qrcodedata)
            if "-4" in str(qrcodedata["data"]):
                print("二维码未失效，请扫码！")
            elif "-5" in str(qrcodedata["data"]):
                print("已扫码，请确认！")
            elif "-2" in str(qrcodedata["data"]):
                print("二维码已失效，请重新运行！")
            elif "True" in str(qrcodedata["status"]):
                print("已确认，登入成功！")
                client.get(qrcodedata["data"]["url"], headers=headers)
                break
            else:
                print("其他：", qrcodedata)
            time.sleep(2)
        client.cookies.jar.save()

    return client
