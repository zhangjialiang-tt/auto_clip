import ctypes
import time
from ctypes import wintypes

# 定义 Windows API 结构体和常量
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("dwTime", ctypes.c_ulong)
    ]

# 加载 user32.dll
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 常量定义
MOUSEEVENTF_MOVE = 0x0001
INPUT_MOUSE = 0

def get_idle_time() -> float:
    """
    获取系统空闲时间（秒）
    """
    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)
    
    if user32.GetLastInputInfo(ctypes.byref(last_input_info)):
        # 获取系统启动后的毫秒数
        tick_count = kernel32.GetTickCount()
        # 计算空闲时间 (毫秒 -> 秒)
        idle_milliseconds = tick_count - last_input_info.dwTime
        return idle_milliseconds / 1000.0
    return 0.0

def jitter_mouse():
    """
    执行鼠标微抖动：向右移动 1 像素，然后立即向左移动 1 像素。
    系统会识别为输入活动，但视觉上光标几乎不动。
    """
    # 向右移动 1 像素
    user32.mouse_event(MOUSEEVENTF_MOVE, 1, 0, 0, 0)
    # 向左移动 1 像素
    user32.mouse_event(MOUSEEVENTF_MOVE, -1, 0, 0, 0)
