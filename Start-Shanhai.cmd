@echo off
where pwsh >nul 2>nul
if %errorlevel% equ 0 (
  pwsh -NoProfile -File "%~dp0Start-Shanhai.ps1"
) else (
  powershell -NoProfile -File "%~dp0Start-Shanhai.ps1"
)
pause
