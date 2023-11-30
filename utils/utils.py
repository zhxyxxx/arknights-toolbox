# 泛用处理
import os


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
