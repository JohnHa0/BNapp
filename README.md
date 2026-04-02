# BNapp - HB Eval System

This project is a Tauri-based application with a Vue.js frontend and a FastAPI backend.

## Environment Setup

### 1. Node.js (Frontend)

We use `nvm` to manage Node.js versions.

```bash
# Install the correct Node.js version
nvm install

# Use the correct version
nvm use
```

Then, install dependencies:

```bash
npm install
```

### 2. Python (Backend)

We use `conda` to manage the Python environment.

```bash
# Create the environment
conda env create bnapp -f backend/environment.yml

# Activate the environment
conda activate bnapp-backend
```

### 3. Rust (Tauri v2)
Ensure you have Rust installed. This project uses **Tauri v2**.
```bash
# Add necessary plugins if not present
# npm run tauri plugin add dialog fs shell
```

## Performance Optimization (Crucial)
If you see a `BLAS installation` warning in the backend logs, it means the math engine is running in slow-motion.
To fix this and get a **10x speed boost**, ensure JAX is synchronized:
```bash
conda activate bnapp-backend
pip install --upgrade jax jaxlib numpyro
```

## Development

### Running the Frontend

```bash
npm run dev
```

### Running the Backend

```bash
cd backend
uvicorn main:app --reload
```

### Running the Tauri App

```bash
npm run tauri dev
```

## Project Structure

- `src/`: Frontend Vue.js source code (incl. DataImporter & VisualizationDashboard).
- `src-tauri/`: Tauri backend source code (Rust), providing desktop app envelope.
- `backend/`: FastAPI backend source code (Python). Connects to PyMC for MCMC sampling.
- `软件需求说明文档.md`: Software requirement specification (detailed usage guides and module outlines).

## Key Features
- **Hierarchical Network Builder**: Drag-and-drop mechanism to visually map covariates and ID columns to dynamic DAG levels.
- **Fast / Accurate Sampling**: Built-in toggle to switch between 500/300 (fast preview) and 1500/1000 (accurate precision) NUTS sampling modes. Customizable parameter injection available.
- **GIS Map View**: Built-in scatter and rippling effect maps for geographical analytics (Lat/Lng support).
- **Domain Scenarios**: Comes with 4 domain-specific sandbox presets, including a complex 4-tier geopolitical conflict map.
- **Native OS Integration**: Uses Tauri v2 Native Dialogs for a premium file saving experience (CSV/PNG).
- **Real-time Engine Logs**: Frontend control-center streams live MCMC sampling progress directly from the Python sub-process.

## 推送更新
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
git tag v1.0.0
git push origin v1.0.0
## 本地打包
- 初始化 PowerShell 扩展：conda init powershell，重启终端以生效
- 激活环境：conda activate bnapp-backend
- 运行脚本：.\scripts\build-local.ps1
### 冲突消解
本地和云端分支不一样的问题：

方案一：统一名称（最推荐、一劳永逸）
将本地的 main 分支重命名为 master，让本地和云端完全一致。以后您只需要盲敲 git push 和 git pull 即可，一切都会非常丝滑。

在终端中只需执行下面两行代码即可：

bash
# 1. 将本地分支改名为 master
git branch -m main master
# 2. 将本地 master 与远端 master 绑定
git push -u origin master
方案二：保留本地 main 名称，强制映射
如果您出于某些原因必须让本地叫 main，您可以配置 Git 将当前分支默认推送到它所追踪的上游分支（忽略名字差异）。

执行以下配置：

bash
# 1. 建立 main 到 remote master 的映射关系并推送
git push -u origin main:master
# 2. 修改 Git 默认推送规则 (告知 Git：以后 push 就认准刚才绑定的上游)
git config push.default upstream
配置完之后，以后您在 main 目录下直接输入 git push，Git 就会自动把它投递到云端的 master 上。