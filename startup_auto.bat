@echo off
REM 大数投资 — 开机自动更新看板
REM 已安装到: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\

REM 开机后等30秒再跑，避免拖慢启动
timeout /t 30 /nobreak >nul

cd /d "C:\Users\steven\Desktop\hermes文件夹\platform"

echo [%date% %time%] 开始更新 >> startup.log

REM 1. 挂载D盘（星耀数智需要）
subst D: "C:\Users\steven\Desktop\hermes文件夹\adm_data" >nul 2>&1

REM 2. 下载数据
python download_data.py >> startup.log 2>&1

REM 3. 运行筛选 + 生成看板
python screen.py >> startup.log 2>&1
python build_html.py >> startup.log 2>&1

echo [%date% %time%] 完成 >> startup.log

REM 打开看板（浏览器）
start "" index.html
