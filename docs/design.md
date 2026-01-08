## 防锁屏工具 - 实现方案

---

## 📋 一、需求概述

| 项目 | 描述 |
|------|------|
| **目标** | 防止公司电脑因长时间无操作自动锁屏 |
| **运行平台** | Windows |
| **技术栈** | Python + PyQt5 |
| **最终产出** | 单个exe可执行文件 |

---

## 🏗️ 二、系统架构

```
┌────────────────────────────────────────────────────────────┐
│                     PyQt5 GUI 层                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │ 主窗口   │  │ 系统托盘 │  │ 设置面板 │  │ 状态显示   │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘ │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                     业务逻辑层                              │
│  ┌─────────────────┐        ┌─────────────────────────┐   │
│  │ 监控调度器      │◄──────►│  配置管理(QSettings)    │   │
│  │ (QTimer定时)    │        │  - 触发时间             │   │
│  └─────────────────┘        │  - 模拟方式             │   │
│            │                │  - 开关状态             │   │
│            ▼                └─────────────────────────┘   │
│  ┌─────────────────┐                                      │
│  │ 空闲检测模块    │                                      │
│  │ (Windows API)   │                                      │
│  └─────────────────┘                                      │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                   用户操作模拟层                            │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │ 鼠标模拟        │  │ 键盘模拟        │                 │
│  │ (ctypes/WinAPI) │  │ (ctypes/WinAPI) │                 │
│  └─────────────────┘  └─────────────────┘                 │
└────────────────────────────────────────────────────────────┘
```

---

## 📦 三、模块划分

### 3.1 GUI模块

| 组件 | 功能 |
|------|------|
| **主窗口** | 显示状态、设置参数、启动/停止按钮 |
| **系统托盘** | 常驻后台、右键菜单、状态提示 |
| **设置面板** | 触发时间、模拟方式选择 |

### 3.2 核心功能模块

| 模块 | 功能 | 技术方案 |
|------|------|----------|
| **空闲检测** | 获取系统空闲时间 | `GetLastInputInfo` (WinAPI) |
| **鼠标模拟** | 模拟鼠标移动/点击 | `mouse_event` (WinAPI) |
| **键盘模拟** | 模拟键盘按键 | `keybd_event` (WinAPI) |
| **配置存储** | 保存用户设置 | `QSettings` |
| **监控调度** | 定时检查空闲状态 | `QTimer` |

---

## 🔧 四、关键接口定义

### 4.1 空闲检测模块

```python
def get_idle_time() -> int:
    """
    获取系统空闲时间
  
    Returns:
        int: 空闲时间(毫秒)
    """

def is_user_active(threshold_seconds: int) -> bool:
    """
    检查用户是否处于空闲状态
  
    Args:
        threshold_seconds: 空闲阈值(秒)
  
    Returns:
        bool: True表示空闲，False表示活跃
    """
```

### 4.2 用户操作模拟模块

```python
def simulate_mouse_move(dx: int = 10, dy: int = 10) -> None:
    """模拟鼠标相对移动"""

def simulate_mouse_click(button: str = "left") -> None:
    """模拟鼠标点击"""

def simulate_key_press(key_code: int, modifiers: int = 0) -> None:
    """模拟键盘按键"""
```

### 4.3 配置管理模块

```python
class ConfigManager:
    def get_idle_threshold(self) -> int: ...
    def set_idle_threshold(self, value: int) -> None: ...
  
    def get_simulate_type(self) -> str: ...
    def set_simulate_type(self, value: str) -> None: ...
  
    def get_enabled(self) -> bool: ...
    def set_enabled(self, value: bool) -> None: ...
  
    def save(self) -> None: ...
    def load(self) -> None: ...
```

### 4.4 主控制模块

```python
class AntiLockController:
    def start_monitoring(self) -> None:
        """启动监控"""
      
    def stop_monitoring(self) -> None:
        """停止监控"""
      
    def is_running(self) -> bool:
        """是否运行中"""
      
    def get_status(self) -> dict:
        """获取当前状态"""
```

---

## ⚙️ 五、技术选型

| 层级 | 方案 | 理由 |
|------|------|------|
| **GUI框架** | PyQt5 | 功能完善、生态成熟 |
| **空闲检测** | WinAPI `GetLastInputInfo` | 原生API、轻量无依赖 |
| **输入模拟** | WinAPI `mouse_event`/`keybd_event` | 原生API、无需第三方库 |
| **配置存储** | QSettings | PyQt内置、跨平台兼容 |
| **打包工具** | PyInstaller | 成熟稳定、支持单文件 |

### 依赖清单（最小化）

```
PyQt5 >= 5.15.0
# 无其他第三方依赖
```

---

## 🎯 六、实现要点

### 6.1 空闲检测

```cpp
// C++伪代码参考
LASTINPUTINFO lastInput;
lastInput.cbSize = sizeof(LASTINPUTINFO);
GetLastInputInfo(&lastInput);
idleTime = GetTickCount() - lastInput.dwTime;
```

### 6.2 模拟操作

```
鼠标移动:
  mouse_event(MOUSEEVENTF_MOVE, dx, dy, 0, 0)

鼠标点击:
  mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
  mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

键盘按键:
  keybd_event(vkCode, 0, KEYEVENTF_KEYDOWN, 0)
  keybd_event(vkCode, 0, KEYEVENTF_KEYUP, 0)
```

### 6.3 模拟操作隐蔽性

| 策略 | 说明 |
|------|------|
| 鼠标微动 | 移动10-20像素，人眼难以察觉 |
| 随机化 | 每次移动位置、方向略有不同 |
| Shift键 | 选择不太干扰用户的键位 |

---

## 📝 七、UI设计规格

### 7.1 主窗口元素

| 元素 | 类型 | 默认值 |
|------|------|--------|
| 状态标签 | QLabel | 显示运行/停止状态 |
| 空闲时间显示 | QLabel | 实时显示当前空闲秒数 |
| 触发时间设置 | QSpinBox | 范围: 10-600秒，默认60秒 |
| 模拟方式选择 | QComboBox | 鼠标微动/鼠标点击/键盘按键 |
| 启动按钮 | QPushButton | 绿色 |
| 停止按钮 | QPushButton | 红色，默认禁用 |

### 7.2 系统托盘

| 功能 | 说明 |
|------|------|
| 图标 | 显示运行状态 |
| 提示文本 | "防锁屏工具 - 运行中/已停止" |
| 右键菜单 | 显示窗口、退出 |
| 气泡通知 | 模拟操作时提示 |

---

## ⚠️ 八、开发注意事项

| 序号 | 注意事项 |
|------|----------|
| 1 | 使用`ctypes`调用WinAPI，避免引入pyautogui等重量级库 |
| 2 | 打包时使用`--noconsole`参数隐藏控制台 |
| 3 | 设置`app.setQuitOnLastWindowClosed(False)`支持后台运行 |
| 4 | 实现`closeEvent`重写，最小化到托盘而非退出 |
| 5 | 定期调用`QApplication.processEvents()`处理事件 |
| 6 | 异常捕获要全面，防止程序崩溃导致锁屏 |
| 7 | 使用`--clean`清理临时文件减小打包体积 |

---

## 📦 九、打包命令

```bash
pyinstaller ^
    --onefile ^
    --noconsole ^
    --name AntiLockScreen ^
    --clean ^
    anti_lock_screen.py
```

**预期exe大小**: 25-35 MB

---

## ✅ 十、验收标准

| 测试项 | 预期结果 |
|--------|----------|
| 启动程序 | 窗口显示，系统托盘出现图标 |
| 点击启动 | 状态变为"运行中"，定时检查空闲 |
| 无操作超过阈值 | 自动模拟鼠标/键盘操作 |
| 手动操作电脑 | 重置空闲计时器 |
| 点击托盘图标 | 显示/隐藏主窗口 |
| 关闭窗口 | 程序最小化到托盘运行 |
| 打包为exe | 单独运行无控制台窗口，体积<40MB |

---

以上方案可直接提供给AI编程工具生成代码。如需调整或补充，请告知。