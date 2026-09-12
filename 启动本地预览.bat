@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 钟锐的个人网站 · 本地预览 (端口 8923)

netstat -ano | findstr ":8923 " | findstr LISTENING >nul 2>&1
if %errorlevel%==0 (
  echo.
  echo  服务已经在运行了，直接打开浏览器...
  echo  地址: http://127.0.0.1:8923/
  echo.
  start "" http://127.0.0.1:8923/
  timeout /t 3 >nul
  exit /b
)

echo.
echo  ================================================
echo    钟锐的个人网站 · 本地预览
echo  ================================================
echo.
echo    地址: http://127.0.0.1:8923/
echo.
echo    关闭这个窗口 = 停止服务
echo.
echo  ================================================
echo.

start "" http://127.0.0.1:8923/
python -m http.server 8923 --bind 127.0.0.1

echo.
echo  服务已停止。按任意键关闭窗口。
pause >nul
