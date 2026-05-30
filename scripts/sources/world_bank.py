"""
世界银行开放数据 — 200+ 国家跨国指标
"""

import requests
import pandas as pd

BASE = "https://api.worldbank.org/v2"

_COUNTRY_MAP = {
    "中国": "CN", "美国": "US", "日本": "JP", "德国": "DE",
    "英国": "GB", "法国": "FR", "印度": "IN", "韩国": "KR",
    "俄罗斯": "RU", "巴西": "BR", "加拿大": "CA", "澳大利亚": "AU",
}

def _fetch(indicator: str, country: str = "CN", years: str = "2015:2024") -> pd.DataFrame:
    url = f"{BASE}/country/{country}/indicator/{indicator}"
    params = {"format": "json", "per_page": 100, "date": years}
    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()
    if len(data) < 2:
        return pd.DataFrame()
    records = [{"year": i["date"], "value": i["value"]} for i in data[1] if i["value"]]
    return pd.DataFrame(records)

def gdp(country: str = "CN", years: str = "2015:2024") -> pd.DataFrame:
    """GDP 现价美元"""
    return _fetch("NY.GDP.MKTP.CD", country, years)

def gdp_growth(country: str = "CN", years: str = "2015:2024") -> pd.DataFrame:
    """GDP 年增长率(%)"""
    return _fetch("NY.GDP.MKTP.KD.ZG", country, years)

def inflation(country: str = "CN", years: str = "2015:2024") -> pd.DataFrame:
    """通胀率 CPI(%)"""
    return _fetch("FP.CPI.TOTL.ZG", country, years)

def population(country: str = "CN", years: str = "2015:2024") -> pd.DataFrame:
    """总人口"""
    return _fetch("SP.POP.TOTL", country, years)

def compare_indicator(indicator: str = "NY.GDP.MKTP.CD",
                      countries: list = None,
                      years: str = "2023",
                      labels: list = None) -> pd.DataFrame:
    """多国同指标对比"""
    if countries is None:
        countries = ["CN", "US", "JP", "DE"]
    rows = []
    for i, c in enumerate(countries):
        df = _fetch(indicator, c, years)
        if not df.empty:
            label = labels[i] if labels and i < len(labels) else c
            for _, r in df.iterrows():
                rows.append({"country": label, "year": r["year"], "value": r["value"]})
    return pd.DataFrame(rows)
