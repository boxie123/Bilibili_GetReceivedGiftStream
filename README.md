[![Bilibili_GetReceivedGiftStream](https://socialify.git.ci/boxie123/Bilibili_GetReceivedGiftStream/image?description=1&descriptionEditable=%E8%8E%B7%E5%8F%96bilibili%E7%A4%BC%E7%89%A9%E6%B5%81%E6%B0%B4%E7%BB%9F%E8%AE%A1%E8%A1%A8%E6%A0%BC&font=Source%20Code%20Pro&forks=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2Fboxie123%2FBilibili_GetReceivedGiftStream%2Fmain%2Fimages%2FBGRGS.png&name=1&pattern=Circuit%20Board&stargazers=1&theme=Dark)](https://boxie123.github.io/Bilibili-GetReceivedGiftStream/)

<div align="center">

# Bilibili_GetReceivedGiftStream

 登录并获取bilibili账号某段时间礼物流水数据，生成表格。

![GitHub](https://img.shields.io/github/license/boxie123/Bilibili_GetReceivedGiftStream)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/boxie123/Bilibili_GetReceivedGiftStream?include_prereleases)

[![qq group](https://img.shields.io/badge/QQ%E7%BE%A4-1054608979-hotpink)](https://jq.qq.com/?_wv=1027&k=mEy0fIIq)

</div>

## 功能列表

1. 统计指定时间段的大航海记录（开通时间，用户名，uid），附表生成各大航海数量与总积分（xlsx格式）

    例表：

    表1：上舰时间

    | ID   | UID      | 舰长              | 提督 | 总督 |
    | ---- | -------- | ------------------- | ---- | ---- |
    | 铂屑 | 35192025 | 2022-04-29 09:24:39 |      |      |

    表2：积分计算

    | ID   | UID      | 总积分 | 舰长 | 提督 | 总督 |
    | ---- | -------- | ------ | ---- | ---- | ---- |
    | 铂屑 | 35192025 | 1      | 1    | 0    | 0    |

2. 统计指定时间段的大航海记录（用户，uid，大航海类型）。生成可直接导入 [BiliMessenger](https://github.com/Xinrea/BiliMessengerElectron)（私信群发助手）使用的数据列表（csv格式）

3. 生成指定时间段收到所有礼物流水列表（用户，uid，礼物名，电池数），附表为（用户，uid，礼物名，数量）（xlsx格式）
   
   例表：

   表1：电池数量

    | ID     | UID      | 小花花(id:31036) | 辣条(id:1) | 这个好诶(id:31213) | 舰长(id:10003) | SUM  |
    | ------ | -------- | ---------------- | ---------- | ------------------ | -------------- | ---- |
    | hyt658 | 23262005 | 5                | 0          | 10                 |                | 15   |
    | 铂屑 | 35192025 |                  |            |                    | 1380           | 1380 |

    表2：数目

    | ID     | UID      | 小花花(id:31036) | 辣条(id:1) | 这个好诶(id:31213) | 舰长(id:10003) |
    | ------ | -------- | ---------------- | ---------- | ------------------ | -------------- |
    | hyt658 | 23262005 | 5                | 2          | 1                  |                |
    | 铂屑 | 35192025 |                  |            |                    | 1              |


4. 同时生成上述三个文件

*********************************

## 注意事项

1. 由于本api仅提供**近180天**的数据，超出范围的数据均为0，请勿使用本程序查询过于久远的记录，防止造成误导。

1. 本程序会自动生成数个文件，分别为

    - `bzcookies`

    - `yyyy年mm月nn日至yyyy年mm月nn日礼物统计(大航海).xlsx/csv` 

    - `yyyy年mm月nn日至yyyy年mm月nn日礼物统计.xlsx`

    请确保运行本程序前，当前文件夹中**无同名文件**，否则会直接覆盖造成数据损失。

> **其中 `bzcookies` 为重要账号登录信息，请谨慎保管、切勿泄漏，否则可能导致账号被盗用等后果。**

****************************************

## 使用方法

### 方法一：下载打包好的程序（推荐）

下载最新的 [Release](https://github.com/boxie123/Bilibili_GetReceivedGiftStream/releases) 中的 `.exe` 文件，双击运行。

Demo：

![Demo](images/Demo.png)

### 方法二：手动构建

> 需使用 [git](https://git-scm.com/)、[pdm](https://github.com/pdm-project/pdm)、[python](https://www.python.org/) 等，不建议小白手动构建。

#### 克隆Git仓库：

```sh
git clone https://github.com/boxie123/Bilibili_GetReceivedGiftStream.git
cd Bilibili_GetReceivedGiftStream
```

#### 构建虚拟环境：

使用 [pdm](https://github.com/pdm-project/pdm)：

```sh
pdm install --prod
```

#### 运行：

```sh
pdm run python main.py
```

************************************

## Q & A

Q: 程序闪退？

A: 大概率是网络问题导致爬取过程中链接超时。

--------------------------------------

Q: 大航海表格可以生成，但礼物表格生成失败？

A: 0.7.0及以下版本使用 xls 的 `SUM` 求和公式，但 xls 为 Excel 2007 之前的版本，求和公式最大参数限制为30个，
目前已弃用 xls 改用 xlsx ，请及时更新至0.8.0及以上版本。

----------------------------------------

若排除以上原因后仍然闪退，请打开 CMD 窗口手动运行程序，带着**报错信息**来提 [Issues](https://github.com/boxie123/Bilibili_GetReceivedGiftStream/issues) 吧！

## 支持与贡献

觉得好用可以给这个项目点个 Star 或者去关注非常可爱的 [艾鸽泰尔德](https://space.bilibili.com/1485569)。

有意见或者建议也欢迎提交 [Issues](https://github.com/boxie123/Bilibili_GetReceivedGiftStream/issues) 和 [Pull requests](https://github.com/boxie123/Bilibili_GetReceivedGiftStream/pulls)。

**************************************

开发者：[铂屑](https://github.com/boxie123)、[hyt658](https://github.com/hyt658)

开发思路：详见[《Bilibili GetReceivedGiftStream》](https://boxie123.github.io/Bilibili-GetReceivedGiftStream/)。
~~在写了再写了（目移）~~

————致 [@艾鸽泰尔德](https://space.bilibili.com/1485569) ，希望可爱的鸽宝统计礼物不再辛苦。
