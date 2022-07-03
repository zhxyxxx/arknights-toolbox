# 数据处理相关


def _is_chinese(uchar):
    # 判断字符是否为汉字
    if uchar >= 19968 and uchar <= 40869:
        return True
    else:
        return False


def _chinese_in_str(str):
    # 判断字符串里是否含有汉字
    for s in str:
        if _is_chinese(ord(s)):
            return True
    return False


def chinese_in_file(path):
    # 判断文件中是否含有汉字
    ''' args
    path: 目标文件路径

    return
    flag(type: bool): 是否含有汉字
    '''
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    for s in lines:
        flag = _chinese_in_str(s)
        if flag:
            return True
    return False


def solve_dict(root, d, f=None, extract_ch=False):
    # 处理复杂词典信息并输出
    ''' args
    root: 根字符
    d: 待处理的信息
    f(default: None): 输出文件
    extract_ch(default: False): 是否过滤中文
    '''
    if isinstance(d, dict):
        for k, v in d.items():
            if root != '':
                k = f'{root}.{k}'
            solve_dict(k, v, f, extract_ch)
    elif isinstance(d, list):
        for idx, l in enumerate(d):
            k = f'{root}.L_{idx}'
            solve_dict(k, l, f, extract_ch)
    else:
        if (not extract_ch) or (isinstance(d, str) and _chinese_in_str(d)):
            print(root, d)
            if f is not None:
                f.write(f'{root} {d}\n')
