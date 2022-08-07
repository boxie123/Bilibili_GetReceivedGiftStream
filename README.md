[![Bilibili_GetReceivedGiftStream](https://socialify.git.ci/boxie123/Bilibili_GetReceivedGiftStream/image?description=1&descriptionEditable=%E8%8E%B7%E5%8F%96bilibili%E7%A4%BC%E7%89%A9%E6%B5%81%E6%B0%B4%E7%BB%9F%E8%AE%A1%E8%A1%A8%E6%A0%BC&font=Source%20Code%20Pro&forks=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2Fboxie123%2FBilibili_GetReceivedGiftStream%2Fmain%2Fimages%2FBGRGS.png&name=1&pattern=Circuit%20Board&stargazers=1&theme=Dark)](https://boxie123.github.io/Bilibili-GetReceivedGiftStream/)

# Bilibili_GetReceivedGiftStream

 登录并获取bilibili账号某段时间礼物流水数据，生成表格。

[![qq group](https://img.shields.io/badge/QQ%E7%BE%A4-1054608979-hotpink)](https://jq.qq.com/?_wv=1027&k=mEy0fIIq)

## 功能列表

1. 统计指定时间段的大航海记录（开通时间，用户名，uid），附表生成各大航海数量与总积分（xls格式）

1. 统计指定时间段的大航海记录（用户，uid，大航海类型）。生成可直接导入BiliMessenger使用的数据列表（csv格式）

1. 生成指定时间段收到所有礼物流水列表（用户，uid，礼物名，电池数），附表为（用户，uid，礼物名，数量）（xls格式）

1. 同时生成上述三个文件

*********************************

## 注意事项

1. 由于本api仅提供**近180天**的数据，超出范围的数据均为0，请勿使用本程序查询过于久远的记录，防止造成误导。

1. 本程序会自动生成数个文件，分别为

    - `bzcookies.txt`

    - `yyyy年mm月nn日至yyyy年mm月nn日礼物统计(大航海).xls/csv` 

    - `yyyy年mm月nn日至yyyy年mm月nn日礼物统计.xls`

    请确保运行本程序前，当前文件夹中**无同名文件**，否则会直接覆盖造成数据损失。

> **其中 `bzcookies.txt` 为重要账号登录信息，请谨慎保管、切勿泄漏，否则可能导致账号被盗用等后果。**

****************************************

开发者：[铂屑](https://github.com/boxie123)、[hyt658](https://github.com/hyt658)

开发思路：详见[《Bilibili GetReceivedGiftStream》](https://boxie123.github.io/Bilibili-GetReceivedGiftStream/)

————致 [@艾鸽泰尔德](https://space.bilibili.com/1485569) ，希望可爱的鸽宝统计礼物不再辛苦。
