from utils import win
import sys
import argparse

parser = argparse.ArgumentParser(description='舟游自动刷图')
parser.add_argument('-w', '--window', type=str, default='夜神模拟器', help='使用的窗口名(的一部分)')
parser.add_argument('-n', '--newUI', action='store_true', help='暂时适配新UI（愚人号），可能因掉落材料过多导致死循环')
parser.add_argument('-t', '--time', type=int, default=100000, help='运行总时长')
parser.add_argument('--test', action='store_true', help='启用测试模式')

args = parser.parse_args()

hwnd_list = win.find_window(args.window)
assert len(hwnd_list) == 1
hwnd = hwnd_list[0]

print('请使用Ctrl+c停止该脚本')
try:
	# print_mouse_pos()
	if args.test:
		import win32gui, win32api
		size = win32gui.GetWindowRect(hwnd)
		win32api.SetCursorPos([size[0]+1100, size[1]+665])
		win.print_mouse_pos()
	elif args.newUI:
		win.sim_inf_onepoint(hwnd, 1100, 665, limit=args.time)
	else:
		win.sim_inf(hwnd, 1100, 665, 1090, 350, limit=args.time)
except KeyboardInterrupt:
	print('脚本已停止')
	sys.exit(0)
