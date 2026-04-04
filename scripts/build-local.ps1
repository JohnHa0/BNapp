<#
.SYNOPSIS
    DeepBayes Local Build Script (Windows)
.DESCRIPTION
    Automates the local building process of Python PyInstaller (onedir) and Rust Tauri.
#>

$ErrorActionPreference = "Stop"

$ProjectRoot = "$PSScriptRoot\.."
Set-Location $ProjectRoot

# 1. Check and download UPX
$UpxDir = "$PSScriptRoot\upx"
$UpxExe = "$UpxDir\upx.exe"

if (-not (Test-Path $UpxExe)) {
    Write-Host ">>> [1/6] UPX not found. Downloading from GitHub..." -ForegroundColor Cyan
    if (!(Test-Path $UpxDir)) { New-Item -ItemType Directory -Force -Path $UpxDir | Out-Null }
    
    $upx_version = "4.2.4"
    $upx_zip = "$UpxDir\upx.zip"
    $upx_url = "https://github.com/upx/upx/releases/download/v$upx_version/upx-$upx_version-win64.zip"
    
    try {
        Invoke-WebRequest -Uri $upx_url -OutFile $upx_zip
        Expand-Archive -Path $upx_zip -DestinationPath $UpxDir -Force
        Move-Item -Path "$UpxDir\upx-$upx_version-win64\upx.exe" -Destination $UpxExe -Force
        Remove-Item -Path "$UpxDir\upx-$upx_version-win64" -Recurse -Force
        Remove-Item -Path $upx_zip -Force
        Write-Host ">>> UPX downloaded successfully." -ForegroundColor Green
    }
    catch {
        Write-Host ">>> [Warning] Failed to download UPX." -ForegroundColor Yellow
        Write-Host ">>> Continuing without UPX, output size will be larger..." -ForegroundColor Yellow
    }
}
else {
    Write-Host ">>> [1/6] UPX detected." -ForegroundColor Green
}

# 2. PyInstaller build (onedir 模式，输出到 dist-backend/main/ 目录，避免与 Vite 的 dist/ 冲突)
Write-Host ">>> [2/6] Building Python backend (onedir mode) via main.spec..." -ForegroundColor Cyan

# 清理旧的构建产物
if (Test-Path "dist-backend") { Remove-Item -Recurse -Force "dist-backend" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

$UpxArgs = @()
if (Test-Path $UpxExe) { $UpxArgs = @("--upx-dir", $UpxDir) }

& pyinstaller main.spec --noconfirm --distpath dist-backend @UpxArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host ">>> [Error] PyInstaller failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

# 3. Setup sidecar binaries (复制整个 onedir 目录)
Write-Host ">>> [3/6] Setting up sidecar binaries (onedir)..." -ForegroundColor Cyan

$BinDir = "src-tauri\binaries"
if (!(Test-Path $BinDir)) { New-Item -ItemType Directory -Force -Path $BinDir | Out-Null }

# 清理旧文件
if (Test-Path "$BinDir\_internal") { Remove-Item -Recurse -Force "$BinDir\_internal" }
if (Test-Path "$BinDir\main-x86_64-pc-windows-msvc.exe") { Remove-Item -Force "$BinDir\main-x86_64-pc-windows-msvc.exe" }

# 复制 exe (重命名为 Tauri sidecar 格式)
Copy-Item -Force "dist-backend\main\main.exe" "$BinDir\main-x86_64-pc-windows-msvc.exe"

# 复制 _internal 运行时目录
Copy-Item -Recurse -Force "dist-backend\main\_internal" "$BinDir\_internal"

$internalSize = (Get-ChildItem -Recurse "$BinDir\_internal" | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host ">>> _internal directory: $([math]::Round($internalSize, 1)) MB" -ForegroundColor DarkGray

# 4. Check Frontend Packages
Write-Host ">>> [4/6] Checking frontend dependencies..." -ForegroundColor Cyan
if (!(Test-Path "node_modules")) {
    npm i
}

# 5. Build Tauri (NSIS only, with compression)
Write-Host ">>> [5/6] Building Tauri App (NSIS)..." -ForegroundColor Cyan
npx tauri build --bundles nsis

# 6. Report results
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Build complete!" -ForegroundColor Green
if (Test-Path "src-tauri\target\release\bundle\nsis") {
    Write-Host "Your installer is at:" -ForegroundColor Green
    $installers = Get-ChildItem "src-tauri\target\release\bundle\nsis\*.exe"
    foreach ($f in $installers) {
        $sizeMB = [math]::Round($f.Length / 1MB, 1)
        Write-Host "  $($f.Name)  ($sizeMB MB)" -ForegroundColor Yellow
    }
}
Write-Host "==========================================================" -ForegroundColor Green
