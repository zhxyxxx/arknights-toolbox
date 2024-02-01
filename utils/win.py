import win32gui, win32api, win32con
import time, io
import win32clipboard as w
import pyautogui
from PIL import Image
from ctypes import *
# windows系统相关操作


def get_all_window():
    # 获取所有窗口名
    ''' return
    lt(type: list): 所有窗口名
    '''
    titles = set()
    def foo(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            titles.add(win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    return lt


def find_window(window_name):
    # 根据窗口名找到特定窗口
    ''' args
    window_name: 目标窗口名含有的文字

    return
    hwnd_list(type: list): 所有符合要求的窗口的句柄
    '''
    hwnd_list = []
    lt = get_all_window()
    for t in lt:
        if(t.find(window_name)) >= 0:
            hwnd_list.append(win32gui.FindWindow(None, t))
    return hwnd_list


def print_mouse_pos():
    # 输出光标的绝对位置坐标
    while True:
        print(win32gui.GetCursorPos())
        time.sleep(2)


def sim_click(hwnd, x, y):
    # 通过向窗口发送信息模拟鼠标点击（窗口后台运行时也可运作）
    ''' args
    hwnd: 目标窗口句柄
    x, y: 点击的窗口xy坐标
    '''
    pos = win32api.MAKELONG(x, y)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, pos)


def hard_click(x, y):
    # 硬件层面上模拟鼠标点击（仅当窗口处于最上层时可用）
    ''' args
    x, y: 点击的屏幕xy坐标
    '''
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


def hard_inf(x1, y1, x2, y2, limit=100000, interval=5):
    # 通过连续点击两点刷图
    # 使用硬模拟
    ''' args
    x1, y1: 第一点的屏幕xy坐标
    x2, y2: 第二点的屏幕xy坐标
    limit(default: 100000): 循环时间上限(秒)
    interval(default: 5): 两次点击之间的间隔(秒)
    '''
    cnt = limit
    while cnt > 0:
        hard_click(x1, y1)
        time.sleep(interval)
        hard_click(x1, y1)
        time.sleep(interval)
        hard_click(x2, y2)
        time.sleep(interval)
        cnt -= 3 * interval


def sim_inf(hwnd, x1, y1, x2, y2, limit=100000, interval=5):
    # 通过连续点击两点刷图
    # 使用软模拟
    ''' args
    hwnd: 目标窗口句柄
    x1, y1: 第一点的窗口xy坐标
    x2, y2: 第二点的窗口xy坐标
    limit(default: 100000): 循环时间上限(秒)
    interval(default: 5): 两次点击之间的间隔(秒)
    '''
    cnt = limit
    while cnt > 0:
        sim_click(hwnd, x1, y1)
        time.sleep(interval)
        sim_click(hwnd, x1, y1)
        time.sleep(interval)
        sim_click(hwnd, x2, y2)
        time.sleep(interval)
        cnt -= 3 * interval


def sim_inf_onepoint(hwnd, x, y, limit=100000, interval=5):
    # 通过连续点击一点刷图（可能因掉落材料过多导致死循环）
    # 使用软模拟
    ''' args
    hwnd: 目标窗口句柄
    x, y: 点击的窗口xy坐标
    limit(default: 100000): 循环时间上限(秒)
    interval(default: 5): 两次点击之间的间隔(秒)
    '''
    cnt = limit
    while cnt > 0:
        sim_click(hwnd, x, y)
        time.sleep(interval)
        cnt -= interval


def send_qq(content, logger, data_format='text', user_name="X-X-X"):
    # 向qq窗口发送消息
    # TODO: 内容格式file暂不可用，此时无法使用WM_PASTE模拟粘贴剪贴板上的文件
    ''' args
    content: 消息内容
    logger: 用于记录的logger
    data_format: 消息内容的格式(text, image, file)
    user_name: 发送对象用户名（确保已且仅打开该用户聊天窗口）

    return
    e: 发生的例外(无例外发生时返回0)
    '''
    class DROPFILES(Structure):
        _fields_ = [("pFiles", c_uint),
                    ("x", c_long),
                    ("y", c_long),
                    ("fNC", c_int),
                    ("fWide", c_bool),
                   ]

    if data_format == 'image':
        img = Image.open(content)
        output = io.BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
    elif data_format == 'file':
        pDropFiles = DROPFILES()
        pDropFiles.pFiles = sizeof(DROPFILES)
        pDropFiles.fWide = True
        metadata = bytes(pDropFiles)
        files = content.replace("/", "\\")
        data = metadata + files.encode("U16")[2:]

    time.sleep(1)
    try:
        w.OpenClipboard()
        w.EmptyClipboard()
        if data_format == 'text':
            w.SetClipboardData(win32con.CF_UNICODETEXT, content)
        elif data_format == 'image':
            w.SetClipboardData(win32con.CF_DIB, data)
        elif data_format == 'file':
            w.SetClipboardData(win32con.CF_HDROP, data)
    except Exception as e:
        logger.error(f'发送\'{content}\'至QQ时发生例外: {e}')
        return e
    finally:
        w.CloseClipboard()

    handle = win32gui.FindWindow(None, user_name)
    if handle == 0:
        logger.error(f'发送\'{content}\'至QQ时发生例外: 未找到窗口{user_name}')
        return -1
    try:
        win32gui.SetWindowPos(handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        time.sleep(1)
        left, top, right, bottom = win32gui.GetWindowRect(handle)
        pyautogui.moveTo(left + 100, bottom - 100)
        pyautogui.click()
        win32gui.SendMessage(handle, win32con.WM_PASTE, 0, 0)
        time.sleep(2)
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN)
    except Exception as e:
        logger.error(f'发送\'{content}\'至QQ时发生例外: {e}')
        return e
    finally:
        win32gui.SetWindowPos(handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    
    return 0
