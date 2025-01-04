#!/bin/bash

# 安装依赖
pip3 install -r requirements.txt

# 使用 PyInstaller 打包
pyinstaller --name="文件整理工具" \
            --windowed \
            --add-data "index.html:." \
            --icon="icon.icns" \
            --clean \
            main.py

echo "打包完成！可执行文件位于 dist/文件整理工具.app" 