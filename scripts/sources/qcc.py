"""
企查查 MCP 工具 — 企业信息查询
=============================
注意：此数据源通过 MCP 工具调用，而非 HTTP API。
此处仅提供工具映射参考，实际查询由 AI 通过 MCP 工具执行。

可用 MCP 工具清单（按业务分类）：
"""

# ── 工商信息 ──
# mcp__qcc-company__get_company_registration_info   — 企业工商登记信息
# mcp__qcc-company__get_shareholder_info            — 股东信息
# mcp__qcc-company__get_actual_controller           — 实际控制人
# mcp__qcc-company__get_beneficial_owners           — 受益所有人
# mcp__qcc-company__get_key_personnel               — 主要人员（董监高）
# mcp__qcc-company__get_financial_data              — 财务数据

# ── 风险信息 ──
# mcp__qcc-risk__get_dishonest_info                 — 失信被执行人
# mcp__qcc-risk__get_judgment_debtor_info           — 被执行人
# mcp__qcc-risk__get_high_consumption_restriction   — 限制高消费
# mcp__qcc-risk__get_exit_restriction               — 限制出境
# mcp__qcc-risk__get_terminated_cases               — 终本案件
# mcp__qcc-risk__get_bankruptcy_reorganization      — 破产重整
# mcp__qcc-risk__get_business_exception             — 经营异常
# mcp__qcc-risk__get_serious_violation              — 严重违法
# mcp__qcc-risk__get_administrative_penalty         — 行政处罚
# mcp__qcc-risk__get_equity_freeze                  — 股权冻结
# mcp__qcc-risk__get_equity_pledge_info             — 股权出质
# mcp__qcc-risk__get_tax_arrears_notice             — 欠税公告
# mcp__qcc-risk__get_tax_violation                  — 税务违法

# ── 知识产权 ──
# mcp__qcc-ipr__get_patent_info                     — 专利信息
# mcp__qcc-ipr__get_trademark_info                  — 商标信息
# mcp__qcc-ipr__get_software_copyright_info         — 软件著作权
# mcp__qcc-ipr__get_ipr_pledge                      — 知产出质

# ── 经营信息 ──
# mcp__qcc-operation__get_financing_records          — 融资记录
# mcp__qcc-operation__get_honor_info                — 荣誉信息
# mcp__qcc-operation__get_recruitment_info          — 招聘信息
# mcp__qcc-operation__get_random_check              — 双随机抽查

# ── 历史沿革 ──
# mcp__qcc-history__get_historical_legal_rep        — 法定代表人变更历史

# ── 高管风险 ──
# mcp__qcc-executive__get_personnel_dishonest           — 高管失信
# mcp__qcc-executive__get_personnel_high_consumption_ban — 高管限高
# mcp__qcc-executive__get_personnel_judgment_debtor     — 高管被执行
# mcp__qcc-executive__get_personnel_exit_restriction     — 高管限出境


def tools_list() -> list:
    """返回所有可用企查查 MCP 工具列表"""
    return [
        # 工商
        "get_company_registration_info", "get_shareholder_info",
        "get_actual_controller", "get_beneficial_owners",
        "get_key_personnel", "get_financial_data",
        # 风险
        "get_dishonest_info", "get_judgment_debtor_info",
        "get_high_consumption_restriction", "get_exit_restriction",
        "get_terminated_cases", "get_bankruptcy_reorganization",
        "get_business_exception", "get_serious_violation",
        "get_administrative_penalty", "get_equity_freeze",
        "get_equity_pledge_info", "get_tax_arrears_notice",
        "get_tax_violation",
        # 知产
        "get_patent_info", "get_trademark_info",
        "get_software_copyright_info", "get_ipr_pledge",
        # 经营
        "get_financing_records", "get_honor_info",
        "get_recruitment_info", "get_random_check",
        # 历史
        "get_historical_legal_rep",
        # 高管风险
        "get_personnel_dishonest", "get_personnel_high_consumption_ban",
        "get_personnel_judgment_debtor", "get_personnel_exit_restriction",
    ]


if __name__ == "__main__":
    tools = tools_list()
    print(f"📋 企查查 MCP 工具共 {len(tools)} 个")
    print("  调用方式：由 AI 通过 MCP 协议直接调用，无需手动执行")
