# -*- coding: utf-8 -*-
"""推送到企业微信"""

import requests, json, sys
from datetime import datetime

WEBHOOK = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=dd6279ce-c8a7-4f93-9e75-ff76650dabc2'


def send_text(text):
    r = requests.post(WEBHOOK, json={'msgtype': 'text', 'text': {'content': text}})
    return r.json()


def send_markdown(md):
    r = requests.post(WEBHOOK, json={'msgtype': 'markdown', 'markdown': {'content': md}})
    return r.json()


def push_screen_result():
    """推送今日筛选结果"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    msg = f"""📊 **大数投资 行业坑位看板** {now}

明天接入`screen.py`输出后自动填充筛选结果。

**V10.9 回测概况：**
- 策略收益：96.87%
- 年化收益：10.50%
- 最大回撤：15.08%
- 已兑现净盈：+2,354,215
- 亏损卖出：0笔
- 当前持仓浮盈：+553,479（17.8%）

⚠️ 注意：本数据为回测历史数据，实盘结果会有差异。
📈 完整看板：https://limuchao919-ui.github.io/dashu/"""
    return send_markdown(msg)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        r = send_text('✅ 大数投资推送测试成功')
        print(r)
    else:
        r = push_screen_result()
        print(r)
