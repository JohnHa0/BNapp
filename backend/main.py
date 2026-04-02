from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import time
import sys
import os
import uvicorn
import subprocess
import pathlib

# [补丁] 强制全局 pathlib.Path.read_text 默认使用 UTF-8，解决 Windows GBK 编码崩溃
_original_read_text = pathlib.Path.read_text
def _patched_read_text(self, encoding=None, errors=None):
    if encoding is None:
        encoding = "utf-8"
    return _original_read_text(self, encoding=encoding, errors=errors)
pathlib.Path.read_text = _patched_read_text

# [补丁] 拦截并修复 scipy >= 1.14 删除了 gaussian 导致 arviz 0.16.1 崩溃的问题
try:
    import scipy.signal
    import scipy.signal.windows
    if not hasattr(scipy.signal, 'gaussian'):
        scipy.signal.gaussian = scipy.signal.windows.gaussian
except Exception:
    pass

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model_factory import build_dynamic_pymc_model, run_mcmc_sampling
from analyzer import extract_insights

app = FastAPI(title="DeepBayes 层次贝叶斯推理引擎 - v1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        df = pd.DataFrame(req.raw_data)
        
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
            
        model = build_dynamic_pymc_model(Y_obs, parsed_levels)
        trace = run_mcmc_sampling(model, req.sampling_mode, req.custom_draws, req.custom_tune)
        performance_data, summary_df, ppc_data, betas = extract_insights(trace, Y_obs, node_names)
        
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
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"后端引擎推理失败: {str(e)}")

@app.get("/api/system_info")
async def get_system_info():
    try:
        import jax
        devices = jax.devices()
        device_types = [str(d.device_kind) for d in devices]
        has_gpu = any("gpu" in d.lower() for d in device_types)
        return {
            "version": "1.0.0",
            "jax_version": jax.__version__,
            "devices": device_types,
            "has_gpu": has_gpu,
            "backend": "GPU" if has_gpu else "CPU"
        }
    except Exception as e:
        return {"version": "1.0.0", "backend": "Unknown", "error": str(e)}

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
        
        # 后台运行并捕捉关键过程 (这里使用 run 阻塞等待，前端通过 Loading 反馈)
        process = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=1800 # 30 分钟超时针对 1GB+ 的巨型包
        )
        
        if process.returncode == 0:
            return {"status": "success", "message": "GPU 驱动强化补丁安装成功！请重启软件。"}
        else:
            return {
                "status": "error", 
                "message": f"安装失败: {process.stderr[-200:]}", # 返回末尾错误日志
                "return_code": process.returncode
            }
            
    except Exception as e:
        return {"status": "error", "message": f"子进程执行异常: {str(e)}"}

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    uvicorn.run(app, host="127.0.0.1", port=18521)