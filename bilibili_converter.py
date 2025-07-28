import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import re
import ffmpeg
from pathlib import Path

CONFIG_FILE = "bilibili_converter_config.json"

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


class BilibiliConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Bilibili缓存转换器")
        
        # 加载配置
        self.config = load_config()
        
        # 缓存目录变量
        self.cache_dir = tk.StringVar()
        self.cache_dir.set(self.config.get('last_cache_dir', "未选择"))
        
        # 输出目录变量
        self.output_dir = tk.StringVar()
        self.output_dir.set(self.config.get('last_output_dir', "未选择"))
        
        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        # 缓存目录选择
        tk.Label(self.root, text="Bilibili缓存目录:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.cache_dir, width=40).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="选择", command=self.select_cache_dir).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录选择
        tk.Label(self.root, text="输出目录:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.output_dir, width=40).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="选择", command=self.select_output_dir).grid(row=1, column=2, padx=5, pady=5)
        
        # 转换按钮
        tk.Button(self.root, text="开始转换", command=self.convert).grid(row=2, column=1, pady=10)
        


    def select_cache_dir(self):
        dir_path = filedialog.askdirectory(
            title="选择Bilibili缓存目录",
            initialdir=self.config.get('last_cache_dir', os.path.expanduser('~'))
        )
        if dir_path:
            self.cache_dir.set(dir_path)
            self.config['last_cache_dir'] = dir_path
            save_config(self.config)
    
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(
            title="选择输出目录",
            initialdir=self.config.get('last_output_dir', os.path.expanduser('~'))
        )
        if dir_path:
            self.output_dir.set(dir_path)
            self.config['last_output_dir'] = dir_path
            save_config(self.config)
    
    def process_m4s_file(self, file_path):
        """处理m4s文件，移除前9个0x30字节"""
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # 移除前9个0x30字节
        if content.startswith(b'\x30'*9):
            content = content[9:]
        
        return content
    
    def get_video_title(self, cache_dir):
        """从videoInfo.json获取视频标题"""
        json_path = os.path.join(cache_dir, "videoInfo.json")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('title', 'output')
        except Exception as e:
            print(f"读取videoInfo.json失败: {e}")
            return "output"

    def convert(self):
        """执行转换操作"""
        cache_dir = self.cache_dir.get()
        output_dir = self.output_dir.get()
        
        if cache_dir == "未选择" or output_dir == "未选择":
            messagebox.showerror("错误", "请先选择缓存目录和输出目录")
            return
        
        try:
            # 获取视频标题
            title = self.get_video_title(cache_dir)
            output_path = os.path.join(output_dir, f"{title}.mp4")
            
            # 查找m4s文件
            m4s_files = [f for f in os.listdir(cache_dir) if f.endswith('.m4s')]
            if len(m4s_files) != 2:
                messagebox.showerror("错误", "缓存目录中必须包含2个.m4s文件")
                return
            
            # 创建临时目录
            temp_dir = os.path.join(output_dir, "temp")
            try:
                os.makedirs(temp_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("错误", f"创建临时目录失败: {e}")
                return
            
            # 处理m4s文件
            processed_files = []
            for i, m4s_file in enumerate(m4s_files):
                file_path = os.path.join(cache_dir, m4s_file)
                processed_content = self.process_m4s_file(file_path)
                temp_path = os.path.join(temp_dir, f"temp_{i}.m4s")
                with open(temp_path, 'wb') as f:
                    f.write(processed_content)
                processed_files.append(temp_path)
            
            # 执行转换
            try:
                video_stream = ffmpeg.input(processed_files[0])
                audio_stream = ffmpeg.input(processed_files[1])
                ffmpeg.overwrite_output(ffmpeg.output(video_stream, audio_stream, output_path, c='copy')).run()
                messagebox.showinfo("成功", f"视频已成功转换并保存到:\n{output_path}")
                
            except Exception as e:
                messagebox.showerror("错误", f"合并视频时出错: {e}")
            finally:
                # 清理临时目录
                try:
                    for temp_file in processed_files:
                        try:
                            os.remove(temp_file)
                        except:
                            pass
                    os.rmdir(temp_dir)
                except Exception as e:
                    print(f"清理临时文件时出错: {e}")
                    
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中出错: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BilibiliConverter(root)
    root.mainloop()
