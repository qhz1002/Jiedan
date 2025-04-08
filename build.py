import os
import sys
import subprocess
from pathlib import Path

def create_spec_file(script_path):
    # 获取 playwright 包路径
    playwright_path = os.path.join(sys.prefix, 'Lib', 'site-packages', 'playwright')

    # 浏览器路径（位于 site-packages/playwright/driver/package/.local-browsers）
    browsers_path = os.path.join(playwright_path, 'driver', 'package', '.local-browsers')

    # 确保 playwright_path 和 browsers_path 存在
    if not os.path.exists(playwright_path):
        raise FileNotFoundError(f"Playwright path not found: {playwright_path}")
    if not os.path.exists(browsers_path):
        raise FileNotFoundError(f"Browsers path not found: {browsers_path}")

    # 列出所有浏览器目录（动态获取，避免硬编码版本号）
    browser_dirs = [d for d in os.listdir(browsers_path) if os.path.isdir(os.path.join(browsers_path, d))]

    # 构建 datas 列表，包含所有浏览器目录
    datas = [
        (os.path.join(playwright_path, "driver"), 'playwright/driver')  # 直接计算路径
    ]
    for browser_dir in browser_dirs:
        browser_dir_path = os.path.join(browsers_path, browser_dir)
        target_path = f'playwright/driver/package/.local-browsers/{browser_dir}'
        datas.append((browser_dir_path, target_path))

    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

a = Analysis(
    ['{script_path}'],
    pathex=[],
    binaries=[],
    datas={datas},
    hiddenimports=[
        'playwright',
        'playwright.sync_api',
        'playwright._impl._driver',
        'playwright._impl._connection',
        'playwright._impl._browser_type',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # 包含所有二进制文件到单个文件中
    a.zipfiles,
    a.datas,
    name='playwright_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    onefile=True  # 启用单文件模式
)
'''

    with open('build.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

def build_executable():
    """构建可执行文件"""
    try:
        create_spec_file('main.py')
        subprocess.run([
            'pyinstaller',
            '--clean',
            '--log-level', 'DEBUG',
            'build.spec'
        ], check=True)
        print("打包成功！")
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")

if __name__ == '__main__':
    build_executable()