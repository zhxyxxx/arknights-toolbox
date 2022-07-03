import re
import glob
# 剧情文件相关处理


def count_words_in_file(file):
    # 计算单个文件中的剧情相关字数
    ''' args
    file: 目标剧情文件路径

    return
    count(type: int): 文件中的剧情字数
    '''
    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    count = 0
    for l in lines:
        if re.search(r'^\[HEADER.*\]', l):
            # HEADER 标题，不计入
            continue
        elif re.search(r'^\[Subtitle.*\]', l):
            # Subtitle 显示在画面中央的字幕
            l0 = re.findall('text="(.*?)"', l)
            if len(l0) == 0:
                continue
            assert len(l0) == 1
            l0 = l0[0]
        elif re.search(r'^\[Decision.*\]', l):
            # Desicion 可选对话
            l0 = re.findall('options="(.*?)"', l)
            assert len(l0) == 1
            l0 = re.sub(';', '', l0[0])
        else:
            # 其它正常的对话框字幕
            l0 = re.sub('^\[.*?\]', '', l)
            l0 = l0.strip()
        if len(l0) == 0:
            continue
        l0 = re.sub(' ', '', l0)
        l0 = re.sub('\\\\n', '', l0)
        count += len(l0)
        # print(l0, len(l0))
    return count


def sum_words_in_dir(dir):
    # 计算文件夹中所有一级文件的字数合计
    ''' args
    dir: 目标文件夹路径

    return
    count(type: int): 文件夹中的剧情字数合计
    '''
    files = glob.glob(f'{dir}/*.txt')
    count = 0
    for file in files:
        count += count_words_in_file(file)
    return count


def count_all(dir, subdir=['main', 'activities', 'memory']):
    # 计算所有剧情的字数并输出
    ''' args
    dir: 目标文件夹路径
    subdir(default: ['main', 'activities', 'memory']): 二级文件夹名

    return
    list_all(type: list): 所有活动名和对应字数
    cnt_all(type: int): 指定文件夹中的所有剧情字数合计
    '''
    cnt_all = 0
    list_all = []
    for d in subdir:
        print(d)
        path = f'{dir}/{d}/*'
        acts = glob.glob(path)
        llist = []

        for act in acts:
            n = act.split('\\')[-1]
            tar_dir = f'{dir}/{d}/{n}'
            count = sum_words_in_dir(tar_dir)
            llist.append((n, count))
            cnt_all += count

        llist.sort(key=lambda x: x[1])
        print(llist)
        list_all.append((d, llist))
    print(cnt_all)
    return list_all, cnt_all


def find_str(dir, query):
    # 在文件夹中查找特定字符串
    ''' args
    dir: 目标文件夹路径
    query: 需要查找的字符串

    return
    lst(type: list): 查找到的字符串和所属文件
    '''
    files = glob.glob(f'{dir}/*.txt')
    lst = []
    for file in files:
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()

        for l in lines:
            if re.search(rf'^\[{query}.*\]', l):
                lst.append((l, file))

    return lst
