<#
.SYNOPSIS
    清理 Git 仓库：剔除不应被追踪的大目录，然后提交推送
#>

$ErrorActionPreference = "Continue"
Set-Location "c:\Users\junya\Qsync\Code\BN"

Write-Host "=== Step 1: 从 Git 追踪中移除大目录 ===" -ForegroundColor Cyan

# 这些目录已在 .gitignore 中，但可能之前被 commit 过
$dirsToRemove = @(
    "src-tauri/target",
    "src-tauri/binaries",
    "build",
    "dist",
    "node_modules",
    "scripts/upx",
    "__pycache__"
)

foreach ($dir in $dirsToRemove) {
    if (Test-Path $dir) {
        Write-Host "  Removing cached: $dir ..." -ForegroundColor Yellow
        git rm -r --cached $dir 2>$null
        Write-Host "  Done: $dir" -ForegroundColor Green
    } else {
        # 即使目录不存在，也尝试从 git index 中移除
        git rm -r --cached $dir 2>$null
    }
}

Write-Host ""
Write-Host "=== Step 2: 暂存所有源代码变更 ===" -ForegroundColor Cyan
git add -A
Write-Host "Done" -ForegroundColor Green

Write-Host ""
Write-Host "=== Step 3: 查看状态 ===" -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "=== Step 4: 提交 ===" -ForegroundColor Cyan
git commit -m "feat: switch PyInstaller onedir, embedded pip GPU install, log cleanup, port fix"

Write-Host ""
Write-Host "=== Step 5: 推送 ===" -ForegroundColor Cyan
git push

Write-Host ""
Write-Host "=== ALL DONE ===" -ForegroundColor Green
