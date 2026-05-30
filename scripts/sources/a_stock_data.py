"""
a-stock-data 核心接口封装
========================
覆盖: 行情 / 研报 / 资金 / 信号 / 基本面 / 公告
代码源自 github.com/simonlin1212/a-stock-data
"""

import requests
import pandas as pd
import urllib.request
import json
import time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


# ══════════════════════════════════════════
# Layer 1: 行情
# ══════════════════════════════════════════

def quote(codes: list) -> pd.DataFrame:
    """实时行情 — PE/PB/市值/换手率/涨跌停价（腾讯财经）"""
    if isinstance(codes, str):
        codes = [codes]
    prefixed = []
    for c in codes:
        c = c.strip().split(".")[0]  # "000001.SZ" -> "000001"
        if c.startswith(("6", "9")): prefixed.append(f"sh{c}")
        elif c.startswith("8"): prefixed.append(f"bj{c}")
        else: prefixed.append(f"sz{c}")

    url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=10).read().decode("gbk")

    records = []
    for line in data.strip().split(";"):
        if not line.strip() or "=" not in line or '"' not in line:
            continue
        vals = line.split('"')[1].split("~")
        if len(vals) < 53:
            continue
        records.append({
            "code":       vals[2],
            "name":       vals[1],
            "price":      float(vals[3]) if vals[3] else None,
            "change_pct": float(vals[32]) if vals[32] else None,
            "open":       float(vals[5]) if vals[5] else None,
            "high":       float(vals[33]) if vals[33] else None,
            "low":        float(vals[34]) if vals[34] else None,
            "pe_ttm":     float(vals[39]) if vals[39] else None,
            "pb":         float(vals[46]) if vals[46] else None,
            "mcap_yi":    float(vals[44]) if vals[44] else None,
            "turnover":   float(vals[38]) if vals[38] else None,
            "limit_up":   float(vals[47]) if vals[47] else None,
            "limit_down": float(vals[48]) if vals[48] else None,
        })
    return pd.DataFrame(records)


def kline(code: str, ktype: int = 1) -> pd.DataFrame:
    """K线数据（百度股市通，自带 MA5/MA10/MA20）"""
    params = {
        "all": "1", "isIndex": "false", "isBk": "false", "isBlock": "false",
        "isFutures": "false", "isStock": "true", "newFormat": "1",
        "group": "quotation_kline_ab", "finClientType": "pc",
        "code": code, "start_time": "", "ktype": str(ktype),
    }
    headers = {"User-Agent": UA, "Accept": "application/vnd.finance-web.v1+json",
               "Origin": "https://gushitong.baidu.com", "Referer": "https://gushitong.baidu.com/"}
    r = requests.get("https://finance.pae.baidu.com/selfselect/getstockquotation",
                     params=params, headers=headers, timeout=10)
    d = r.json()
    md = d.get("Result", {}).get("newMarketData", {})
    keys = md.get("keys", [])
    rows = md.get("marketData", "").split(";")

    records = []
    for row in rows:
        vals = row.split(",")
        if len(vals) >= len(keys):
            records.append(dict(zip(keys, vals)))
    return pd.DataFrame(records)


# ══════════════════════════════════════════
# Layer 2: 研报
# ══════════════════════════════════════════

def research_reports(code: str, pages: int = 3) -> pd.DataFrame:
    """东财研报列表"""
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Referer": "https://data.eastmoney.com/"})
    all_records = []
    for page in range(1, pages + 1):
        params = {
            "industryCode": "*", "pageSize": "50", "industry": "*",
            "rating": "*", "ratingChange": "*",
            "beginTime": "2000-01-01", "endTime": "2030-01-01",
            "pageNo": str(page), "fields": "", "qType": "0",
            "orgCode": "", "code": code,
            "p": str(page), "pageNum": str(page), "pageNumber": str(page),
        }
        r = session.get("https://reportapi.eastmoney.com/report/list",
                        params=params, timeout=30)
        data = r.json().get("data") or []
        if not data:
            break
        all_records.extend(data)
        time.sleep(0.3)
    records = []
    for item in all_records:
        records.append({
            "title": item.get("title", ""),
            "org": item.get("orgSName", ""),
            "analyst": item.get("analyst", ""),
            "date": (item.get("publishDate") or "")[:10],
            "rating": item.get("rating", ""),
            "stock": item.get("stockName", ""),
            "code": item.get("stockCode", ""),
        })
    return pd.DataFrame(records)


# ══════════════════════════════════════════
# Layer 3: 东财数据中心（龙虎榜/解禁/两融/大宗）
# ══════════════════════════════════════════

DC_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"

def _datacenter(report_name: str, filter_str: str = "",
                columns: str = "ALL", page_size: int = 20,
                sort_col: str = "", sort_type: str = "-1") -> pd.DataFrame:
    params = {
        "reportName": report_name, "columns": columns,
        "filter": filter_str, "pageNumber": "1", "pageSize": str(page_size),
        "sortColumns": sort_col, "sortTypes": sort_type,
        "source": "WEB", "client": "WEB",
    }
    r = requests.get(DC_URL, params=params, headers={"User-Agent": UA}, timeout=15)
    data = (r.json().get("result") or {}).get("data") or []
    return pd.DataFrame(data)


def longhu(stock: str = "", page_size: int = 20) -> pd.DataFrame:
    """龙虎榜 — 日级上榜记录"""
    f = f'(SECURITY_CODE="{stock}")' if stock else ""
    return _datacenter("RPT_LHB", filter_str=f, page_size=page_size,
                       sort_col="TRADE_DATE", sort_type="-1")


# ══════════════════════════════════════════
# Layer 4: 基本面
# ══════════════════════════════════════════

def financial_reports(code: str) -> dict:
    """新浪财报三表（资产负债表/利润表/现金流量表）"""
    url = f"https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getFinanceData?symbol={code}"
    r = requests.get(url, headers={"User-Agent": UA}, timeout=15)
    data = r.json()
    return data


def stock_info(code: str) -> pd.DataFrame:
    """东财个股基础信息（行业/股本/市值/上市日期）"""
    code_clean = code.split(".")[0]
    prefix = "1" if code_clean.startswith(("6", "9")) else "0"
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "secid": f"{prefix}.{code_clean}",
        "fields": "f57,f58,f85,f116,f117,f162,f167,f168,f169,f170",
    }
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=10)
    d = r.json().get("data", {})
    return pd.DataFrame([{
        "code": d.get("f57", ""),
        "name": d.get("f58", ""),
        "industry": d.get("f85", ""),
    }])


# ══════════════════════════════════════════
# 一键查询
# ══════════════════════════════════════════

def stock_overview(code: str) -> dict:
    """个股综合概览：行情 + 基础信息"""
    q = quote([code])
    info = stock_info(code)
    return {
        "quote": q.to_dict("records") if not q.empty else [],
        "info": info.to_dict("records") if not info.empty else [],
    }


if __name__ == "__main__":
    print("=" * 60)
    print("📈 a-stock-data 接口测试")
    print("=" * 60)

    print("\n1️⃣  实时行情 — 贵州茅台")
    df = quote(["600519"])
    print(df.to_string(index=False))

    print("\n2️⃣  研报列表 — 宁德时代（前3条）")
    df2 = research_reports("300750", pages=1)
    print(df2.head(3).to_string(index=False))
