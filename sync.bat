@echo off
cd /d "%~dp0"
echo 📤 正在同步网站到 GitHub...
git add -A
git commit -m "网站更新 %date% %time%"
git push
echo.
echo ✅ 同步完成！30秒后刷新 https://zr-president.github.io/my-website/
pause
