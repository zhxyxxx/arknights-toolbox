import requests
from lxml import html
import time
import argparse
import sys
import re
import datetime

parser = argparse.ArgumentParser(description='PRTS爬取干员素材')
parser.add_argument('-s', '--star', type=int, default=5, help='想要爬取的干员星级')
parser.add_argument('-a', '--anniversary', type=float, default=None, help='爬取该周年庆往前半年的干员')
args = parser.parse_args()

star = args.star
if star < 4 or star > 6:
    print("不支持或不存在该星级的干员！")
    sys.exit(1)

if args.anniversary:
    anni = args.anniversary
    startyear = 2019
    if anni*10 % 10 == 0: # 周年
        start = datetime.date(int(startyear+anni-1), 11, 2)
        end = datetime.date(int(startyear+anni), 5, 1)
    else: # 半周年
        start = datetime.date(int(startyear+anni-0.5), 5, 2)
        end = datetime.date(int(startyear+anni-0.5), 11, 1)

page = requests.get('http://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88')
tree = html.fromstring(page.text)
data = tree.get_element_by_id('filter-data')
operators = []
for d in list(data):
    if int(d.get('data-rarity')) == star-1:
        operators.append((d.get('data-zh')))
print(f"共{len(operators)}名{star}星干员")
print(operators)

for op in operators:
    link = 'http://prts.wiki/w/' + op
    flag = True

    p = requests.get(link)
    t = html.fromstring(p.text)
    impl_time = t.xpath('//table[@class="wikitable"]/tbody/tr/td/text()')  # 实装时间

    for i in impl_time:
        l0 = re.findall(r'(\d+)年(\d+)月(\d+)日', i)
        if len(l0) == 1:
            assert len(l0[0]) == 3
            date = datetime.date(int(l0[0][0]), int(l0[0][1]), int(l0[0][2]))
            break
    if args.anniversary: # 通过实装时间筛选
        if date < start or date > end:
            flag = False

    if flag:
        d = t.xpath('//table[@class="wikitable logo"]/tbody/tr/td/div/a/@title')  # 素材
        num = t.xpath('//table[@class="wikitable logo"]/tbody/tr/td/div/span/text()')  # 数量
        if len(d) == 0:
            print(op, '读取失败或无相关数据')
            continue
        print(op, d[2], num[2], d[3], num[3], d[6], num[6], d[7], num[7], date)
    time.sleep(1)
