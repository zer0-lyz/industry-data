"""
中国宏观经济 — GDP / CPI / PPI / PMI / M2 / 进出口
来自国家统计局、央行、海关总署
"""

import akshare as ak
import pandas as pd

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)
pd.set_option("display.max_rows", 30)


def gdp():
    """国内生产总值（季度，含三大产业拆分）"""
    return ak.macro_china_gdp()

def cpi():
    """居民消费价格指数（月度）"""
    return ak.macro_china_cpi_monthly()

def ppi():
    """工业生产者出厂价格指数（月度）"""
    return ak.macro_china_ppi_monthly()

def pmi():
    """采购经理人指数"""
    return ak.macro_china_pmi()

def m2():
    """货币供应量 M0/M1/M2（月度）"""
    return ak.macro_china_money_supply()

def trade():
    """进出口贸易数据（月度）"""
    return ak.macro_china_trade()

def all_macro():
    """一键全部宏观指标"""
    return {
        "gdp": gdp(),
        "cpi": cpi(),
        "ppi": ppi(),
        "pmi": pmi(),
        "m2": m2(),
        "trade": trade(),
    }
