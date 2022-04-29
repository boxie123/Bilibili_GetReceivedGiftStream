import login
import gift_get
import time

if __name__ == '__main__':
    session = login.bzlogin()
    print("==========================================")
    print("开始获取大航海信息...")
    gift_get.generate_gift_file(session)
    print("统计结果生成完成！请查看 统计结果.txt 与 大航海统计.xls")
    time.sleep(5)
