# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# 确保 arviz/pymc 等包的数据文件被正确收集
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

# 确保 pip 被打包进来，供 GPU 在线安装使用
hiddenimports = [
    'pip',
    'pip._internal',
    'pip._internal.cli',
    'pip._internal.cli.main',
    'pip._vendor',
]

a = Analysis(
    ['backend/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'IPython', 'notebook', 'jedi', 'pygments', 'pytest', 'tornado', 'PyQt5', 'PyQt6'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

# --onedir 模式：exe 只包含启动器，依赖文件由 COLLECT 收集到 _internal/
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,   # ← 关键：不把 binaries/datas 塞进 exe
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# COLLECT：将所有依赖收集到 dist-backend/main/ 目录（避免与 Vite 的 dist/ 冲突）
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
