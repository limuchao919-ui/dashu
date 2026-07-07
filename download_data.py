# -*- coding: utf-8 -*-
"""
大数投资筛选平台 — 数据层
每天运行一次，从星耀数智拉数据写入 SQLite
"""

import sys, os, sqlite3
sys.path.insert(0, r'C:\Users\steven\Desktop\hermes文件夹\AmazingData_extracted')

from AmazingData.login.tgw_login import login
from AmazingData.query_api.info_data import InfoData
import pandas as pd

DB = r'C:\Users\steven\Desktop\hermes文件夹\platform\dashu.db'


def init_db():
    conn = sqlite3.connect(DB)
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS stock_basic (
            code TEXT PRIMARY KEY, name TEXT, list_date TEXT,
            is_listed INTEGER, industry_l1 TEXT, industry_l2 TEXT
        );
        CREATE TABLE IF NOT EXISTS valuation (
            code TEXT, date TEXT, pb REAL, pe REAL, mcap REAL,
            nav_ps REAL, eps_ttm REAL,
            PRIMARY KEY (code, date)
        );
        CREATE TABLE IF NOT EXISTS mine_field (
            code TEXT, date TEXT, pledge_ratio REAL, goodwill_ratio REAL,
            ocf_sign INTEGER, annual_loss INTEGER, is_st INTEGER,
            PRIMARY KEY (code, date)
        );
        CREATE TABLE IF NOT EXISTS profit_trend (
            code TEXT, date TEXT, net_profit REAL, yoy_pct REAL,
            rev REAL, PRIMARY KEY (code, date)
        );
        CREATE TABLE IF NOT EXISTS industry_map (
            code TEXT, industry_l1 TEXT, industry_l2 TEXT,
            industry_l3 TEXT, level INTEGER,
            PRIMARY KEY (code, industry_l1, industry_l2, industry_l3)
        );
    ''')
    conn.commit(); conn.close()
    print('DB init OK')


def download_all():
    login(username='11000159591', password='li8487668487',
          host='101.230.159.234', port=8600)
    idata = InfoData()

    # 1. 行业分类：下载511个行业 → 构建申万31大类映射
    print('下载行业分类...')
    ind_df = idata.get_industry_base_info()
    # 只取L1=31大类
    l1 = ind_df[ind_df['LEVEL_TYPE'] == 1][['INDEX_CODE', 'LEVEL1_NAME']].drop_duplicates()
    print(f'  申万一级行业: {len(l1)}个')

    # 2. 下载行业成分股
    print('下载成分股...')
    all_stocks = set()
    ind_codes = l1['INDEX_CODE'].tolist()
    for code in ind_codes:
        try:
            df = idata.get_industry_constituent(code_list=[code], is_local=False)
            if df and code in df and not df[code].empty:
                stocks = df[code]['CON_CODE'].tolist()
                all_stocks.update(stocks)
                print(f'  {code}: {len(stocks)}只')
        except: pass
    print(f'  总股票: {len(all_stocks)}只')

    # 3. 下载基本面数据（取前100只做验证）
    stock_list = list(all_stocks)[:100]
    print(f'下载{len(stock_list)}只基本面...')
    try:
        bal = idata.get_balance_sheet(code_list=stock_list, is_local=False)
        inc = idata.get_income(code_list=stock_list, is_local=False)
        print(f'  资产负债表: {len(bal)}只  利润表: {len(inc)}只')
    except Exception as e:
        print(f'  下载失败: {e}')

    # 4. 下载质押数据
    print('下载质押数据...')
    try:
        pled = idata.get_equity_pledge_freeze(code_list=stock_list[:20], is_local=False)
        print(f'  质押: {len(pled)}只')
    except Exception as e:
        print(f'  质押失败: {e}')

    print('\n数据下载完成。下一步: 写入SQLite并构建筛选引擎。')


if __name__ == '__main__':
    init_db()
    download_all()
