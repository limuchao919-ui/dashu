# -*- coding: utf-8 -*-
"""
生成 HTML 看板 — 从 SQLite 读数据输出静态网页
"""
import sqlite3, json
from datetime import datetime

DB = r'C:\Users\steven\Desktop\hermes文件夹\platform\dashu.db'
OUT = r'C:\Users\steven\Desktop\hermes文件夹\platform\index.html'

HTML = '''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>大数投资 行业坑位看板</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'Microsoft YaHei',sans-serif;background:#f4f6f9;padding:16px;max-width:800px;margin:auto}
h1{font-size:20px;text-align:center;color:#1a1a2e;margin-bottom:4px}
.sub{text-align:center;color:#888;font-size:12px;margin-bottom:16px}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08)}
th{background:#1a1a2e;color:#fff;padding:8px 6px;font-size:12px;text-align:left}
td{padding:6px;font-size:12px;border-bottom:1px solid #e8eaef}
tr:hover{background:#f0f4ff}
.badge{padding:2px 6px;border-radius:4px;font-size:10px;font-weight:700}
.buy{background:#d4edda;color:#155724}
.hold{background:#fff3cd;color:#856404}
.gap{background:#f8d7da;color:#721c24}
.score{font-weight:700}
.alert{background:#ffeeba}
</style>
</head>
<body>
<h1>📊 大数投资 行业坑位看板</h1>
<div class="sub">申万31行业 × 最低估值合格代表 | __TIME__</div>
<table>
<thead><tr><th>#</th><th>行业</th><th>代表股</th><th>PB</th><th>PE</th><th>得分</th><th>持仓</th><th>排雷</th></tr></thead>
<tbody>
__ROWS__
</tbody>
</table>
</body>
</html>'''


def build_rows():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    conn.close()

    if 'valuation' not in tables:
        return '<tr><td colspan="8" style="text-align:center;padding:40px;color:#aaa">数据尚未就绪 — 运行 download_data.py 拉取数据</td></tr>'

    # TODO: 接入真实数据后填充
    rows = '<tr><td colspan="8" style="text-align:center;padding:40px">数据层已就绪，等待接入筛选引擎</td></tr>'
    return rows


if __name__ == '__main__':
    rows = build_rows()
    html = HTML.replace('__TIME__', datetime.now().strftime('%Y-%m-%d %H:%M'))
    html = html.replace('__ROWS__', rows)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'看板已生成: {OUT}')
    print('下一步: 部署到 GitHub Pages')
