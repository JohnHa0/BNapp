<#
.SYNOPSIS
    DeepBayes 本地离线环境打包构建脚本 (Windows)
.DESCRIPTION
    此脚本会自动化 Python PyInstaller 和 Rust Tauri 的构建。
    它包含对体积压缩的极致优化方案：自动下载执行 UPX 压缩，以及剔除庞大而不需要的 Python(如 matplotlib 等) 库。
    且不修改 tauri.conf.json，确保完全独立运行不干扰 GitHub Actions。
#>

$ErrorActionPreference = "Stop"

$ProjectRoot = "$PSScriptRoot\.."
Set-Location $ProjectRoot

# 1. 初始化并检查 UPX 压缩引擎
$UpxDir = "$PSScriptRoot\upx"
$UpxExe = "$UpxDir\upx.exe"

if (-not (Test-Path $UpxExe)) {
    Write-Host ">>> [1/5] 未检测到 UPX，正在尝试从 GitHub 下载并提取 UPX (用于压缩 Python 二进制文件)..." -ForegroundColor Cyan
    if (!(Test-Path $UpxDir)) { New-Item -ItemType Directory -Force -Path $UpxDir | Out-Null }
    
    $upx_version = "4.2.4"
    $upx_zip = "$UpxDir\upx.zip"
    $upx_url = "https://github.com/upx/upx/releases/download/v$upx_version/upx-$upx_version-win64.zip"
    
    try {
        Invoke-WebRequest -Uri $upx_url -OutFile $upx_zip
        Expand-Archive -Path $upx_zip -DestinationPath $UpxDir -Force
        # 移动 upx.exe 到 upx 根目录，并清理
        Move-Item -Path "$UpxDir\upx-$upx_version-win64\upx.exe" -Destination $UpxExe -Force
        Remove-Item -Path "$UpxDir\upx-$upx_version-win64" -Recurse -Force
        Remove-Item -Path $upx_zip -Force
        Write-Host ">>> UPX 下载并部署成功。" -ForegroundColor Green
    }
    catch {
        Write-Host ">>> [警告] 下载 UPX 失败。网络可能无法直连 GitHub。" -ForegroundColor Yellow
        Write-Host ">>> 请手动下载: $upx_url"
        Write-Host ">>> 解压后将 upx.exe 放入 $UpxDir 目录中，然后重新运行本脚本。"
        Write-Host ">>> 继续执行打包，本次打包体积将偏大..." -ForegroundColor Yellow
    }
} else {
    Write-Host ">>> [1/5] 已检测到 UPX ($UpxExe)。" -ForegroundColor Green
}

# 2. PyInstaller 构建 Python 后端
Write-Host ">>> [2/5] 正在精简打包 Python Sidecar..." -ForegroundColor Cyan

# 检测是否有 upx 参数
$UpxArgs = if (Test-Path $UpxExe) { "--upx-dir", $UpxDir } else { "" }

# 核心模块剔除列表 (极大减小体积)
$ExcludeModules = @(
    "--exclude-module", "matplotlib",
    "--exclude-module", "tkinter",
    "--exclude-module", "IPython",
    "--exclude-module", "notebook",
    "--exclude-module", "jedi",
    "--exclude-module", "pygments",
    "--exclude-module", "pytest"
)

$PyInstallerArgs = @(
    "--onefile",
    "--name", "main"
) + $UpxArgs + $ExcludeModules + @("backend/main.py")

& pyinstaller $PyInstallerArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host ">>> [错误] PyInstaller 打包失败！" -ForegroundColor Red
    exit $LASTEXITCODE
}

# 3. 移动后端二进制文件至 Tauri 指定文件夹
Write-Host ">>> [3/5] 配置 Tauri Sidecar..." -ForegroundColor Cyan
if (!(Test-Path "src-tauri/binaries")) { New-Item -ItemType Directory -Force -Path "src-tauri/binaries" | Out-Null }
$TargetName = "main-x86_64-pc-windows-msvc.exe"
Move-Item -Force "dist/main.exe" "src-tauri/binaries/$TargetName"

# 4. 前端依赖 (若未安装)
Write-Host ">>> [4/5] 检查前端库..." -ForegroundColor Cyan
if (!(Test-Path "node_modules")) {
    npm i
}

# 5. Tauri 本地独立构建 (仅编译 NSIS Exe，不影响 tauri.conf.json 里的 "all" 设置)
Write-Host ">>> [5/5] 使用 Tauri 构建并生成精简版安装程序 (NSIS)..." -ForegroundColor Cyan
npx tauri build --bundles nsis

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "打包大功告成！" -ForegroundColor Green
if (Test-Path "src-tauri\target\release\bundle\nsis") {
    Write-Host "🎉 您的离线安装包 (.exe) 位于:" -ForegroundColor Green
    Write-Host (Resolve-Path "src-tauri\target\release\bundle\nsis\*").Path -ForegroundColor Yellow
}
Write-Host "==========================================================" -ForegroundColor Green
