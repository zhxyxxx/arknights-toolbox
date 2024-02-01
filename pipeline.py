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

logger = utils.set_logger()

acttime = 202402
actname = "怀黍离"
acttype = "act_ss"  # main, act_ss, act_om
memory_list = ["黍", "仇白", "铎铃", "崖心"]

king = '孤星'
limit_hour = 1 # 最长执行时间(h)
internal_minute = 15 # 每次执行间隔(min)
wait_start_hour = 0 # 执行开始前等待时间(h)

#####################################################

exec_time = 0

time.sleep(wait_start_hour * 60 * 60)
logger.info('=====开始执行程序=====')
win.send_qq('=====开始执行程序=====', logger, 'text')

try:
    while True:
        if exec_time > limit_hour * 60 * 60:
            break
        if exec_time > 0:
            time.sleep(internal_minute * 60)
        exec_time += internal_minute * 60


        # 更新github
        git_repo = git.Repo("../ArknightsGameData")
        info = git_repo.remotes.origin.fetch()
        info = git_repo.git.pull()
        if info == "Already up to date.":
            logger.info('github未发现新内容')
        else:
            logger.info('github已更新')


        # 复制剧情文件至指定文件夹
        if acttype == "main":
            chapter = int(actname.split("_")[0])
            ori_data = f"../ArknightsGameData/zh_CN/gamedata/story/obt/main/*_{chapter:02}-*.txt"
            # record_data = f"../ArknightsGameData/zh_CN/gamedata/story/obt/record/main_{chapter:02}/*.txt"
            file_list = glob.glob(ori_data)
            story_count = len(file_list)
            save_dir = f"./story/main/{actname}"
            if len(file_list) == 0:
                logger.warning(f"未找到活动文件 {actname}")
                win.send_qq(f"尚未更新 {actname}", logger, 'text')
                continue
        elif acttype == "act_ss" or acttype == "act_om":
            with open("../ArknightsGameData/zh_CN/gamedata/excel/activity_table.json", encoding="utf-8") as dic:
                act_dict = json.load(dic)
            act2id = {}  # 通过活动名获取id
            for k, v in act_dict["basicInfo"].items():
                act2id[v["name"]] = k
            if actname not in act2id:
                logger.warning(f'未找到活动名 {actname}')
                win.send_qq(f"尚未更新 {actname}", logger, 'text')
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
            if len(file_list) == 0:
                logger.warning(f"未找到活动文件 {code}")
                win.send_qq(f"尚未更新 {code}", logger, 'text')
                continue
        else:
            logger.error(f"错误的活动类型 {acttype}")
            break


        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
            logger.debug(f"make directory {save_dir}")
        else:
            logger.warning(f"已存在活动文件夹 {actname}")
        for f in file_list:
            shutil.copy2(f, save_dir)
            logger.debug(f"copy {f} to {save_dir}")


        # 复制干员密录至指定文件夹
        memory_dir = "./story/memory/new"
        old_memory_file = glob.glob(f"{memory_dir}/*.txt")
        for f in old_memory_file:  # 将上次剩余的密录移出
            shutil.move(f, "./story/memory/memory")
            logger.debug(f"move previous {f} to ./story/memory/memory")

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
            if chr not in chr2id:
                logger.error(f'未找到干员 {chr}')
                continue
            memory_file = glob.glob(f"{ori_memory_data}/story_{chr2id[chr]}_*_*.txt")
            for f in memory_file:
                if f.split("/")[-1] not in existed_memory_file:
                    memory_file_list.append(f)
        for f in memory_file_list:  # 复制新密录
            shutil.copy2(f, "./story/memory/new")
            logger.debug(f"copy {f} to ./story/memory/new")
        memory_count = len(memory_file_list)


        # 计算字数、写入csv、可视化
        count = story.sum_words_in_dir(save_dir)
        count_memory = story.sum_words_in_dir(memory_dir)
        logger.info(f"活动 {actname} 字数 {count} 共{story_count}篇，干员密录 字数 {count_memory} 共{memory_count}篇")

        with open("./data/event.csv", mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            l = [row for row in reader]
            id = l[-1][0]
            existed_act = [i[1] for i in l[1:]]
        if actname in existed_act:
            logger.warning(f"已记录活动 {actname}，跳过记录")
        else:
            with open("./data/event.csv", mode="a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([int(id) + 1, actname, count, acttime, acttype])
                logger.debug(f"write {[int(id)+1, actname, count, acttime, acttype]} to ./data/event.csv")

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
        logger.debug(f'plot {fig_path.split("/")[-1]}, {fig_part_path.split("/")[-1]}, {fig_table_path.split("/")[-1]} to ./data')

        fig = visualize.crop_img(fig_path)
        fig_part = visualize.crop_img(fig_part_path)
        fig_table = visualize.crop_img(fig_table_path)
        visualize.watermark(fig, x=fig.size[0]-300, y=50, output_path=fig_path)
        visualize.watermark(fig_part, x=75, y=50, output_path=fig_part_path)

        win.send_qq(fig_path, logger, 'image')
        win.send_qq(fig_part_path, logger, 'image')
        win.send_qq(fig_table_path, logger, 'image')


        # 自动输出文案
        with open("./data/event.csv", mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            act_list = [row for row in reader][1:-1]
        minimal = 999999
        nearest = ''
        for act in act_list:
            if abs(count - int(act[2])) < minimal and act[4] == acttype:
                minimal = abs(count - int(act[2]))
                nearest = act[1]
        king_count = utils.get_act_count(king)
        memory_op = ''
        for op in memory_list:
            memory_op += f'【{op}】、'
        memory_op = memory_op[:-1]

        if acttype == 'main':
            writes = utils.TEMPLATE_MAIN.format(actname.split('_')[0], actname.split('_')[1], story_count, count/10000,
                                                nearest.split('_')[0], nearest.split('_')[1], utils.round_005(count/king_count), king, 
                                                memory_op, memory_count, count_memory/10000)
        elif acttype == 'act_ss':
            writes = utils.TEMPLATE_SS.format(actname, story_count, count/10000, nearest, utils.round_005(count/king_count), king, 
                                            memory_op, memory_count, count_memory/10000)
        elif acttype == 'act_om':
            writes = utils.TEMPLATE_OM.format(actname, story_count, count/10000, nearest, 
                                            memory_op, memory_count, count_memory/10000)
        logger.info(writes)
        win.send_qq(writes, logger, 'text')

        break

except Exception as e:
    logger.error(f'捕捉到例外 {e}')
finally:
    logger.info('=====程序已停止=====')
    win.send_qq("=====程序已停止=====", logger, 'text')
    with open('./logging.txt', encoding='utf_8') as f:
        win.send_qq(f.read(), logger, 'text')
