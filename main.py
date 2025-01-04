import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
import threading
import queue

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件整理工具")
        
        # 设置窗口最小尺寸
        self.root.minsize(800, 600)
        
        # 配置根窗口的网格布局
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 初始化消息队列用于线程间通信
        self.message_queue = queue.Queue()
        
        # 设置主题和样式
        self.style = ttk.Style()
        if os.name == 'posix':  # macOS
            self.style.theme_use('aqua')
        else:
            self.style.theme_use('default')
        
        # 创建主容器
        self.main_container = ttk.Frame(root)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # 配置主容器的网格布局
        self.main_container.grid_rowconfigure(0, weight=0)  # 标题区域
        self.main_container.grid_rowconfigure(1, weight=1)  # 内容区域
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # 创建标题
        title_frame = ttk.Frame(self.main_container)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=0)
        
        title = ttk.Label(
            title_frame, 
            text="文件整理工具", 
            font=("Arial", 24, "bold")
        )
        title.grid(row=0, column=0, pady=5)
        
        # 创建水印
        watermark = ttk.Label(
            title_frame,
            text="PM-小工具_Acmes",
            font=("Arial", 10),
            foreground="#cccccc"
        )
        watermark.grid(row=0, column=1, padx=5)
        
        # 创建内容框架
        content_frame = ttk.Frame(self.main_container)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=0)  # 步骤区域
        content_frame.grid_rowconfigure(1, weight=0)  # 操作区域
        content_frame.grid_rowconfigure(2, weight=0)  # 进度条区域
        content_frame.grid_rowconfigure(3, weight=1)  # 结果区域
        
        # 创建步骤指示器
        self.create_steps_frame(content_frame)
        
        # 创建操作区域
        self.create_operation_area(content_frame)
        
        # 创建进度条区域
        self.create_progress_area(content_frame)
        
        # 创建结果显示区域
        self.create_result_area(content_frame)
        
        # 初始化变量
        self.selected_folder = None
        self.organized_files = []
        self.organizing = False
        self.cancel_flag = False
        
        # 初始化文件类型映射
        self.init_file_types()
        
        # 启动GUI更新循环
        self.root.after(100, self.check_queue)
    
    def init_file_types(self):
        """初始化文件类型映射"""
        self.file_type_map = {
            # 图片文件
            '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image',
            '.bmp': 'image', '.tiff': 'image', '.webp': 'image',
            # 文档文件
            '.doc': 'document', '.docx': 'document', '.pdf': 'document',
            '.txt': 'document', '.rtf': 'document', '.odt': 'document',
            '.xls': 'document', '.xlsx': 'document', '.ppt': 'document',
            '.pptx': 'document',
            # 音频文件
            '.mp3': 'audio', '.wav': 'audio', '.flac': 'audio',
            '.m4a': 'audio', '.aac': 'audio', '.wma': 'audio',
            # 视频文件
            '.mp4': 'video', '.avi': 'video', '.mkv': 'video',
            '.mov': 'video', '.wmv': 'video', '.flv': 'video',
            # 压缩文件
            '.zip': 'archive', '.rar': 'archive', '.7z': 'archive',
            '.tar': 'archive', '.gz': 'archive',
            # 代码文件
            '.py': 'code', '.java': 'code', '.cpp': 'code',
            '.html': 'code', '.css': 'code', '.js': 'code',
        }
    
    def get_file_type(self, filename):
        """获取文件类型"""
        ext = os.path.splitext(filename)[1].lower()
        return self.file_type_map.get(ext, 'other')
    
    def create_steps_frame(self, parent):
        steps_frame = ttk.Frame(parent)
        steps_frame.grid(row=0, column=0, sticky="ew", pady=10)
        
        # 配置列权重以均匀分布步骤
        for i in range(3):
            steps_frame.grid_columnconfigure(i, weight=1)
        
        steps = ["选择需要整理的文件夹", "开始整理文件", "选择存放位置"]
        for i, step in enumerate(steps):
            step_frame = ttk.Frame(steps_frame, padding=5)
            step_frame.grid(row=0, column=i, padx=5, sticky="nsew")
            step_frame.grid_columnconfigure(0, weight=1)
            
            # 创建圆形数字标签的样式
            number_frame = ttk.Frame(step_frame, style='Circle.TFrame')
            number_frame.grid(row=0, column=0, pady=(0, 5))
            
            number = ttk.Label(
                number_frame,
                text=str(i + 1),
                font=("Arial", 14, "bold"),
                foreground="#666666"
            )
            number.grid(row=0, column=0, padx=10, pady=5)
            
            text = ttk.Label(
                step_frame,
                text=step,
                wraplength=120,
                justify="center",
                font=("Arial", 12)
            )
            text.grid(row=1, column=0, pady=5)
    
    def create_operation_area(self, parent):
        operation_frame = ttk.Frame(parent)
        operation_frame.grid(row=1, column=0, sticky="ew", pady=10)
        operation_frame.grid_columnconfigure(0, weight=1)
        
        # 创建按钮容器
        button_container = ttk.Frame(operation_frame)
        button_container.grid(row=0, column=0, pady=10)
        
        select_btn = ttk.Button(
            button_container,
            text="选择源文件夹",
            command=self.select_folder,
            width=20
        )
        select_btn.grid(row=0, column=0, padx=5)
        
        self.folder_label = ttk.Label(
            operation_frame,
            text="未选择文件夹",
            wraplength=600,
            font=("Arial", 11)
        )
        self.folder_label.grid(row=1, column=0, pady=10)
        
        # 创建操作按钮容器
        action_button_frame = ttk.Frame(operation_frame)
        action_button_frame.grid(row=2, column=0, pady=10)
        
        self.organize_btn = ttk.Button(
            action_button_frame,
            text="开始整理",
            command=self.start_organize_files,
            state="disabled",
            width=15
        )
        self.organize_btn.grid(row=0, column=0, padx=5)
        
        self.cancel_btn = ttk.Button(
            action_button_frame,
            text="取消",
            command=self.cancel_organization,
            state="disabled",
            width=15
        )
        self.cancel_btn.grid(row=0, column=1, padx=5)
    
    def create_progress_area(self, parent):
        self.progress_frame = ttk.Frame(parent)
        self.progress_frame.grid(row=2, column=0, sticky="ew", pady=10)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        # 创建进度条容器
        progress_container = ttk.Frame(self.progress_frame)
        progress_container.grid(row=0, column=0, sticky="ew")
        progress_container.grid_columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(
            progress_container,
            mode="determinate",
            length=600
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=5)
        
        self.progress_label = ttk.Label(
            progress_container,
            text="",
            font=("Arial", 11)
        )
        self.progress_label.grid(row=1, column=0, pady=5)
        
        # 初始时隐藏进度框架
        self.progress_frame.grid_remove()
    
    def create_result_area(self, parent):
        self.result_frame = ttk.Frame(parent)
        self.result_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(0, weight=1)
        
        # 创建文本框架
        text_frame = ttk.Frame(self.result_frame)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=20)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        # 创建文本框和滚动条
        self.result_text = tk.Text(
            text_frame,
            height=10,
            width=70,
            state="disabled",
            wrap=tk.WORD,
            font=("Arial", 11)
        )
        scrollbar = ttk.Scrollbar(text_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 创建按钮容器
        button_container = ttk.Frame(self.result_frame)
        button_container.grid(row=1, column=0, pady=10)
        
        # 创建保存按钮
        self.save_btn = ttk.Button(
            button_container,
            text="选择存放位置",
            command=self.select_save_location,
            state="disabled",
            width=20
        )
        self.save_btn.grid(row=0, column=0, pady=5)
        
        # 初始时隐藏结果框架
        self.result_frame.grid_remove()
    
    def check_queue(self):
        """检查消息队列并更新GUI"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                action = message.get('action')
                data = message.get('data')
                
                if action == 'update_progress':
                    self.progress_bar['value'] = data['progress']
                    self.progress_label['text'] = data['text']
                elif action == 'show_error':
                    messagebox.showerror("错误", data['message'])
                elif action == 'enable_organize_btn':
                    self.organize_btn['state'] = 'normal'
                    self.cancel_btn['state'] = 'disabled'
                elif action == 'show_results':
                    self.show_results()
                elif action == 'organization_complete':
                    self.organizing = False
                    self.organize_btn['state'] = 'normal'
                    self.cancel_btn['state'] = 'disabled'
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
    
    def select_folder(self):
        """选择要整理的文件夹"""
        folder = filedialog.askdirectory(title="选择要整理的文件夹")
        if folder:
            self.selected_folder = folder
            self.folder_label['text'] = f"已选择: {folder}"
            self.organize_btn['state'] = 'normal'
            self.result_frame.grid_remove()
            self.progress_frame.grid_remove()
            self.organized_files = []
    
    def start_organize_files(self):
        """开始整理文件"""
        if not self.selected_folder or not os.path.exists(self.selected_folder):
            messagebox.showerror("错误", "请先选择有效的文件夹")
            return
        
        self.organizing = True
        self.cancel_flag = False
        self.organize_btn['state'] = 'disabled'
        self.cancel_btn['state'] = 'normal'
        self.progress_frame.grid()
        self.result_frame.grid_remove()
        self.organized_files = []
        
        # 在新线程中执行文件整理
        thread = threading.Thread(target=self.organize_files)
        thread.daemon = True
        thread.start()
    
    def organize_files(self):
        """执行文件整理操作"""
        try:
            total_files = sum([len(files) for _, _, files in os.walk(self.selected_folder)])
            processed_files = 0
            
            for root, _, files in os.walk(self.selected_folder):
                if self.cancel_flag:
                    self.message_queue.put({
                        'action': 'enable_organize_btn'
                    })
                    return
                
                for filename in files:
                    if self.cancel_flag:
                        self.message_queue.put({
                            'action': 'enable_organize_btn'
                        })
                        return
                    
                    file_path = os.path.join(root, filename)
                    file_type = self.get_file_type(filename)
                    
                    # 记录文件信息
                    self.organized_files.append({
                        'name': filename,
                        'type': file_type,
                        'path': file_path
                    })
                    
                    processed_files += 1
                    progress = (processed_files / total_files) * 100
                    
                    self.message_queue.put({
                        'action': 'update_progress',
                        'data': {
                            'progress': progress,
                            'text': f"正在处理: {filename}"
                        }
                    })
            
            self.message_queue.put({
                'action': 'show_results'
        })

    except Exception as e:
            self.message_queue.put({
                'action': 'show_error',
                'data': {
                    'message': f"整理文件时出错: {str(e)}"
                }
            })
        finally:
            self.message_queue.put({
                'action': 'organization_complete'
            })
    
    def show_results(self):
        """显示整理结果"""
        self.result_frame.grid()
        self.result_text['state'] = 'normal'
        self.result_text.delete(1.0, tk.END)
        
        file_types = {}
        for file_info in self.organized_files:
            file_type = file_info['type']
            if file_type not in file_types:
                file_types[file_type] = []
            file_types[file_type].append(file_info['name'])
        
        result_text = "整理结果:\n\n"
        for file_type, files in file_types.items():
            result_text += f"{file_type.capitalize()}文件 ({len(files)}个):\n"
            for filename in files:
                result_text += f"  - {filename}\n"
            result_text += "\n"
        
        self.result_text.insert(1.0, result_text)
        self.result_text['state'] = 'disabled'
        self.save_btn['state'] = 'normal'
    
    def select_save_location(self):
        """选择文件存放位置并移动文件"""
        if not self.organized_files:
            messagebox.showerror("错误", "没有可移动的文件")
            return
        
        save_location = filedialog.askdirectory(title="选择文件存放位置")
        if not save_location:
            return
        
        try:
            # 创建类型文件夹
            for file_info in self.organized_files:
                type_folder = os.path.join(save_location, file_info['type'])
                if not os.path.exists(type_folder):
                    os.makedirs(type_folder)
                
                # 移动文件
                filename = os.path.basename(file_info['path'])
                new_path = os.path.join(type_folder, filename)
                
                # 如果目标位置已存在同名文件，添加时间戳
                if os.path.exists(new_path):
                    name, ext = os.path.splitext(filename)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_path = os.path.join(type_folder, f"{name}_{timestamp}{ext}")
                
                shutil.move(file_info['path'], new_path)
            
            messagebox.showinfo("成功", "文件整理完成！")
            self.save_btn['state'] = 'disabled'

    except Exception as e:
            messagebox.showerror("错误", f"移动文件时出错: {str(e)}")
    
    def cancel_organization(self):
        """取消文件整理操作"""
        self.cancel_flag = True
        self.cancel_btn['state'] = 'disabled'

def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 