import re
from time import sleep
import requests
from lxml import etree
import random
import csv

def main(page, f):
    url = f'https://movie.douban.com/top250?start={page * 25}&filter='
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.35 Safari/537.36', }

    # 发送HTTP GET请求，获取页面内容。
    resp = requests.get(url, headers=headers)
    html = resp.text
    # 解析返回的HTML内容。
    tree = etree.HTML(html)

    # 获取详情页的链接列表
    href_list = tree.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/@href')
    # 获取电影名称列表
    name_list = tree.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')

    for url, name in zip(href_list, name_list):
        # zip():将两个或多个可迭代对象（如列表、元组等）生成一个元组的列表，第i个元组包含每个参数序列的第i个元素。
        f.flush()                      # 刷新文件缓冲区，将数据写入文件。
        try:
            get_info(url, name)        # 获取详情页的信息
        except:
            pass                       # 如果发生异常，忽略错误继续执行。
        sleep(1 + random.random())     # 休息，随机延迟一段时间，避免被反爬虫机制检测
    print(f'第{i + 1}页爬取完毕')
    csvwriter.writerow('该页爬取完毕')

# 获取详情页的信息
def get_info(url, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.35 Safari/537.36',
        # 使用 User-Agent 头部可以伪装爬虫，避免被一些网站检测到爬虫活动并阻止访问
        'Host': 'movie.douban.com',
        # 请求的目标主机
    }

    # 发送HTTP GET请求，获取页面内容。
    # 解析返回的HTML内容。
    resp = requests.get(url, headers=headers)
    html = resp.text
    tree = etree.HTML(html)

    # 导演
    dir = tree.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]      # [0]:用于从返回的列表中获取第一个元素。
    # 电影类型
    type_ = re.findall(r'property="v:genre">(.*?)</span>', html)  # html 是一个包含完整网页内容的字符串。正则表达式需要在整个 HTML 文本中搜索匹配项
    type_ = '/'.join(type_)
    # 国家
    country = re.findall(r'地区:</span> (.*?)<br', html)[0]
    # 上映时间
    time = tree.xpath('//*[@id="content"]/h1/span[2]/text()')[0]
    time = time[1:5]
    # 评分
    rate = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
    # 打印结果，使用ljust设置宽度
    print(name.ljust(10), dir.ljust(10), type_.ljust(15), country.ljust(8), time.ljust(5), rate.ljust(5))
    # 保存到文件中，使用固定宽度对齐
    csvwriter.writerow((name.ljust(10), dir.ljust(10), type_.ljust(10), country.ljust(8), time.ljust(4), rate.ljust(5)))

if __name__ == '__main__':
    # 创建movie-xpath.csv文件,以追加模式保存数据
    with open('movie-xpath.csv', 'a', encoding='utf-8', newline='') as f:
        # 创建CSV写入器对象
        csvwriter = csv.writer(f)
        # 写入表头标题
        csvwriter.writerow(('电影名称      ', '导演        ', '电影类型      ', '国家      ', '上映年份', '评分'))
        csvwriter.writerow(' ')        # 空行
        for i in range(3):             # 爬取3页
            main(i, f)                 # 调用主函数
            sleep(1 + random.random())