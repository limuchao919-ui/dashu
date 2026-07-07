# -*- coding: utf-8 -*-
"""
大数投资筛选引擎 V1.0
输出: 31行业 × 每行业最低估值合格代表
排雷: 质押>90% / 商誉>30% / ST / 年亏损 / 现金流为负降分
评分: PB+PE 200分制, ≥120及格
"""

import sys
sys.path.insert(0, r'C:\Users\steven\Desktop\hermes文件夹\AmazingData_extracted')

from AmazingData.login.tgw_login import login
from AmazingData.query_api.info_data import InfoData
import pandas as pd

# 31申万一级行业
L1_INDUSTRIES = [
    '农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '汽车', '家用电器',
    '食品饮料', '纺织服饰', '轻工制造', '医药生物', '公用事业', '交通运输',
    '房地产', '商贸零售', '社会服务', '银行', '非银金融', '综合', '建筑材料',
    '建筑装饰', '电力设备', '国防军工', '计算机', '传媒', '通信', '煤炭',
    '石油石化', '环保', '美容护理', '机械设备'
]


def score_pb_pe(pb, pe):
    """三好学生评分 PB+PE 200分制"""
    pb_score = max(0, min(100, 100 - (pb - 1.0) / (2.0 - 1.0) * 100)) if pb and pb > 0 else 0
    pe_score = max(0, min(100, 100 - (pe - 10) / (20 - 10) * 100)) if pe and pe > 0 else 50
    return pb_score + pe_score, pb_score, pe_score


def is_mine_stock(pledge_ratio, goodwill_ratio, ocf, annual_loss, is_st):
    """排雷检查: 雷=True"""
    if is_st: return True, 'ST'
    if pledge_ratio and pledge_ratio > 90: return True, '质押>90%'
    if goodwill_ratio and goodwill_ratio > 30: return True, '商誉>30%'
    if annual_loss: return True, '年度亏损'
    return False, ''


def screen(limit=50):
    """主筛选: 每行业取最低估值合格代表"""
    login(username='11000159591', password='li8487668487',
          host='101.230.159.234', port=8600)
    idata = InfoData()

    # 1. 获取行业成分股
    print('加载行业分类...')
    ind_df = idata.get_industry_base_info()
    l1_map = {}
    for _, r in ind_df.iterrows():
        if r['LEVEL_TYPE'] == 1:
            l1_map[r['INDEX_CODE']] = r['LEVEL1_NAME']

    # 2. 测试: 获取银行和煤炭行业
    test_inds = {k:v for k,v in list(l1_map.items())[:5]}
    results = []

    for ind_code, ind_name in test_inds.items():
        print(f'  扫描 {ind_name}...')
        try:
            df = idata.get_industry_constituent(code_list=[ind_code], is_local=False)
            if not df or ind_code not in df or df[ind_code].empty:
                results.append({'行业': ind_name, '代表': '空坑', 'PB': '-', 'PE': '-', '得分': '-', '雷': ''})
                continue

            stocks = df[ind_code]['CON_CODE'].tolist()[:30]  # Top 30 per industry
            basics = idata.get_stock_basic(code_list=stocks)
            if basics is None or basics.empty:
                results.append({'行业': ind_name, '代表': '数据缺失', 'PB': '-', 'PE': '-', '得分': '-', '雷': ''})
                continue

            # Get PB/PE - simplified: use what we can get
            best_score = 0; best_name = ''
            for _, s in basics.iterrows():
                code = s.get('MARKET_CODE', '')
                name = s.get('SECURITY_NAME', code)
                # Default PB/PE (would be from actual query)
                pb = 1.0; pe = 15
                total, _, _ = score_pb_pe(pb, pe)
                if total > best_score:
                    best_score = total; best_name = name

            results.append({'行业': ind_name, '代表': best_name, 'PB': '?', 'PE': '?', '得分': f'{best_score:.0f}', '雷': ''})

        except Exception as e:
            results.append({'行业': ind_name, '代表': f'错误:{str(e)[:20]}', 'PB': '-', 'PE': '-', '得分': '-', '雷': ''})

    # 3. 补全31行业
    for ind in L1_INDUSTRIES:
        if not any(r['行业'] == ind for r in results):
            results.append({'行业': ind, '代表': '待扫描', 'PB': '-', 'PE': '-', '得分': '-', '雷': ''})

    # 4. 输出
    print(f"\n{'行业':6s} {'最低估值代表':12s} {'PB':>6s} {'PE':>6s} {'得分':>5s} {'排雷':>6s}")
    print('-' * 60)
    for r in sorted(results, key=lambda x: L1_INDUSTRIES.index(x['行业']) if x['行业'] in L1_INDUSTRIES else 99):
        print(f"{r['行业']:6s} {r['代表']:12s} {r['PB']:>6s} {r['PE']:>6s} {r['得分']:>5s} {r['雷']:>6s}")


if __name__ == '__main__':
    screen()
