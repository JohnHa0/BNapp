import warnings
import os
import sys
import logging
import logging.handlers

# ─────────────────────── 日志系统初始化 ───────────────────────
# 日志文件保存在 exe 同级的 logs/ 目录下，方便打包后排查问题
def _setup_logging():
    """初始化本地文件日志系统，同时输出到控制台和文件"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后
        base_dir = os.path.dirname(sys.executable)
    else:
        # 开发模式
        base_dir = os.path.dirname(os.path.abspath(__file__))

    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "deepbayes_backend.log")

    # 文件 Handler：RotatingFileHandler 防止日志无限膨胀（最大 5MB，保留 3 个备份）
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    # 控制台 Handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "[%(levelname)s] %(message)s"
    ))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return logging.getLogger("deepbayes")

logger = _setup_logging()
logger.info("=" * 60)
logger.info("DeepBayes Backend 启动中...")
logger.info(f"Python: {sys.version}")
logger.info(f"Frozen: {getattr(sys, 'frozen', False)}")
logger.info(f"Executable: {sys.executable}")
logger.info("=" * 60)

# ─────────────────────── 抑制无害警告 ───────────────────────
# pytensor BLAS 告警（pip 安装时常见，不影响计算正确性，仅速度略慢）
warnings.filterwarnings("ignore", message=".*PyTensor could not link to a BLAS.*")
warnings.filterwarnings("ignore", category=UserWarning, module="pytensor")
os.environ.setdefault("PYTENSOR_FLAGS", "device=cpu,floatX=float64,optimizer=fast_compile")

# matplotlib: 强制使用非交互式后端，避免打包后找不到 Tk/Qt
os.environ.setdefault("MPLBACKEND", "Agg")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import time
import uvicorn
import subprocess
import pathlib

# [进度条捕获钩子] 拦截 PyMC/tqdm 的输出，提取最新的一行进度
class OutputGrabber:
    def __init__(self):
        self.lines = []
        self.current_line = ""
        self.original_stderr = sys.stderr
        self.original_stdout = sys.stdout

    def write(self, text):
        self.original_stderr.write(text)
        for char in text:
            if char == '\r':
                self.current_line = "" # 回车时覆盖当前行（tqdm 动画原理）
            elif char == '\n':
                if self.current_line.strip():
                    self.lines.append(self.current_line)
                self.current_line = ""
            else:
                self.current_line += char
        if len(self.lines) > 50:
             self.lines = self.lines[-50:]

    def flush(self):
        self.original_stderr.flush()
        self.original_stdout.flush()

    def get_latest(self):
        if self.current_line.strip():
            return self.current_line.strip()
        if self.lines:
            return self.lines[-1].strip()
        return ""
    
    def clear(self):
        self.lines = []
        self.current_line = ""

    def isatty(self):
        return False

    def fileno(self):
        return self.original_stderr.fileno()

    @property
    def encoding(self):
        return self.original_stderr.encoding

output_grabber = OutputGrabber()
sys.stderr = output_grabber
sys.stdout = output_grabber


# [补丁] 强制全局 pathlib.Path.read_text 默认使用 UTF-8，解决 Windows GBK 编码崩溃
_original_read_text = pathlib.Path.read_text
def _patched_read_text(self, encoding=None, errors=None):
    if encoding is None:
        encoding = "utf-8"
    return _original_read_text(self, encoding=encoding, errors=errors)
pathlib.Path.read_text = _patched_read_text

# [补丁] 拦截并修复 scipy >= 1.14 删除了 gaussian 导致 arviz 崩溃的问题
try:
    import scipy.signal
    import scipy.signal.windows
    if not hasattr(scipy.signal, 'gaussian'):
        scipy.signal.gaussian = scipy.signal.windows.gaussian
except Exception:
    pass

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logger.info("正在加载 PyMC / Arviz 核心模块...")
try:
    from model_factory import build_dynamic_pymc_model, run_mcmc_sampling
    from analyzer import extract_insights
    logger.info("核心模块加载成功！")
except Exception as e:
    logger.exception(f"核心模块加载失败: {e}")
    raise

app = FastAPI(title="DeepBayes 层次贝叶斯推理引擎 - v1.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """轻量健康检查端点，前端用来判断后端是否已就绪"""
    return {"status": "ok"}

class SchemaLevel(BaseModel):
    level_index: int
    level_name: str
    id_column: str
    covariates: List[str]

class TargetVariable(BaseModel):
    name: str
    type: str

class InferenceRequest(BaseModel):
    project_name: str
    target_variable: TargetVariable
    hierarchy: List[SchemaLevel]
    raw_data: List[Dict[str, Any]]
    sampling_mode: Optional[str] = "fast"
    custom_draws: Optional[int] = None
    custom_tune: Optional[int] = None

import traceback

@app.post("/api/run_inference")
async def run_inference(req: InferenceRequest):
    output_grabber.clear()
    logger.info(f"收到推理请求: project={req.project_name}, mode={req.sampling_mode}")
    try:
        df = pd.DataFrame(req.raw_data)
        logger.info(f"数据集: {len(df)} 行, {len(df.columns)} 列")
        
        # 稳健的数据预处理：强制转换数值型并剔除含有空值的行
        id_cols = [l.id_column for l in req.hierarchy if l.id_column]
        cov_cols = [cov for l in req.hierarchy for cov in l.covariates]
        target_col = req.target_variable.name
        
        numeric_cols = cov_cols + [target_col]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        present_cols = [c for c in (id_cols + numeric_cols) if c in df.columns]
        df = df.dropna(subset=present_cols).copy()
        
        if len(df) == 0:
             raise ValueError("解析后发现所有行均包含空值或格式错误的数据，中止计算。")
             
        Y_obs = df[req.target_variable.name].values
        
        # 提取最底层节点名称
        bottom_level_id = req.hierarchy[-1].id_column
        node_names = df[bottom_level_id].values
        
        parsed_levels = {}
        for level in req.hierarchy:
            idx = pd.Categorical(df[level.id_column]).codes
            n_nodes = len(df[level.id_column].unique())
            
            if level.covariates:
                X_matrix = df[level.covariates].values
                # 标准化处理防止梯度爆炸
                X_matrix = (X_matrix - np.mean(X_matrix, axis=0)) / (np.std(X_matrix, axis=0) + 1e-8)
            else:
                X_matrix = None
                
            parsed_levels[level.level_index] = {
                "name": level.level_name,
                "idx": idx,
                "n_nodes": n_nodes,
                "X": X_matrix,
                "cov_names": level.covariates
            }
        
        logger.info("模型构建中...")
        model = build_dynamic_pymc_model(Y_obs, parsed_levels)
        logger.info("MCMC 采样中...")
        trace = run_mcmc_sampling(model, req.sampling_mode, req.custom_draws, req.custom_tune)
        logger.info("提取分析结果...")
        performance_data, summary_df, ppc_data, betas = extract_insights(trace, Y_obs, node_names)
        
        logger.info("推理完成！")
        return {
            "status": "success", 
            "results": {
                "performance_data": performance_data, 
                "summary_df": summary_df,
                "ppc_data": ppc_data,
                "betas": betas
            }
        }
        
    except Exception as e:
        logger.exception(f"推理失败: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"后端引擎推理失败: {str(e)}")

@app.get("/api/logs")
async def get_logs():
    return {"log": output_grabber.get_latest()}

@app.get("/api/system_info")
async def get_system_info():
    try:
        import jax
        devices = jax.devices()
        device_types = [str(d.device_kind) for d in devices]
        has_gpu = any("gpu" in d.lower() for d in device_types)
        logger.info(f"系统信息: JAX {jax.__version__}, devices={device_types}")
        return {
            "version": "1.0.1",
            "jax_version": jax.__version__,
            "devices": device_types,
            "has_gpu": has_gpu,
            "backend": "GPU" if has_gpu else "CPU"
        }
    except Exception as e:
        logger.warning(f"JAX 检测失败 (正常，将使用 PyMC 原生采样): {e}")
        return {"version": "1.0.1", "backend": "CPU (PyMC)", "error": str(e)}

@app.post("/api/install_gpu_pack")
async def install_gpu_pack():
    """
    一键自动化安装 GPU 加速补丁 (JAX CUDA 支持)。
    专门配置了国内清华大学 Tuna 镜像以适配中国地区宽带。
    """
    try:
        # 使用当前 Python 解释器执行安装，确保环境正确
        python_exe = sys.executable
        # 指定清华源提升下载速度
        mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
        
        # 核心包：目前主流为 cuda12
        cmd = [python_exe, "-m", "pip", "install", "jax[cuda12]", "-i", mirror_url]
        
        logger.info(f"开始安装 GPU 补丁: {' '.join(cmd)}")
        process = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=1800 # 30 分钟超时针对 1GB+ 的巨型包
        )
        
        if process.returncode == 0:
            logger.info("GPU 补丁安装成功！")
            return {"status": "success", "message": "GPU 驱动强化补丁安装成功！请重启软件。"}
        else:
            logger.error(f"GPU 补丁安装失败: {process.stderr[-500:]}")
            return {
                "status": "error", 
                "message": f"安装失败: {process.stderr[-200:]}", # 返回末尾错误日志
                "return_code": process.returncode
            }
            
    except Exception as e:
        logger.exception(f"GPU 安装异常: {e}")
        return {"status": "error", "message": f"子进程执行异常: {str(e)}"}

def _kill_process_on_port(port: int):
    """在 Windows 上查找并杀死占用指定端口的进程，防止 Errno 10048"""
    try:
        import socket
        # 先快速检测端口是否真的被占用
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            if result != 0:
                # 端口空闲，无需处理
                return
        
        logger.warning(f"端口 {port} 已被占用，正在尝试释放...")
        
        # 使用 netstat 找到占用端口的 PID
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True, text=True, timeout=10
        )
        
        target_pids = set()
        for line in result.stdout.splitlines():
            # 匹配 LISTENING 状态的 127.0.0.1:port
            if f'127.0.0.1:{port}' in line and 'LISTENING' in line:
                parts = line.strip().split()
                if parts:
                    try:
                        pid = int(parts[-1])
                        if pid != os.getpid():  # 不要杀死自己
                            target_pids.add(pid)
                    except ValueError:
                        pass
        
        for pid in target_pids:
            logger.info(f"正在终止占用端口的进程 PID={pid}")
            try:
                subprocess.run(
                    ['taskkill', '/F', '/PID', str(pid)],
                    capture_output=True, timeout=10
                )
            except Exception as e:
                logger.warning(f"终止进程 {pid} 失败: {e}")
        
        if target_pids:
            import time as _time
            _time.sleep(1)  # 等待端口释放
            logger.info(f"端口 {port} 清理完成")
            
    except Exception as e:
        logger.warning(f"端口清理过程出错（将继续尝试启动）: {e}")


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    port = int(os.environ.get("DEEPBAYES_PORT", "18521"))
    
    # 启动前清理：杀死之前残留的后端进程
    _kill_process_on_port(port)
    
    logger.info(f"启动 FastAPI 服务器 -> http://127.0.0.1:{port}")
    uvicorn.run(app, host="127.0.0.1", port=port)