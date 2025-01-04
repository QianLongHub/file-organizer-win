@echo off

REM 安装依赖
pip install -r requirements.txt

REM 使用 PyInstaller 打包
pyinstaller --name="FileOrganizer" ^
            --windowed ^
            --add-data "index.html;." ^
            --icon="icon.ico" ^
            --clean ^
            main.py

echo 打包完成！可执行文件位于 dist\FileOrganizer\FileOrganizer.exe 