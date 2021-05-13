import requests
from lxml import html
import time
import argparse
import sys

parser = argparse.ArgumentParser(description='PRTS爬取干员素材')
parser.add_argument('-s', '--star', type=int, default=5, help='想要爬取的干员星级')
args = parser.parse_args()

star = args.star
if star < 4 or star > 6:
    print("不支持或不存在该星级的干员！")
    sys.exit(1)

page = requests.get('http://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88')
tree = html.fromstring(page.text)
data = tree.xpath(f'//div[@class="smwdata" and @data-rarity="{star-1}"]/@data-cn')
print(f"共{len(data)}名{star}星干员")
print(data)

for op in data:
    link = 'http://prts.wiki/w/' + op

    p = requests.get(link)
    t = html.fromstring(p.text)
    d = t.xpath('//table[@class="wikitable logo"]/tbody/tr/td/div/a/@title')  # 素材
    num = t.xpath('//table[@class="wikitable logo"]/tbody/tr/td/div/span/text()')  # 数量
    if len(d) == 0:
        continue
    print(op, d[2], num[2], d[3], num[3], d[6], num[6], d[7], num[7])
    time.sleep(1)

'''
# execl计算公式
for i in range(len(data)):
    print(f"=VLOOKUP(B{i+2},N2:O40,2,0)*C{i+2}+VLOOKUP(D{i+2},N2:O40,2,0)*E{i+2}+VLOOKUP(F{i+2},N2:O40,2,0)*G{i+2}+VLOOKUP(H{i+2},N2:O40,2,0)*I{i+2}")
'''
