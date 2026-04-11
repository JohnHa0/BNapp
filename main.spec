# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

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

# 确保 pip 被完整打包进来，供 GPU 在线安装使用
hiddenimports = collect_submodules('pip')
datas += collect_data_files('pip')

# ================= RAG / ChromaDB / PyMuPDF 依赖配置 =================
datas += collect_data_files('chromadb')
try:
    datas += collect_data_files('llama_cpp')
except Exception:
    pass
try:
    datas += collect_data_files('onnxruntime')
    datas += collect_data_files('tokenizers')
except Exception:
    pass
datas += copy_metadata('chromadb')
try:
    datas += copy_metadata('llama_cpp')
except Exception:
    pass
try:
    datas += copy_metadata('hnswlib')
    datas += copy_metadata('onnxruntime')
    datas += copy_metadata('tokenizers')
    datas += copy_metadata('pydantic')
    datas += copy_metadata('fastapi')
    datas += copy_metadata('uvicorn')
except Exception:
    pass

hiddenimports += collect_submodules('chromadb')
hiddenimports += collect_submodules('pydantic')
try:
    hiddenimports += collect_submodules('llama_cpp')
except Exception:
    pass
hiddenimports += [
    'fitz',  # PyMuPDF
    'chromadb.telemetry.product.posthog',
    'chromadb.api.segment',
    'chromadb.db.impl.sqlite',
    'hnswlib',
    'onnxruntime',
    'tokenizers',
    'uvicorn',
    'fastapi'
]
# ===================================================================

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
    upx=False,
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
    upx=False,
    upx_exclude=[],
    name='main',
)
