"""
This is a setup.py script generated for the FileOrganizer application.
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter'],
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': "文件整理工具",
        'CFBundleDisplayName': "文件整理工具",
        'CFBundleIdentifier': "com.acmes.fileorganizer",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2024 Acmes. All rights reserved."
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 