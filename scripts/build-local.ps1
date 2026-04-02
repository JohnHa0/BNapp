<#
.SYNOPSIS
    DeepBayes Local Build Script (Windows)
.DESCRIPTION
    Automates the local building process of Python PyInstaller and Rust Tauri.
#>

$ErrorActionPreference = "Stop"

$ProjectRoot = "$PSScriptRoot\.."
Set-Location $ProjectRoot

# 1. Check and download UPX
$UpxDir = "$PSScriptRoot\upx"
$UpxExe = "$UpxDir\upx.exe"

if (-not (Test-Path $UpxExe)) {
    Write-Host ">>> [1/5] UPX not found. Downloading from GitHub..." -ForegroundColor Cyan
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
        Write-Host ">>> [Warning] Failed to download UPX. Network might be unstable." -ForegroundColor Yellow
        Write-Host ">>> Please download manually: $upx_url"
        Write-Host ">>> Extract 'upx.exe' into $UpxDir, then run this script again."
        Write-Host ">>> Continuing without UPX support, the output size will be large..." -ForegroundColor Yellow
    }
} else {
    Write-Host ">>> [1/5] UPX detected." -ForegroundColor Green
}

# 2. PyInstaller build
Write-Host ">>> [2/5] Building Python backend..." -ForegroundColor Cyan

$UpxArgs = if (Test-Path $UpxExe) { "--upx-dir", $UpxDir } else { "" }

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
    Write-Host ">>> [Error] PyInstaller failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

# 3. Move backend binary
Write-Host ">>> [3/5] Setup sidecar binaries..." -ForegroundColor Cyan
if (!(Test-Path "src-tauri/binaries")) { New-Item -ItemType Directory -Force -Path "src-tauri/binaries" | Out-Null }
$TargetName = "main-x86_64-pc-windows-msvc.exe"
Move-Item -Force "dist/main.exe" "src-tauri/binaries/$TargetName"

# 4. Check Frontend Packages
Write-Host ">>> [4/5] Checking frontend dependencies..." -ForegroundColor Cyan
if (!(Test-Path "node_modules")) {
    npm i
}

# 5. Build Tauri (NSIS only)
Write-Host ">>> [5/5] Building Tauri App (NSIS)..." -ForegroundColor Cyan
npx tauri build --bundles nsis

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Build complete!" -ForegroundColor Green
if (Test-Path "src-tauri\target\release\bundle\nsis") {
    Write-Host "Your installer is at:" -ForegroundColor Green
    Write-Host (Resolve-Path "src-tauri\target\release\bundle\nsis\*").Path -ForegroundColor Yellow
}
Write-Host "==========================================================" -ForegroundColor Green
