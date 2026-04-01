from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import uvicorn

from model_factory import build_dynamic_pymc_model, run_mcmc_sampling
from analyzer import extract_insights

app = FastAPI(title="视频侦查效能评估 - 层次贝叶斯引擎")

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

@app.post("/api/run_inference")
async def run_inference(req: InferenceRequest):
    try:
        df = pd.DataFrame(req.raw_data)
        Y_obs = df[req.target_variable.name].values
        
        # 提取最底层节点名称 (战术层)
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
        trace = run_mcmc_sampling(model)
        performance_data, summary_df = extract_insights(trace, Y_obs, node_names)
        
        return {
            "status": "success", 
            "results": {
                "performance_data": performance_data, 
                "summary_df": summary_df
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"后端引擎推理失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)