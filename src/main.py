import tkinter as tk
from tkinter import ttk, messagebox
import utils
import threading
import time
from datetime import datetime

class AntiLockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("防锁屏工具 (Anti-Lock)")
        self.root.geometry("320x220")
        self.root.resizable(False, False)

        # 变量初始化
        self.is_running = False
        self.idle_threshold = tk.IntVar(value=60) # 默认60秒
        self.current_idle_var = tk.StringVar(value="当前空闲: 0.0 秒")
        self.status_var = tk.StringVar(value="状态: 已停止")
        self.log_var = tk.StringVar(value="等待启动...")

        # 构建界面
        self.create_widgets()
        
        # 启动定时器用于更新UI显示的空闲时间（独立于防锁屏逻辑）
        self.update_ui_timer()

    def create_widgets(self):
        # 主容器
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 状态显示
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 10, "bold"))
        status_label.pack(pady=(0, 10))

        # 阈值设置区域
        setting_frame = ttk.LabelFrame(main_frame, text="设置", padding="10")
        setting_frame.pack(fill=tk.X, pady=5)

        ttk.Label(setting_frame, text="触发阈值(秒):").pack(side=tk.LEFT)
        spinbox = ttk.Spinbox(setting_frame, from_=5, to=3600, textvariable=self.idle_threshold, width=10)
        spinbox.pack(side=tk.RIGHT)

        # 实时信息区域
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, textvariable=self.current_idle_var).pack(anchor="w")
        ttk.Label(info_frame, textvariable=self.log_var, foreground="gray", font=("Arial", 8)).pack(anchor="w")

        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))

        self.start_btn = ttk.Button(btn_frame, text="启动监控", command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.stop_btn = ttk.Button(btn_frame, text="停止", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))

    def update_ui_timer(self):
        """
        每100ms更新一次界面上的空闲时间显示
        """
        try:
            idle_time = utils.get_idle_time()
            self.current_idle_var.set(f"当前空闲: {idle_time:.1f} 秒")
            
            # 核心监控逻辑放在这里，利用after循环
            if self.is_running:
                threshold = self.idle_threshold.get()
                if idle_time >= threshold:
                    self.trigger_action()
                    
        except Exception as e:
            # 在无控制台模式下，print可能会导致错误，因此注释掉
            # print(f"Error: {e}")
            pass

        # 只有窗口未销毁时才继续调度
        if self.root.winfo_exists():
            self.root.after(100, self.update_ui_timer)

    def trigger_action(self):
        """
        触发防锁屏动作
        """
        utils.jitter_mouse()
        now = datetime.now().strftime("%H:%M:%S")
        self.log_var.set(f"上次触发: {now} (鼠标微动)")
        # 抖动后，系统API的空闲时间会立即归零，所以不需要手动重置变量

    def start_monitoring(self):
        self.is_running = True
        self.status_var.set("状态: 监控中 🟢")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.log_var.set("正在监控系统空闲...")

    def stop_monitoring(self):
        self.is_running = False
        self.status_var.set("状态: 已停止 🔴")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log_var.set("监控已停止")

if __name__ == "__main__":
    root = tk.Tk()
    # 尝试设置图标 (如果有的话，这里略过)
    app = AntiLockApp(root)
    root.mainloop()