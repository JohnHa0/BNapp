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

# ─────────────────────── 日志自动清理 ───────────────────────
def _cleanup_old_logs(max_age_days=7):
    """清理超过 max_age_days 天的旧日志文件"""
    import glob
    import time as _time
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    log_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(log_dir):
        return
    
    now = _time.time()
    cutoff = now - (max_age_days * 86400)  # 86400 = 24*60*60
    cleaned = 0
    
    for f in glob.glob(os.path.join(log_dir, "*.log*")):
        try:
            if os.path.getmtime(f) < cutoff:
                os.remove(f)
                cleaned += 1
        except Exception:
            pass
    
    if cleaned > 0:
        logger.info(f"已清理 {cleaned} 个超过 {max_age_days} 天的旧日志文件")

_cleanup_old_logs()

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

# ─────────────────────── PyTensor / PyMC 运行时修正 ───────────────────────
def _setup_pytensor_for_frozen():
    """解决打包后 C Linker 找不到 _internal\\libs 的问题，彻底禁用 C 语言编译"""
    if not getattr(sys, 'frozen', False):
        return

    try:
        # 设置 PyTensor 编译缓存路径到用户本地目录 (避免安装目录无权限)
        user_local_appdata = os.environ.get("LOCALAPPDATA", os.path.join(os.path.expanduser("~"), "AppData", "Local"))
        app_data_dir = os.path.join(user_local_appdata, "DeepBayes", "pytensor_cache")
        os.makedirs(app_data_dir, exist_ok=True)
        
        # 核心修复: 禁用 C 语言后端的编译 (cxx="") 
        # 因为目标机器上往往没有安装 GCC/MSYS2，尝试调用 CLinker 会引发 WinError 3 (系统找不到指定的路径)
        # 禁用后会自动回退到纯 Python / NumPy 后端执行推演，兼容性最好。
        flags = f"device=cpu,floatX=float64,cxx=,optimizer=fast_compile,base_compiledir={app_data_dir}"
        os.environ["PYTENSOR_FLAGS"] = flags
        
        logger.info(f"开启打包兼容模式，PYTENSOR_FLAGS: {flags}")
             
    except Exception as e:
        logger.warning(f"PyTensor 运行时环境配置失败: {e}")

_setup_pytensor_for_frozen()

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

app = FastAPI(title="DeepBayes 层次贝叶斯推理引擎 - v1.0.2")

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

from scipy.spatial.distance import cdist

class BenchmarkRequest(BaseModel):
    project_features: Dict[str, float]
    historical_data: List[Dict[str, Any]]
    covariate_cols: List[str]
    betas: Dict[str, float]
    id_column: str
    target_column: str

@app.post("/api/benchmark")
async def benchmark_project(req: BenchmarkRequest):
    try:
        if not req.historical_data or not req.covariate_cols:
            raise ValueError("历史数据或协变量为空")
            
        df_hist = pd.DataFrame(req.historical_data)
        
        for cov in req.covariate_cols:
            if cov not in df_hist.columns:
                df_hist[cov] = 0.0
                
        X_hist = df_hist[req.covariate_cols].values
        X_new = np.array([[req.project_features.get(cov, 0.0) for cov in req.covariate_cols]])
        
        # Standardize for distance metric
        mean_X = np.mean(X_hist, axis=0)
        std_X = np.std(X_hist, axis=0) + 1e-8
        
        X_hist_std = (X_hist - mean_X) / std_X
        X_new_std = (X_new - mean_X) / std_X
        
        # Euclidean distance in normalized space
        distances = cdist(X_new_std, X_hist_std, metric='euclidean').flatten()
        df_hist['benchmark_distance'] = distances
        
        # Calculate expected score delta (sum of beta * standard_X)
        beta_array = np.array([req.betas.get(f"beta_{cov}", 0.0) for cov in req.covariate_cols])
        expected_delta = np.sum(X_new_std[0] * beta_array)
        
        # Get baseline expected. Approx mean of Y
        base_y = df_hist[req.target_column].mean() if req.target_column in df_hist.columns else 0.0
        expected_y = base_y + expected_delta
        
        # Top 3 closest matches
        top3 = df_hist.sort_values(by='benchmark_distance').head(3)
        
        matches = []
        for _, row in top3.iterrows():
            matches.append({
                "node_name": str(row.get(req.id_column, "Unknown")),
                "distance": float(row['benchmark_distance']),
                "actual_y": float(row.get(req.target_column, 0.0))
            })
            
        return {
            "status": "success",
            "expected_y": float(expected_y),
            "expected_delta": float(expected_delta),
            "matches": matches
        }
    except Exception as e:
        logger.exception(f"Benchmark 失败: {e}")
        raise HTTPException(status_code=500, detail=f"基准对标失败: {str(e)}")

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
            "version": "1.0.2",
            "jax_version": jax.__version__,
            "devices": device_types,
            "has_gpu": has_gpu,
            "backend": "GPU" if has_gpu else "CPU"
        }
    except Exception as e:
        logger.warning(f"JAX 检测失败 (正常，将使用 PyMC 原生采样): {e}")
        return {"version": "1.0.2", "backend": "CPU (PyMC)", "error": str(e)}

@app.post("/api/install_gpu_pack")
async def install_gpu_pack():
    """
    一键自动化安装 GPU 加速补丁 (JAX CUDA 支持)。
    onedir 打包模式下使用内嵌的 pip 直接安装到 _internal/ 目录。
    """
    mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    
    if getattr(sys, 'frozen', False):
        # ── onedir 打包模式：使用内嵌 pip 安装 ──
        try:
            # -------- PyInstaller PIP 补丁 --------
            # pip._vendor.distlib 找不到 finder 导致报错。手动为 PyInstaller 的 loader 注册 finder
            import pip._vendor.distlib.resources as distlib_res
            
            importer_type = type(sys.modules['pip._vendor.distlib'].__loader__)
            if importer_type not in distlib_res.finder_registry:
                class DummyResource:
                    def __init__(self, name, b):
                        self.name = name
                        self.bytes = b
                        
                class PyInstallerFinder:
                    def __init__(self, module):
                        self.module = module
                        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
                        if not os.path.basename(base_dir) == "_internal":
                            base_dir = os.path.join(base_dir, "_internal")
                        self.base_path = os.path.join(base_dir, module.__name__.replace('.', os.sep))
                        
                    def find(self, resource_name):
                        p = os.path.join(self.base_path, resource_name.replace('/', os.sep))
                        if os.path.exists(p):
                            with open(p, 'rb') as f:
                                return DummyResource(resource_name, f.read())
                        return None
                        
                    def iterator(self, resource_name):
                        p = os.path.join(self.base_path, resource_name.replace('/', os.sep))
                        if os.path.isdir(p):
                            for fname in os.listdir(p):
                                rp = os.path.join(p, fname)
                                if os.path.isfile(rp):
                                    with open(rp, 'rb') as f:
                                        res_name = f"{resource_name}/{fname}" if resource_name else fname
                                        yield DummyResource(res_name, f.read())
                                        
                distlib_res.finder_registry[importer_type] = PyInstallerFinder
                logger.info("已成功注册 PyInstaller PIP 资源扫描器钩子。")
            # --------------------------------------
            from pip._internal.cli.main import main as pip_main
        except ImportError:
            logger.error("内嵌 pip 模块未找到")
            return {
                "status": "error",
                "message": "内部 pip 模块缺失，请联系开发者重新打包。"
            }
        
        # 安装目标：_internal/ 目录（PyInstaller onedir 的运行时目录）
        internal_dir = os.path.dirname(sys.executable)
        internal_path = os.path.join(internal_dir, "_internal")
        if not os.path.isdir(internal_path):
            internal_path = internal_dir  # fallback
        
        logger.info(f"使用内嵌 pip 安装到: {internal_path}")
        
        try:
            # 在子线程中运行 pip，避免阻塞事件循环
            import asyncio
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: pip_main([
                    "install", "jax[cuda12]",
                    "--target", internal_path,
                    "-i", mirror_url,
                    "--no-warn-script-location",
                    "--quiet"
                ])
            )
            
            if result == 0:
                logger.info("GPU 补丁安装成功！")
                return {"status": "success", "message": "GPU 加速组件安装成功！请重启软件以生效。"}
            else:
                logger.error(f"pip install 返回码: {result}")
                return {"status": "error", "message": f"安装失败 (返回码 {result})。\n请检查网络连接或磁盘空间。"}
                
        except Exception as e:
            logger.exception(f"GPU 安装异常: {e}")
            return {"status": "error", "message": f"安装过程出错: {str(e)}"}
    
    else:
        # ── 开发模式：直接用当前 Python 的 pip ──
        try:
            cmd = [sys.executable, "-m", "pip", "install", "jax[cuda12]", "-i", mirror_url]
            
            logger.info(f"开始安装 GPU 补丁: {' '.join(cmd)}")
            process = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=1800
            )
            
            if process.returncode == 0:
                logger.info("GPU 补丁安装成功！")
                return {"status": "success", "message": "GPU 驱动强化补丁安装成功！请重启软件。"}
            else:
                error_msg = (process.stderr or '').strip()[-500:] or '未知错误'
                logger.error(f"GPU 补丁安装失败: {error_msg}")
                return {
                    "status": "error", 
                    "message": f"安装失败: {error_msg[-200:]}",
                    "return_code": process.returncode
                }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "安装超时，请检查网络连接后重试。"}
        except Exception as e:
            logger.exception(f"GPU 安装异常: {e}")
            return {"status": "error", "message": f"子进程执行异常: {str(e)}"}

def _kill_process_on_port(port: int):
    """在 Windows 上查找并杀死占用指定端口的进程，防止 Errno 10048"""
    import socket
    import time as _time
    
    def _is_port_free(p):
        """True = 端口可用，False = 被占用"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', p)) != 0
    
    try:
        if _is_port_free(port):
            logger.info(f"端口 {port} 空闲，无需清理")
            return
        
        logger.warning(f"端口 {port} 已被占用，正在尝试释放...")
        
        # 第一轮：用 netstat 找 PID 并 taskkill
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True, text=True, timeout=10
        )
        
        target_pids = set()
        for line in result.stdout.splitlines():
            if f'127.0.0.1:{port}' in line or f'0.0.0.0:{port}' in line:
                if 'LISTENING' in line or 'ESTABLISHED' in line:
                    parts = line.strip().split()
                    if parts:
                        try:
                            pid = int(parts[-1])
                            if pid != os.getpid() and pid > 0:
                                target_pids.add(pid)
                        except ValueError:
                            pass
        
        for pid in target_pids:
            logger.info(f"正在终止占用端口的进程 PID={pid}")
            try:
                # /T = 同时终止子进程树
                subprocess.run(
                    ['taskkill', '/F', '/T', '/PID', str(pid)],
                    capture_output=True, timeout=10
                )
            except Exception as e:
                logger.warning(f"终止进程 {pid} 失败: {e}")
        
        # 第二轮：反复验证端口是否已释放（最多等 8 秒）
        for i in range(16):
            _time.sleep(0.5)
            if _is_port_free(port):
                logger.info(f"端口 {port} 已成功释放（等待了 {(i+1)*0.5:.1f} 秒）")
                return
        
        # 第三轮：如果还是没释放，尝试杀死所有名为 main.exe 的进程
        logger.warning(f"端口 {port} 仍未释放，尝试杀死所有 main.exe 进程...")
        try:
            subprocess.run(
                ['taskkill', '/F', '/IM', 'main.exe'],
                capture_output=True, timeout=10
            )
        except Exception:
            pass
        
        # 最后再等 2 秒
        _time.sleep(2)
        if _is_port_free(port):
            logger.info(f"端口 {port} 最终清理成功")
        else:
            logger.error(f"端口 {port} 始终无法释放，服务可能启动失败")
            
    except Exception as e:
        logger.warning(f"端口清理过程出错（将继续尝试启动）: {e}")


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    port = int(os.environ.get("DEEPBAYES_PORT", "18521"))
    
    # 启动前清理：杀死之前残留的后端进程
    _kill_process_on_port(port)
    
    logger.info(f"启动 FastAPI 服务器 -> http://127.0.0.1:{port}")
    
    # 增加重试机制，解决 Windows 端口释放延迟导致的 Errno 10048
    max_retries = 5
    for attempt in range(max_retries):
        try:
            uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
            break
        except Exception as e:
            if "10048" in str(e) and attempt < max_retries - 1:
                logger.warning(f"端口绑定失败 (重试 {attempt+1}/{max_retries})...")
                time.sleep(1.5)
            else:
                logger.error(f"无法启动服务器: {e}")
                raise e