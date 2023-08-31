import pandas as pd
import lxml
from lxml import html
import numpy as np
import pandas as pd
import requests
import time
import random

max_page = 90  # 爬取的最大页数
all_time = []  # 爬取的发表时间储存列表
all_web = []  # 爬取所有标题的网页
all_read = []  # 爬取所有阅读量
all_comment = []  # 爬取所有评论量
all_text = []  # 所有的贴吧内容
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
           Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50'}  # 构造头文件，模拟浏览器。
etree = html.etree
page_numbers = 0
# etree.HTML()可以用来解析字符串格式的HTML文档对象


for page in range(83, max_page + 1):
    # 获取网页源代码
    print('crawling the page is {}'.format(page))

    # 防止同一IP频繁访问网站被拦截
    t = random.uniform(15, 20)
    time.sleep(t)

    url = f'http://guba.eastmoney.com/list,601117_{page}.html'
    response = requests.get(url, headers=headers)
    # 解析网页源代码
    root = etree.HTML(response.text)
    text = root.xpath("//div[contains(@class,'articleh normal_post')]//span[@class='l3 a3']//a//text()")
    # contains() 获取包含xxx的元素，找到class=articleh normal_post中的span位置，然后找到span的class=l3 ，a3的位置
    # //text()转为text的形式
    datetime = root.xpath("//div[contains(@class,'articleh normal_post')]//span[@class='l5 a5']//text()")
    web = root.xpath("//div[contains(@class,'articleh normal_post')]//span[@class='l3 a3']/a/@href")
    read = root.xpath("//div[contains(@class,'articleh normal_post')]//span[@class='l1 a1']//text()")
    comment = root.xpath("//div[contains(@class,'articleh normal_post')]//span[@class='l2 a2']//text()")
    all_text += text  # 保存到总数组上
    all_time += datetime
    all_web += web
    all_read += read
    all_comment += comment
while True:
    try:
        all_text.remove('问董秘')
    except:
        break  # 去除多余的网页
# 有些网站不能直接打开需要加'http://guba.eastmoney.com'
all_web = pd.DataFrame({'web': all_web})
all_web = all_web[all_web['web'].apply(lambda x: len(x)) < 60]  # 去掉新闻
all_web = 'http://guba.eastmoney.com' + all_web
data_raw = pd.DataFrame()
data_raw['text'] = all_text
# title列全都是评论
data_raw['time'] = all_time
# time列全都是时间
data_raw['web'] = all_web
data_raw['read'] = all_read
data_raw['comment'] = all_comment
data_raw = data_raw.dropna(axis=0)
data_raw.to_excel('中国化学.xlsx', index=False)
