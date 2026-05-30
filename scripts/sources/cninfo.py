"""
巨潮资讯网 — 上市公司公告查询
==========================
免费，无需 API Key
公告 PDF 下载地址: https://static.cninfo.com.cn/{adjunctUrl}
"""

import requests
import pandas as pd

BASE = "http://www.cninfo.com.cn/new/hisAnnouncement/query"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "http://www.cninfo.com.cn",
    "Referer": "http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice",
}

PLATE_MAP = {"sz": "szse", "sh": "sse", "bj": "neeq"}

CATEGORIES = {
    "年报": "category_ndbg_szsh;",
    "半年报": "category_bndbg_szsh;",
    "季报": "category_yjdbg_szsh;",
    "IPO": "category_scgkfx_szsh;",
    "分红": "category_fhcsjq_szsh;",
}


def query(stock: str = "", plate: str = "sz", category: str = "",
          keyword: str = "", start_date: str = "", end_date: str = "",
          page: int = 1, page_size: int = 20) -> pd.DataFrame:
    """
    查询上市公司公告
    stock : 股票代码，如 "000001"
    plate : sz / sh / bj
    category : 年报/半年报/季报/IPO/分红，或直接传类别代码
    keyword : 关键词
    """
    col = PLATE_MAP.get(plate, "szse")
    cat_code = CATEGORIES.get(category, category)
    se_date = ""
    if start_date or end_date:
        se_date = f"{start_date or '2000-01-01'}~{end_date or '2030-12-31'}"

    data = {
        "pageNum": page, "pageSize": page_size, "tabName": "fulltext",
        "column": col, "stock": stock, "searchkey": keyword,
        "plate": plate, "category": cat_code, "seDate": se_date,
        "trade": "", "sortName": "", "sortType": "",
    }

    resp = requests.post(BASE, headers=HEADERS, data=data, timeout=15)
    result = resp.json()
    announcements = result.get("announcements") or []

    records = []
    for item in announcements:
        pdf_url = f"https://static.cninfo.com.cn/{item['adjunctUrl']}" if item.get("adjunctUrl") else ""
        records.append({
            "code": item.get("secCode", ""),
            "name": item.get("secName", ""),
            "title": item.get("announcementTitle", ""),
            "date": item.get("announcementDate", ""),
            "type": item.get("categoryName", ""),
            "size_kb": item.get("adjunctSize", ""),
            "pdf_url": pdf_url,
        })

    return pd.DataFrame(records)


def search(keyword: str, plate: str = "sz", page: int = 1) -> pd.DataFrame:
    """按关键词搜索公告"""
    return query(keyword=keyword, plate=plate, page=page)


def annual_reports(stock: str = "", plate: str = "sz", year: int = 2024) -> pd.DataFrame:
    """获取年度报告"""
    return query(stock=stock, plate=plate, category="年报",
                 start_date=f"{year}-01-01", end_date=f"{year}-12-31")


def ipo_documents(stock: str = "", plate: str = "sz") -> pd.DataFrame:
    """获取 IPO 相关文件"""
    return query(stock=stock, plate=plate, category="IPO")


if __name__ == "__main__":
    print("=" * 60)
    print("📋 巨潮资讯 — 测试查询（2024 年年报节选）")
    print("=" * 60)
    df = query(category="年报", start_date="2024-01-01", end_date="2024-06-30", page_size=5)
    if not df.empty:
        for _, r in df.iterrows():
            print(f"  [{r['date']}] {r['code']} {r['name']}: {r['title']}")
            print(f"    PDF: {r['pdf_url']}")
    else:
        print("  暂无数据")
