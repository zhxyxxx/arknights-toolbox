# 泛用处理
import os
import pandas as pd


def solve_filename(filename, dir='./data'):
    # 处理重复文件名
    ''' args
    filename: 目标文件名（包含扩展名）
    dir: 目标文件夹

    return
    filename: 不重复的目标文件名
    '''
    existed = os.listdir(dir)

    target, ext = os.path.splitext(filename)
    if filename in existed:
        cnt = 2
        while True:
            if f'{target}_{cnt}{ext}' in existed:
                cnt += 1
            else:
                break
        return f'{dir}/{target}_{cnt}{ext}'
    else:
        return f'{dir}/{filename}'
    

def get_act_count(actname):
    # 获取指定活动的字数
    ''' args
    actname: 活动名

    return
    count: 对应文字数
    '''
    df = pd.read_csv("data/event.csv")
    count = df[df['sname'] == actname]['charnum'].item()
    return int(count)


def round_005(x):
    # 小数点后第二位近似至0/5
    ''' args
    x: 数字

    return
    x: 近似后的值
    '''
    x = int(x * 100)
    tail = x % 10
    if tail >= 0 and tail <= 2:
        x = (x - tail) / 100
    elif tail >= 3 and tail <= 7:
        x = (x - tail + 5) / 100
    elif tail >= 8 and tail <= 9:
        x = (x - tail + 10) / 100
    return x


TEMPLATE_SS = '#明日方舟# 剧情文本量速览\n\
SideStory「#{}#」内含主要剧情{}段，总计约{:.1f}万字，剧情长度与「{}」相近，约等于{}个「{}」。\n\
另外本次更新新增{}共{}篇干员密录，总计约{:.1f}万字。'

TEMPLATE_MAIN = '#明日方舟# 剧情文本量速览\n\
主题曲{}「#{}#」内含主要剧情{}段，以及「{}」内的{}段剧情，总计约{:.1f}万字，剧情长度与{}「{}」相当，约等于{}个「{}」。\n\
另外本次更新新增{}共{}篇干员密录，总计约{:.1f}万字。'

TEMPLATE_OM = '#明日方舟# 剧情文本量速览\n\
故事集「#{}#」内含剧情{}段，总计约{:.1f}万字，与「{}」长度相近。\n\
另外本次更新新增{}共{}篇干员密录，总计约{:.1f}万字。'
