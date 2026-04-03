# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# 收集运行时需要的静态数据文件
# - arviz: HTML 模板、CSS、图标
# - matplotlib: 字体、配色方案
# - pytensor: C 源码文件（运行时编译张量运算节点）
datas = []
datas += collect_data_files('arviz')
datas += collect_data_files('matplotlib')
datas += collect_data_files('pytensor')

# pytensor -> cons -> unification 依赖链在运行时通过 importlib.metadata
# 查询包版本，必须手动收集这些包的 dist-info 元数据
datas += copy_metadata('logical-unification')
datas += copy_metadata('cons')
datas += copy_metadata('etuples')
datas += copy_metadata('miniKanren')
datas += copy_metadata('pytensor')
datas += copy_metadata('pymc')
datas += copy_metadata('arviz')

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
