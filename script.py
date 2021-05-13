import win32gui, win32api, win32con
import time, sys
import argparse

parser = argparse.ArgumentParser(description='舟游自动刷图')
parser.add_argument('-w', '--window', type=str, default='夜神模拟器', help='使用的窗口名(的一部分)')
parser.add_argument('-t', '--time', type=int, default=180, help='一次通关所用时间')
parser.add_argument('-i', '--iter', type=int, default=5, help='需要通关次数')

args = parser.parse_args()


titles = set()
def foo(hwnd, mouse):
	if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
		titles.add(win32gui.GetWindowText(hwnd))

win32gui.EnumWindows(foo, 0)
lt = [t for t in titles if t]
lt.sort()
for t in lt:
	if(t.find(args.window)) >= 0:
		hwnd = win32gui.FindWindow(None, t)
		print(hwnd)
		#win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 1300, 750, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
		size = win32gui.GetWindowRect(hwnd)
		#print(size)
try:
	hwnd
except NameError:
	print(f'未找到窗口:{args.window}')
	sys.exit(1)

# 输出光标的绝对位置坐标
def print_mouse_pos():
	while True:
		print(win32gui.GetCursorPos())
		time.sleep(2)

# 通过向窗口发送信息模拟鼠标点击（窗口后台运行时也可运作）
def sim_click(x, y):
	pos = win32api.MAKELONG(x, y)
	win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)
	win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, pos)

# 硬件层面上模拟鼠标点击（仅当窗口处于最上层时可用）
def hard_click(x, y):
	win32api.SetCursorPos([size[0] + x, size[1] + y])
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

# 通过指定时间准确复现操作（实际使用误差大）
def click_by_time():
	for i in range(args.iter):
		sim_click(1100, 675)
		time.sleep(5)
		sim_click(1100, 600)
		time.sleep(args.time)
		sim_click(1100, 350)
		print(f'第{i+1}/{args.iter}次')
		time.sleep(12)

# 通过连续点击两点刷图（可能发生误操作）
def click_inf():
	while True:
		sim_click(1100, 655)
		time.sleep(5)
		sim_click(1100, 655)
		time.sleep(5)
		sim_click(1090,350)
		time.sleep(5)

if __name__ == '__main__':

	print('请使用Ctrl+c停止该脚本')
	try:
		#print_mouse_pos()
		# click_by_time()
		click_inf()
	except KeyboardInterrupt:
		print('脚本已停止')
		sys.exit(0)
