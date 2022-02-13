import re
import glob

# 计算单个文件中的字数
def count_words(file):
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

# 计算文件夹中所有一级文件的字数合计
def sum_words(dir):
    files = glob.glob(f'{dir}/*.txt')

    count = 0

    for file in files:
        count += count_words(file)

    return count


choice = ['main', 'activities', 'memory']
for c in choice:
    print(c)
    path = f'./story/{c}/*'
    acts = glob.glob(path)

    llist = []

    for act in acts:
        n = act.split('\\')[-1]
        dir = f'./story/{c}/{n}'

        count = sum_words(dir)

        llist.append((n, count))
        # print(n, count)

    llist.sort(key=lambda x: x[1])
    print(llist)

# count = sum_words('./story/activities/*')
# count = count_words('./story/activities/*/*.txt')
