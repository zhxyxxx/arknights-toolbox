import glob
import shutil
import os
import json
import csv
import git
import time
import pandas as pd
from utils import story, visualize, win, utils

# 主线格式：章节号_名字

# 未实装：
# 发送程序log至qq
# 自动生成文案
# 重复执行


for jj in range(24):
    if jj > 0:
        time.sleep(900)


    acttime = 202311
    actname = "崔林特尔梅之金"
    acttype = "act_ss"  # main, act_ss, act_om
    memory_list = ["塑心", "早露", "折光", "车尔尼", "寒檀", "暮落"]


    # 更新github
    git_repo = git.Repo("../ArknightsGameData")
    info = git_repo.remotes.origin.fetch()
    info = git_repo.git.pull()
    if info == "Already up to date.":
        print("尚未更新")
        win.send_qq("尚未更新")
    else:
        print(info)


    # 复制剧情文件至指定文件夹
    if acttype == "main":
        chapter = int(actname.split("_")[0])
        ori_data = f"../ArknightsGameData/zh_CN/gamedata/story/obt/main/*_{chapter:02}-*.txt"
        record_data = f"../ArknightsGameData/zh_CN/gamedata/story/obt/record/main_{chapter:02}/*.txt"
        file_list = glob.glob(ori_data)
        story_count = [len(file_list), 0]
        record_list = glob.glob(record_data)
        file_list.extend(record_list)
        save_dir = f"./story/main/{actname}"
        story_count[1] = len(record_list)
        if len(file_list) == 0 or len(file_list) == len(record_list):
            print(f"尚未更新 {actname}")
            win.send_qq(f"ERROR!! 尚未更新 {actname}")
            continue
    elif acttype == "act_ss" or acttype == "act_om":
        with open("../ArknightsGameData/zh_CN/gamedata/excel/activity_table.json", encoding="utf-8") as dic:
            act_dict = json.load(dic)
        act2id = {}  # 通过活动名获取id
        for k, v in act_dict["basicInfo"].items():
            act2id[v["name"]] = k
        if actname not in act2id:
            print(f"未找到活动 {actname}")
            win.send_qq(f"ERROR!! 未找到活动 {actname}")
            continue
        else:
            code = act2id[actname]
        ori_data = f"../ArknightsGameData/zh_CN/gamedata/story/activities/{code}/*.txt"
        file_list = glob.glob(ori_data)
        save_dir = f"./story/activities/{actname}"
        story_count = len(file_list)
        for f in file_list:
            if 'entry' in f:
                story_count -= 1
                break
    else:
        print(f"ERROR!! 错误的活动类型 {acttype}")
        break

    if len(file_list) == 0:
        print(f"不存在活动文件 {code}")
        win.send_qq(f"ERROR!! 不存在活动文件 {code}")
        continue
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
        print(f"make directory {save_dir}")
    else:
        print(f"WARNING!! 已存在活动 {actname}")
    for f in file_list:
        shutil.copy2(f, save_dir)
        print(f"copy {f} to {save_dir}")


    # 复制干员密录至指定文件夹
    memory_dir = "./story/memory/new"
    old_memory_file = glob.glob(f"{memory_dir}/*.txt")
    for f in old_memory_file:  # 将上次剩余的密录移出
        shutil.move(f, "./story/memory/memory")
        print(f"move previous {f} to ./story/memory/memory")

    with open("../ArknightsGameData/zh_CN/gamedata/excel/character_table.json", encoding="utf-8") as dic:
        chr_dict = json.load(dic)
    chr2id = {}  # 通过干员名获取id
    for k, v in chr_dict.items():
        if k.split("_")[0] == "char" and not v['isNotObtainable']:
            chr2id[v["name"]] = k.split("_")[-1]

    existed_memory_file = glob.glob("./story/memory/memory/*.txt")
    existed_memory_file = list(map(lambda x: x.split("/")[-1], existed_memory_file))
    ori_memory_data = "../ArknightsGameData/zh_CN/gamedata/story/obt/memory"
    memory_file_list = []
    for chr in memory_list:
        memory_file = glob.glob(f"{ori_memory_data}/story_{chr2id[chr]}_*_*.txt")
        for f in memory_file:
            if f.split("/")[-1] not in existed_memory_file:
                memory_file_list.append(f)
    for f in memory_file_list:  # 复制新密录
        shutil.copy2(f, "./story/memory/new")
        print(f"copy {f} to ./story/memory/new")
    memory_count = len(memory_file_list)


    # 计算字数、写入csv、可视化
    count = story.sum_words_in_dir(save_dir)
    count_memory = story.sum_words_in_dir("./story/memory/new")
    print(f"活动 {actname} 字数 {count} 共{story_count}篇")
    print(f"干员密录 字数 {count_memory} 共{memory_count}篇")
    win.send_qq(f"活动 {actname} 字数 {count} 共{story_count}篇，干员密录 字数 {count_memory} 共{memory_count}篇")

    with open("./data/event.csv", mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        id = l[-1][0]
        existed_act = [i[1] for i in l[1:]]
    if actname in existed_act:
        print(f"WARNING!! 已记录活动 {actname}，跳过记录")
        break
    else:
        with open("./data/event.csv", mode="a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([int(id) + 1, actname, count, acttime, acttype])
            print(f"write {[int(id)+1, actname, count, acttime, acttype]} to ./data/event.csv")

    df = pd.read_csv("data/event.csv")
    fig = visualize.plot_h(df, False)
    df_part = visualize.extract_type(df, acttype)
    fig_part = visualize.plot_v(df_part, False)
    if acttype == 'main':
        actname = f'EP{actname}'
    fig_table = visualize.plot_table(df, actname, False)
    fig_path = utils.solve_filename(f'full_{acttime}.png')
    fig_table_path = utils.solve_filename(f'table_{acttime}.png')
    fig_part_path = utils.solve_filename(f'{acttype}_{acttime}.png')
    fig.write_image(fig_path, engine="kaleido")
    fig_part.write_image(fig_part_path, engine="kaleido")
    fig_table.write_image(fig_table_path, engine="kaleido")
    print(f'plot {fig_path.split("/")[-1]}, {fig_part_path.split("/")[-1]}, {fig_table_path.split("/")[-1]} to ./data')

    fig = visualize.crop_img(fig_path)
    fig_part = visualize.crop_img(fig_part_path)
    fig_table = visualize.crop_img(fig_table_path)
    visualize.watermark(fig, x=fig.size[0]-300, y=50, output_path=fig_path)
    visualize.watermark(fig_part, x=75, y=50, output_path=fig_part_path)

    win.send_qq(fig_path, False)
    win.send_qq(fig_part_path, False)
    win.send_qq(fig_table_path, False)

    break

win.send_qq("程序已停止")
exit()
