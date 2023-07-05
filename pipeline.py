import glob
import shutil
import os
import json
import csv
import git
import time
import pandas as pd
from utils import story, visualize

# 未实装：
# 主线剧情处理
# 干员2密录处理
# 可视化图片自动裁剪及增加水印
# 发送程序log至qq
# 自动生成文案

def send_qq(content, is_text=True):
  import win32gui
  import win32con
  import win32clipboard as w
  import io
  from PIL import Image

  if not is_text:
    img = Image.open(content)
    output = io.BytesIO()
    img.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

  time.sleep(1)
  w.OpenClipboard()
  w.EmptyClipboard()
  if is_text:
    w.SetClipboardData(win32con.CF_UNICODETEXT, content)
  else:
    w.SetClipboardData(win32con.CF_DIB, data)
  w.CloseClipboard()

  handle = win32gui.FindWindow(None, 'X-X-X')
  win32gui.SendMessage(handle, win32con.WM_PASTE, 0, 0)
  time.sleep(2)
  win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN)


while True:
  time.sleep(1800)

  import datetime
  base = datetime.time(11, 10, 0)
  dt_now = datetime.datetime.now()
  now = dt_now.time()
  if now > base:

    for jj in range(13):
      if jj > 0:
        time.sleep(1800)

      acttime = 202307
      actname = '眠于树影之中'
      acttype = 'act_om'
      code = 'act15mini'
      memory_list = ['缪尔赛思', '雪绒', '但书', '赤冬']


      git_repo= git.Repo('../ArknightsGameData')
      info = git_repo.remotes.origin.fetch()
      info = git_repo.git.pull()
      if info == 'Already up to date.':
        print('尚未更新')
        send_qq('尚未更新')
        # exit()


      # 复制剧情文件至指定文件夹
      ori_data = f'../ArknightsGameData/zh_CN/gamedata/story/activities/{code}/*.txt'
      file_list = glob.glob(ori_data)
      if len(file_list) == 0:
        print(f'不存在活动{code}')
        send_qq(f'ERROR!! 不存在活动{code}')
        # exit()
        continue
      save_dir = f'./story/activities/{actname}'
      if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
        print(f'make directory {save_dir}')
      for f in file_list:
        shutil.copy2(f, save_dir)
        print(f'copy {f} to {save_dir}')


      # 复制干员密录至指定文件夹
      memory_dir = './story/memory/new'
      old_memory_file = glob.glob(f'{memory_dir}/*.txt')
      for f in old_memory_file: # 将上次剩余的密录移出
        shutil.move(f, './story/memory/memory')
        print(f'move previous {f} to ./story/memory/memory')

      with open('../ArknightsGameData/zh_CN/gamedata/excel/character_table.json', encoding='utf-8') as dic:
        chr_dict = json.load(dic)
      chr2id = {} # 通过干员名获取id
      for k, v in chr_dict.items():
        if k.split('_')[0] == 'char':
          chr2id[v['name']] = k.split('_')[-1]

      ori_memory_data = '../ArknightsGameData/zh_CN/gamedata/story/obt/memory'
      memory_file_list = []
      for chr in memory_list:
        memory_file_list.extend(glob.glob(f'{ori_memory_data}/story_{chr2id[chr]}_*_*.txt'))
      for f in memory_file_list: # 复制新密录
        shutil.copy2(f, './story/memory/new')
        print(f'copy {f} to ./story/memory/new')


      # 计算字数、写入csv、可视化
      count = story.sum_words_in_dir(save_dir)
      count_memory = story.sum_words_in_dir('./story/memory/new')
      print(f'活动 {actname} 字数 {count}')
      print(f'干员密录 字数 {count_memory}')
      send_qq(f'活动 {actname} 字数 {count}，干员密录 字数 {count_memory}')

      with open('./data/event.csv', mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        id = l[-1][0]
      with open('./data/event.csv', mode='a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([int(id)+1, actname, count, acttime, acttype])
        print(f'write {[int(id)+1, actname, count, acttime, acttype]} to ./data/event.csv')

      df = pd.read_csv('data/event.csv')
      fig = visualize.plot_h(df, False)
      df_part = visualize.extract_type(df, acttype)
      fig_part = visualize.plot_v(df_part, False)
      fig_table = visualize.plot_table(df, actname, False)
      fig.write_image(f'./data/full_{acttime}.png', engine='kaleido')
      fig_part.write_image(f'./data/{acttype}_{acttime}.png', engine='kaleido')
      fig_table.write_image(f'./data/table_{acttime}.png', engine='kaleido')
      print(f'plot full_{acttime}.png, {acttype}_{acttime}.png, table_{acttime}.png to ./data')

      send_qq(f'./data/full_{acttime}.png', False)
      send_qq(f'./data/{acttype}_{acttime}.png', False)
      send_qq(f'./data/table_{acttime}.png', False)

    send_qq('程序已停止')
    exit()
