@echo off
cd /d "c:\Users\junya\Qsync\Code\BN"
set LOG=scripts\git-output.txt

echo [%date% %time%] Starting git operations > %LOG%

echo [%date% %time%] Step 1: git rm cached binaries >> %LOG% 2>&1
git rm -r --cached src-tauri\binaries 2>> %LOG% || echo skipped >> %LOG%

echo [%date% %time%] Step 2: git rm cached build >> %LOG% 2>&1
git rm -r --cached build 2>> %LOG% || echo skipped >> %LOG%

echo [%date% %time%] Step 3: git add >> %LOG% 2>&1
git add -A >> %LOG% 2>&1

echo [%date% %time%] Step 4: git status >> %LOG% 2>&1
git status --short >> %LOG% 2>&1

echo [%date% %time%] Step 5: git commit >> %LOG% 2>&1
git commit -m "feat: switch PyInstaller onedir, embedded pip GPU install, log cleanup, port fix" >> %LOG% 2>&1

echo [%date% %time%] Step 6: git push >> %LOG% 2>&1
git push >> %LOG% 2>&1

echo [%date% %time%] ALL DONE >> %LOG%
