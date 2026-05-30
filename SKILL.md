---
name: "行业数据"
description: "行业分析报告数据查询。统一的注册表式数据源管理器，支持通过 sources.json 动态挂载新的数据接口。内置中国宏观（GDP/CPI/PPI/PMI/M2/进出口）和世界银行（200+ 国家跨国指标）两个数据源。当用户需要宏观经济数据、全球指标对比或行业分析基础数据时使用。"
---

# 行业数据 Skill

数据源注册中心模式。所有接口统一注册在 `sources.json`，新增数据源只需添加一个条目。

## 数据源列表

```bash
python3 manager.py list
```

当前已注册：

| ID | 名称 | 说明 | 认证 |
|----|------|------|------|
| `macro_china` | 中国宏观经济 | GDP / CPI / PPI / PMI / M2 / 进出口 | 无需 |
| `world_bank` | 世界银行 | 200+ 国家跨国指标 | 无需 |

## 对话用法

直接说需求，我会调对应数据源：

- "查 GDP" → macro_china
- "对比中美日 GDP" → world_bank
- "拉 CPI 和 M2" → macro_china

## 手动执行

```bash
# 列出所有数据源
python3 manager.py list

# 查看某个数据源详情（含可用函数）
python3 manager.py show macro_china

# 执行某个数据源的函数
python3 manager.py run macro_china gdp
python3 manager.py run world_bank compare_indicator
```

## 如何新增一个数据源

在 `sources.json` 里加一个条目，并在 `scripts/sources/` 下放对应的 Python 脚本即可。

```json
{
  "id": "my_source",
  "name": "我的数据",
  "description": "说明",
  "provider": "来源",
  "auth": "none",
  "script": "scripts/sources/my_source.py",
  "functions": ["func1", "func2"],
  "enabled": true
}
```

也可以直接对我说 **"帮我把 xxx 接口加到行业数据里"**，我来写。

## 依赖

```bash
pip install akshare pandas requests
```
