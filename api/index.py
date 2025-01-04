from flask import Flask, request, jsonify, send_from_directory, send_file, Response
import os
from datetime import datetime
import shutil
from pathlib import Path
import mimetypes
from waitress import serve
import json
import subprocess

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

def get_file_type(file_path):
    mime_type = mimetypes.guess_type(file_path)[0]
    if mime_type:
        if 'image' in mime_type:
            return 'IMG'
        elif 'video' in mime_type:
            return 'VID'
        elif 'audio' in mime_type:
            return 'AUD'
        elif 'text' in mime_type or 'document' in mime_type:
            return 'DOC'
    return 'FILE'

@app.route('/')
def index():
    return send_file(os.path.join(current_dir, 'index.html'))

@app.route('/select_folder', methods=['GET'])
def select_folder():
    try:
        # AppleScript 命令来显示文件夹选择对话框
        script = '''
        tell application "System Events"
            activate
            set folderPath to choose folder with prompt "选择保存位置"
            return POSIX path of folderPath
        end tell
        '''
        
        # 执行 AppleScript
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            folder_path = result.stdout.strip()
            return jsonify({
                'status': 'success',
                'path': folder_path
            })
        else:
            return jsonify({
                'status': 'cancelled',
                'error': '未选择文件夹'
            })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/organize', methods=['POST'])
def organize_files():
    try:
        # 获取上传的文件列表
        files = request.files.getlist('files[]')
        if not files:
            return jsonify({'error': '没有找到文件'})

        # 创建目标文件夹（使用当前日期）
        today = datetime.now().strftime('%Y%m%d')
        temp_folder = os.path.join(current_dir, f'整理_{today}')
        os.makedirs(temp_folder, exist_ok=True)

        # 用于记录每种文件类型的计数
        counters = {}
        processed_files = []
        total_files = len(files)

        # 处理每个文件
        for index, file in enumerate(files, 1):
            try:
                # 获取文件类型
                file_type = get_file_type(file.filename)
                
                # 更新计数器
                if file_type not in counters:
                    counters[file_type] = 1
                else:
                    counters[file_type] += 1

                # 生成新文件名
                new_filename = f"{today}_{file_type}_{counters[file_type]:03d}{os.path.splitext(file.filename)[1]}"
                new_path = os.path.join(temp_folder, new_filename)

                # 保存文件
                file.save(new_path)

                processed_files.append({
                    'original': file.filename,
                    'new': new_filename,
                    'status': 'success'
                })

            except Exception as e:
                processed_files.append({
                    'original': file.filename,
                    'new': '',
                    'status': 'error',
                    'error': str(e)
                })

        return jsonify({
            'status': 'success',
            'temp_folder': temp_folder,
            'folder_name': f'整理_{today}',
            'processed_files': processed_files
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/move_folder', methods=['POST'])
def move_folder():
    try:
        data = request.json
        source_folder = data.get('source_folder')
        target_path = data.get('target_path')
        folder_name = data.get('folder_name')

        if not all([source_folder, target_path, folder_name]):
            return jsonify({'error': '缺少必要的参数'})

        # 确保目标路径存在
        target_folder = os.path.join(target_path, folder_name)
        
        # 如果目标文件夹已存在，添加数字后缀
        counter = 1
        original_target = target_folder
        while os.path.exists(target_folder):
            target_folder = f"{original_target}_{counter}"
            counter += 1

        # 移动文件夹
        shutil.move(source_folder, target_folder)

        return jsonify({
            'status': 'success',
            'message': '文件夹已移动到指定位置',
            'final_path': target_folder
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("服务器已启动，请访问 http://127.0.0.1:8080")
    serve(app, host='127.0.0.1', port=8080) 