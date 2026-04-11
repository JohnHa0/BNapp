import os
import sys
import json
import uuid
import datetime
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
import requests

# Set up logging matching main
import logging
logger = logging.getLogger("deepbayes.settings")

router = APIRouter(prefix="/api/settings")

# ─────────────────── CONFIGURATION STORE ───────────────────
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".deepbayes", "config.json")
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"provider": "ollama", "ollama_host": "http://127.0.0.1:11434", "ollama_model": "qwen", "gguf_path": ""}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

class LlmConfig(BaseModel):
    provider: str
    ollama_host: str
    ollama_model: str
    gguf_path: str = ""

@router.get("/get")
def get_settings():
    return load_config()

@router.post("/llm/test")
def test_llm(cfg: LlmConfig):
    save_config(cfg.model_dump())
    
    if cfg.provider == "ollama":
        try:
            url = f"{cfg.ollama_host.rstrip('/')}/api/tags"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                models = [m.get("name") for m in data.get("models", [])]
                if any(cfg.ollama_model in m for m in models):
                    return {"status": "success", "msg": "Connected to Ollama!"}
                else:
                    raise HTTPException(status_code=400, detail=f"Ollama connected, but model '{cfg.ollama_model}' not found. Available: {', '.join(models)}")
            raise HTTPException(status_code=400, detail=f"Ollama returned {res.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            raise HTTPException(status_code=400, detail="Cannot connect to Ollama service.")
            
    elif cfg.provider == "llama_cpp":
        return {"status": "success", "msg": "Built-in engine selected. Models will be loaded dynamically."}

    raise HTTPException(status_code=400, detail="Unknown provider")


@router.get("/local_models")
def list_local_models():
    """Scan ~/.deepbayes/models for .gguf files"""
    models_dir = os.path.join(os.path.expanduser("~"), ".deepbayes", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    gguf_files = []
    for f in os.listdir(models_dir):
        if f.endswith(".gguf"):
            path = os.path.join(models_dir, f)
            size_mb = os.path.getsize(path) / (1024 * 1024)
            gguf_files.append({
                "name": f,
                "size_mb": round(size_mb, 1),
                "path": path
            })
            
    return {"models": gguf_files, "models_dir": models_dir}

@router.get("/open_models_dir")
def open_models_dir():
    """Open models directory in OS file explorer"""
    models_dir = os.path.join(os.path.expanduser("~"), ".deepbayes", "models")
    os.makedirs(models_dir, exist_ok=True)
    import subprocess
    if os.name == 'nt':
        os.startfile(models_dir)
    elif sys.platform == 'darwin':
        subprocess.call(['open', models_dir])
    else:
        subprocess.call(['xdg-open', models_dir])
    return {"status": "success"}


# ─────────────────── RAG & DATABASE ───────────────────
RAG_DB_DIR = os.path.join(os.path.expanduser("~"), ".deepbayes", "knowledge_base")
os.makedirs(RAG_DB_DIR, exist_ok=True)

# Safe load ChromaDB (graceful degradation)
chroma_client = None
try:
    import chromadb
    from chromadb.config import Settings
    chroma_client = chromadb.PersistentClient(path=RAG_DB_DIR)
    collection = chroma_client.get_or_create_collection(name="strategy_docs")
    logger.info(f"ChromaDB initialized at {RAG_DB_DIR}")
except ImportError:
    logger.warning("chromadb not installed. RAG features will be disabled.")
    collection = None

@router.get("/rag/list")
def list_rag_files():
    if not collection:
        return {"files": []}
    
    # We store the "file logic" in the collection metadata or by querying unique source tags
    try:
        results = collection.get()
        # Group by source
        files_map = {}
        metadatas = results.get("metadatas", []) or []
        for meta in metadatas:
            source = meta.get("source", "unknown")
            file_id = meta.get("file_id", "unknown")
            ts = meta.get("timestamp", "")
            if file_id not in files_map:
                files_map[file_id] = {"id": file_id, "name": source, "chunks": 0, "timestamp": ts}
            files_map[file_id]["chunks"] += 1
            
        return {"files": list(files_map.values())}
    except Exception as e:
        logger.error(f"Failed to list RAG files: {e}")
        return {"files": []}

@router.delete("/rag/delete/{file_id}")
def delete_rag_file(file_id: str):
    if not collection:
        raise HTTPException(status_code=500, detail="Database offline")
    collection.delete(where={"file_id": file_id})
    return {"status": "success"}

@router.post("/rag/upload")
def upload_rag_file(files: list[UploadFile] = File(...)):
    if not collection:
        raise HTTPException(status_code=500, detail="Database offline. Install chromadb.")
        
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise HTTPException(status_code=500, detail="PyMuPDF not installed. Cannot parse PDFs.")

    new_ids = []
    
    for file in files:
        file_id = str(uuid.uuid4())[:8]
        content = ""
        # Save temp file
        temp_path = f"/tmp/{file.filename}" if not os.name == 'nt' else f"{os.getenv('TEMP')}\\{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
            
        # Parse content
        if file.filename.endswith(".pdf"):
            doc = fitz.open(temp_path)
            for page in doc:
                content += page.get_text() + "\n\n"
            doc.close()  # VERY IMPORTANT FOR WINDOWS
        elif file.filename.endswith(".txt"):
            with open(temp_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {file.filename}")
            
        os.remove(temp_path)
        
        # Simple Text Splitter (approx 500 chars per chunk w/ overlap)
        chunks = []
        chunk_size = 500
        overlap = 100
        start = 0
        while start < len(content):
            chunks.append(content[start:start+chunk_size])
            start += chunk_size - overlap
            
        if not chunks:
            continue
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Insert to DB
        ids = [f"{file_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file.filename, "file_id": file_id, "timestamp": timestamp} for _ in chunks]
        
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        new_ids.append(file_id)
        
    return {"status": "success", "imported": new_ids}


# ─────────────────── RAG + LLM PIPELINE ───────────────────
from fastapi.responses import StreamingResponse

class ShockData(BaseModel):
    shock_type: str
    var_drop: float
    trigger_node: str = ""
    top_fragile: list = []
    top_resilient: list = []

@router.post("/llm/stream_decision")
def stream_decision(data: ShockData):
    cfg = load_config()
    
    # 1. RAG Retrieval
    context = ""
    if collection:
        try:
            # Create a simple query based on the shock
            query = f"风险应对预案，节点崩溃：{data.trigger_node}，系统效能下降。防御与恢复策略。"
            results = collection.query(query_texts=[query], n_results=3)
            docs = results.get("documents", [])
            if docs and len(docs) > 0 and len(docs[0]) > 0:
                context = "\n\n".join(docs[0])
        except Exception as e:
            logger.warning(f"RAG query failed: {e}")
            
    # 2. Build Prompt
    prompt = f"""你现在是 DeepBayes 平台的首席安全与战略专家（CISO）。目前系统遭遇了一次极端安全冲击（压力测试）。
冲击类型：{data.shock_type}
系统大盘整体破坏均值 (VAR)：{data.var_drop:.3f}
触发此破坏的核心节点：{data.trigger_node}
最脆弱的资产节点：{", ".join(data.top_fragile)}
最能扛压的韧性资产：{", ".join(data.top_resilient)}

请结合以上数据，给出战术性的行动指导，包括防守建议和资金调配规划。"""

    if context:
        prompt += f"\n\n【参考战略智库预案文献片段】：\n{context}\n\n请在你的回答中引用文献中的防卫建议（如果有的话）。"

    # 3. Stream from LLM
    if cfg["provider"] == "ollama":
        url = f"{cfg['ollama_host'].rstrip('/')}/api/generate"
        payload = {
            "model": cfg["ollama_model"],
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": 0.3}
        }
        
        def ollama_stream():
            try:
                import json
                with requests.post(url, json=payload, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    for line in r.iter_lines():
                        if line:
                            decoded = json.loads(line.decode('utf-8'))
                            if "response" in decoded:
                                yield decoded["response"]
            except Exception as e:
                yield f"\n[连接大模型引擎中断: {str(e)}]"
                
        return StreamingResponse(ollama_stream(), media_type="text/plain")
        
    elif cfg["provider"] == "llama_cpp":
        def gguf_stream():
            try:
                from llama_cpp import Llama
            except ImportError:
                yield "【错误：尚未安装本地推理底层核心 (llama-cpp-python)】\n\n"
                yield "由于架构原因，请在终端（需 C++ 编译环境或拉取预编译包）手工安装该组件：\n> pip install llama-cpp-python\n"
                return
                
            gguf_path = cfg.get("gguf_path", "")
            if not gguf_path or not os.path.exists(gguf_path):
                yield "【模型错误：未找到指定的 GGUF 模型文件】\n请点击右上角齿轮 -> 本地 GGUF 库，选择并挂载一个您下载的实装模型。"
                return
                
            yield "【正挂载核心，启用极耗算力的本地推理，请耐心等待...】\n\n"
            try:
                # Lazy load model (only when needed to save RAM)
                llm = Llama(model_path=gguf_path, n_ctx=2048, verbose=False)
                
                # Instruction format adjustments for Qwen/Llama3 could be complex. Simply supplying the prompt usually falls back gracefully.
                full_prompt = f"System: 你是系统安全防卫终端战略参谋。\nUser: {prompt}\nAssistant:"
                
                stream = llm.create_completion(
                    full_prompt,
                    max_tokens=600,
                    stop=["User:", "\n\n\n"],
                    stream=True,
                    temperature=0.3
                )
                for chunk in stream:
                    text = chunk.get("choices", [{}])[0].get("text", "")
                    if text:
                        yield text
            except Exception as e:
                yield f"\n[引擎矩阵推理发生崩溃: {str(e)}]"
                
        return StreamingResponse(gguf_stream(), media_type="text/plain")
