from utils import data
import os

for curDir, dirs, files in os.walk("../ArknightsGameData/zh_CN/gamedata"):
    first_dirs = dirs
    break

writef = open('chinese_file.txt', mode='w')

for dir in first_dirs:
    chinese_file = []
    print(dir)
    for curDir, dirs, files in os.walk(f"../ArknightsGameData/zh_CN/gamedata/{dir}"):
        if len(files) != 0:
            for f in files:
                flag = data.chinese_in_file(f'{curDir}/{f}')
                if flag:
                    chinese_file.append(f'{curDir}/{f}')
    print(len(chinese_file))

    writef.write(f'{dir} {len(chinese_file)}\n')
    for cf in chinese_file:
        if cf.split('.')[-1] != 'txt':
            writef.write(f'{cf}\n')
    writef.write('\n')

writef.close()
