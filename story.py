import re
import glob

path = './story/activities/act15side/*.txt'
files = glob.glob(path)
# print(files)

count = 0

for file in files:
    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    for l in lines:
        if re.search(r'^\[HEADER.*\]', l):
            # HEADER 标题，不计入
            continue
        elif re.search(r'^\[Subtitle.*\]', l):
            # Subtitle 显示在画面中央的字幕
            l0 = re.findall('text="(.*?)",', l)
            if len(l0) == 0:
                continue
            assert len(l0) == 1
            l0 = l0[0]
        else:
            # 其它正常的对话框字幕
            l0 = re.sub('^\[.*\]', '', l)
            l0 = l0.strip()
        if len(l0) == 0:
            continue
        l0 = re.sub(' ', '', l0)
        l0 = re.sub('\\\\n', '', l0)
        count += len(l0)
        # print(l0, len(l0))

print(count)
