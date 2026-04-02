# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['backend\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'matplotlib', 'matplotlib.backends.backend_agg',
        'arviz', 'arviz.plots',
        'scipy.special.cython_special',
        'scipy.signal.windows',
        'pkg_resources.extern',
        'logging.handlers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # GUI 工具包（后端不需要显示窗口，只需 Agg 渲染器）
        'tkinter', '_tkinter', 'tkinter.filedialog',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_qt4agg',
        'matplotlib.backends.backend_wxagg',
        'matplotlib.backends.backend_gtk3agg',
        'matplotlib.backends.backend_gtk4agg',
        'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'wx', 'gi',
        # 交互式 / 开发工具
        'IPython', 'notebook', 'jupyter', 'jedi', 'pygments',
        'pytest', 'doctest', 'unittest', 'pdb',
        # 图像处理（不需要）
        'PIL', 'Pillow',
        # 网络 / IO（后端自己有 uvicorn，不需要 tornado）
        'tornado',
        # 其他大型未使用模块
        'sqlite3', 'curses',
    ],
    noarchive=False,
    optimize=2,
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
