#!/usr/bin/env python3
"""
行业数据 — 统一数据源管理器
=========================
用法:
  python3 manager.py list              # 列出所有数据源
  python3 manager.py run <id> <func>   # 调用指定数据源的函数
  python3 manager.py show <id>         # 查看数据源详情
"""

import json, sys, importlib.util, os
from pathlib import Path

SKILL_DIR = Path(__file__).parent
SOURCES_FILE = SKILL_DIR / "sources.json"


def load_sources():
    with open(SOURCES_FILE) as f:
        return json.load(f)["sources"]


def load_script(script_path):
    """动态加载一个 Python 脚本"""
    full_path = SKILL_DIR / script_path
    spec = importlib.util.spec_from_file_location("source_mod", full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cmd_list():
    sources = load_sources()
    print(f"{'ID':<20} {'名称':<16} {'说明':<38} {'认证':<6}")
    print("-" * 80)
    for s in sources:
        if s.get("enabled", True):
            auth = s.get("auth", "none")
            print(f"{s['id']:<20} {s['name']:<16} {s['description']:<38} {auth:<6}")


def cmd_show(source_id):
    sources = load_sources()
    for s in sources:
        if s["id"] == source_id:
            print(f"ID:          {s['id']}")
            print(f"名称:        {s['name']}")
            print(f"说明:        {s['description']}")
            print(f"数据来源:    {s.get('provider', '?')}")
            print(f"认证要求:    {s.get('auth', 'none')}")
            print(f"可用函数:    {', '.join(s['functions'])}")
            print(f"脚本路径:    {s['script']}")
            return
    print(f"未找到数据源: {source_id}")


def cmd_run(source_id, func_name, *args):
    sources = load_sources()
    for s in sources:
        if s["id"] == source_id and s.get("enabled", True):
            mod = load_script(s["script"])
            func = getattr(mod, func_name, None)
            if not func:
                print(f"函数 '{func_name}' 不存在。可用: {', '.join(s['functions'])}")
                return
            result = func(*args)
            if result is not None:
                print(result.to_string(index=False) if hasattr(result, 'to_string') else result)
            return
    print(f"未找到数据源: {source_id}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 manager.py <list|show|run> [args...]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        cmd_list()
    elif cmd == "show" and len(sys.argv) >= 3:
        cmd_show(sys.argv[2])
    elif cmd == "run" and len(sys.argv) >= 4:
        cmd_run(sys.argv[2], sys.argv[3], *sys.argv[4:])
    else:
        print("用法: python3 manager.py <list|show|run>")
        sys.exit(1)
