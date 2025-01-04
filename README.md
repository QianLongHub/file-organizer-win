# 文件整理工具

一个简单实用的文件整理工具，帮助你自动整理文件夹中的各类文件。

## 功能特点

- 自动识别并分类常见文件类型
- 支持图片、文档、音频、视频、压缩包等多种文件格式
- 简洁直观的图形界面
- 实时显示整理进度
- 可以随时取消整理操作
- 支持自定义文件存放位置

## 支持的文件类型

- 图片：jpg, jpeg, png, gif, bmp, tiff, webp
- 文档：doc, docx, pdf, txt, rtf, odt, xls, xlsx, ppt, pptx
- 音频：mp3, wav, flac, m4a, aac, wma
- 视频：mp4, avi, mkv, mov, wmv, flv
- 压缩包：zip, rar, 7z, tar, gz
- 代码文件：py, java, cpp, html, css, js

## 使用方法

1. 运行程序
2. 点击"选择源文件夹"按钮选择需要整理的文件夹
3. 点击"开始整理"按钮
4. 等待程序扫描并分析文件
5. 查看整理结果
6. 点击"选择存放位置"按钮选择文件存放位置
7. 等待文件移动完成

## 下载

你可以从 [Releases](../../releases) 页面下载最新版本的程序。

## 开发环境

- Python 3.10
- tkinter (GUI库)
- PyInstaller (打包工具)

## 构建说明

如果你想自己构建程序：

1. 克隆仓库：
```bash
git clone https://github.com/YOUR_USERNAME/file-organizer.git
cd file-organizer
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python main.py
```

4. 构建可执行文件：
```bash
pyinstaller --clean file_organizer.spec
```

## 许可证

MIT License 