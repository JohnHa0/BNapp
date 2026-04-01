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

### 3. Rust (Tauri)

Ensure you have Rust installed and configured for Tauri development. See the [Tauri documentation](https://tauri.app/v1/guides/getting-started/prerequisites) for more details.

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
