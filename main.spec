# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 收集运行时需要的静态数据文件
# - arviz: HTML 模板、CSS、图标
# - matplotlib: 字体、配色方案
# - pytensor: C 源码文件（运行时编译张量运算节点）
datas = []
datas += collect_data_files('arviz')
datas += collect_data_files('matplotlib')
datas += collect_data_files('pytensor')

a = Analysis(
    ['backend\\main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'IPython', 'notebook', 'jedi', 'pygments', 'pytest', 'tornado', 'PyQt5', 'PyQt6'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
