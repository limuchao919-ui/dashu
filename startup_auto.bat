@echo off
REM 大数投资 — 开机自动更新看板 + 推送到 GitHub Pages
REM 已安装到: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\

REM 开机后等30秒再跑，避免拖慢启动
timeout /t 30 /nobreak >nul

cd /d "C:\Users\steven\Desktop\hermes文件夹\platform"

echo [%date% %time%] 开始更新 >> startup.log

REM 1. 挂载D盘（星耀数智需要）
subst D: "C:\Users\steven\Desktop\hermes文件夹\adm_data" >nul 2>&1

REM 2. 下载数据
python download_data.py >> startup.log 2>&1
if %errorlevel% neq 0 (
    echo 数据下载失败，使用缓存数据
)

REM 3. 运行筛选 + 生成看板
python screen.py >> startup.log 2>&1
python build_html.py >> startup.log 2>&1

REM 4. 推送到GitHub Pages
git add index.html startup.log *.py
git commit -m "自动更新 %date% %time%" >> startup.log 2>&1
git push origin main >> startup.log 2>&1

REM 5. 推送到企业微信
python push_wechat.py >> startup.log 2>&1

echo [%date% %time%] 完成 >> startup.log
