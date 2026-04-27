import os
import re
import time
import threading
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class YouTubeTimeEstimatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Time Estimator (Screenshots)")
        self.root.geometry("450x400")
        
        self.running = False
        self.target_time = None
        self.reload_time = None
        self.count = 0
        self.max_count = 120
        self.driver = None
        self.thread = None
        
        self.screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        self.log_file = os.path.join(os.path.dirname(__file__), "log.txt")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        self.setup_ui()
        self.update_ui_loop()

    def setup_ui(self):
        # URL Input
        tk.Label(self.root, text="YouTube URL:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.url_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.url_var, width=50).pack(pady=5)
        
        # Start/Stop Button
        self.btn_start = tk.Button(self.root, text="開始", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.toggle_process)
        self.btn_start.pack(pady=10)
        
        # Info Labels
        frame = tk.Frame(self.root)
        frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(frame, text="現在時刻:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5)
        self.lbl_now = tk.Label(frame, text="--:--:--", font=("Arial", 12, "bold"))
        self.lbl_now.grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(frame, text="次回リロード予定:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
        self.lbl_reload = tk.Label(frame, text="--:--:--", font=("Arial", 12, "bold"), fg="blue")
        self.lbl_reload.grid(row=1, column=1, sticky="w", pady=5)
        
        tk.Label(frame, text="次回撮影予定:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=5)
        self.lbl_target = tk.Label(frame, text="--:--:--", font=("Arial", 12, "bold"), fg="red")
        self.lbl_target.grid(row=2, column=1, sticky="w", pady=5)
        
        tk.Label(frame, text="実行回数:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", pady=5)
        self.lbl_count = tk.Label(frame, text="0 / 120", font=("Arial", 12, "bold"))
        self.lbl_count.grid(row=3, column=1, sticky="w", pady=5)

        self.lbl_status = tk.Label(self.root, text="待機中...", font=("Arial", 10))
        self.lbl_status.pack(pady=10)

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        msg = f"[{timestamp}] {message}"
        print(msg)
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except Exception as e:
            print(f"Log write error: {e}")

    def update_ui_loop(self):
        # Update current time
        now = datetime.now()
        self.lbl_now.config(text=now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4])
        
        # Update target/reload times
        if self.reload_time:
            self.lbl_reload.config(text=self.reload_time.strftime("%H:%M:%S"))
        else:
            self.lbl_reload.config(text="--:--:--")
            
        if self.target_time:
            self.lbl_target.config(text=self.target_time.strftime("%H:%M:%S"))
        else:
            self.lbl_target.config(text="--:--:--")
            
        # Update count
        self.lbl_count.config(text=f"{self.count} / {self.max_count}")
        
        # Loop every 50ms
        self.root.after(50, self.update_ui_loop)

    def toggle_process(self):
        if self.running:
            self.stop_process()
        else:
            self.start_process()

    def start_process(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("エラー", "URLを入力してください。")
            return
            
        self.running = True
        self.count = 0
        self.btn_start.config(text="停止", bg="#F44336")
        self.lbl_status.config(text="実行中...")
        self.log(f"プロセス開始: URL={url}")
        
        self.thread = threading.Thread(target=self.process_loop, args=(url,), daemon=True)
        self.thread.start()

    def stop_process(self):
        self.running = False
        self.btn_start.config(text="開始", bg="#4CAF50")
        self.lbl_status.config(text="待機中...")
        self.target_time = None
        self.reload_time = None
        self.log("プロセス停止")

    def get_next_times(self, now: datetime):
        # 次の05秒または55秒を計算
        if now.second < 5:
            target = now.replace(second=5, microsecond=0)
        elif now.second < 55:
            target = now.replace(second=55, microsecond=0)
        else:
            target = (now + timedelta(minutes=1)).replace(second=5, microsecond=0)
            
        # リロード時刻はターゲットの3秒前
        reload_time = target - timedelta(seconds=3)
        return target, reload_time

    def sanitize_filename(self, url):
        suffix = url[-10:] if len(url) >= 10 else url
        return re.sub(r'[\\/:*?"<>|]', '_', suffix)

    def init_browser(self):
        self.log("ブラウザを起動しています...")
        options = Options()
        options.add_argument('--headless')  # 画面非表示
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.implicitly_wait(10)
            return driver
        except Exception as e:
            self.log(f"ブラウザ初期化エラー: {e}")
            return None

    def process_loop(self, url):
        self.driver = self.init_browser()
        if not self.driver:
            self.root.after(0, self.stop_process)
            messagebox.showerror("エラー", "ブラウザの起動に失敗しました。ログを確認してください。")
            return
            
        is_first_access = True
        
        try:
            while self.running and self.count < self.max_count:
                now = datetime.now()
                self.target_time, self.reload_time = self.get_next_times(now)
                
                # リロード待機フェーズ
                while datetime.now() < self.reload_time:
                    if not self.running:
                        break
                    time.sleep(0.05)
                
                if not self.running:
                    break
                    
                # リロード実行フェーズ
                try:
                    if is_first_access:
                        self.log("初回アクセス中...")
                        self.driver.get(url)
                        is_first_access = False
                    else:
                        self.log("リロード実行")
                        self.driver.get(url) # リフレッシュよりも確実な再読み込みのためgetを使用
                except Exception as e:
                    self.log(f"ページ読み込みエラー: {e}")
                    # エラーでもリトライできるように進める
                
                # リロード完了後、現在の時刻をチェックし、ターゲット時刻を過ぎていないか確認
                now_after_reload = datetime.now()
                if now_after_reload >= self.target_time:
                    self.log("missed timing: リロードに時間がかかりすぎました。")
                    continue
                    
                # 撮影待機フェーズ (高頻度監視)
                while datetime.now() < self.target_time:
                    if not self.running:
                        break
                    time.sleep(0.005) # 5ms待機
                    
                if not self.running:
                    break
                    
                # 撮影実行フェーズ (ターゲット時刻ジャスト)
                actual_capture_time = datetime.now()
                # ファイル名はターゲット時刻を基準にする (例: 05秒または55秒)
                filename_time_str = self.target_time.strftime("%Y%m%d%H%M%S")
                url_suffix = self.sanitize_filename(url)
                filename = f"{filename_time_str}_{url_suffix}.png"
                filepath = os.path.join(self.screenshot_dir, filename)
                
                try:
                    self.driver.save_screenshot(filepath)
                    diff = (actual_capture_time - self.target_time).total_seconds()
                    self.log(f"スクリーンショット取得: {filename} (ズレ: {diff:.3f}秒)")
                    self.count += 1
                except Exception as e:
                    self.log(f"スクリーンショット保存エラー: {e}")
                    
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
            self.log("ブラウザを終了しました。")
            if self.count >= self.max_count:
                self.log("規定回数(120回)の実行が完了しました。")
            self.root.after(0, self.stop_process)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeTimeEstimatorApp(root)
    root.mainloop()
