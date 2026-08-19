#!/usr/bin/env python3
"""
第一个接单自动化示例：每日资讯汇总器（优化建议 #83 落地）
============================================================
- 抓取免费新闻源（IT之家 RSS / 新浪财经7x24）→ 汇总当日资讯 → 保存 Markdown
- 这是【数据整理类】自动化的最小模板——中小企业最常外包的类型
- 改造方向：换新闻源 / 换输出格式(Excel/Word) / 定时运行(Windows计划任务) = 接单变现

用法:
  python scripts/automation_starter.py            # 抓取并保存到 knowledge_base/automation/
  python scripts/automation_starter.py --limit 10  # 只取前10条

前置: pip install requests
配套: 本地部署 Qwen3.8-27B 后，可用它做摘要/分类（隐私数据不出域）
"""

import sys, os, io, re, argparse, requests
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "knowledge_base", "automation")

SOURCES = [
    {"name": "IT之家(科技)", "type": "rss", "url": "https://www.ithome.com/rss/",
     "headers": {"User-Agent": "Mozilla/5.0"}},
    {"name": "新浪财经7x24", "type": "json",
     "url": "https://zhibo.sina.com.cn/api/zhibo/feed?page=1&page_size=20&zhibo_id=152&tag_id=0",
     "headers": {}},
]


def strip_html(s):
    s = re.sub(r'<[^>]+>', ' ', str(s))
    return re.sub(r'\s+', ' ', s).strip()


def fetch():
    """抓取各源，返回 [{title, source}]（去重）"""
    results, seen = [], set()
    for src in SOURCES:
        try:
            r = requests.get(src["url"], headers=src["headers"], timeout=15)
            r.raise_for_status()
            items = []
            if src["type"] == "rss":
                import xml.etree.ElementTree as ET
                root = ET.fromstring(r.content)
                for it in root.iter("item"):
                    title = strip_html(it.findtext("title", ""))
                    if title:
                        items.append({"title": title, "source": src["name"]})
            elif src["type"] == "json":
                data = r.json()
                feed = data.get("result", {}).get("data", {}).get("feed", {}).get("list", [])
                for it in feed:
                    title = strip_html(it.get("rich_text", ""))
                    if title:
                        items.append({"title": title, "source": src["name"]})
            for it in items:
                key = it["title"][:20]
                if key not in seen:
                    seen.add(key)
                    results.append(it)
            print(f"  ✓ {src['name']}: {len(items)} 条")
        except Exception as e:
            print(f"  ! {src['name']} 失败: {str(e)[:80]}")
    return results


def main():
    ap = argparse.ArgumentParser(description="每日资讯汇总器（接单自动化模板）")
    ap.add_argument("--limit", type=int, default=15, help="保存条数")
    args = ap.parse_args()

    print("🚀 每日资讯汇总器启动…")
    news = fetch()
    if not news:
        print("✗ 未抓到任何资讯")
        sys.exit(1)

    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{today}.md")

    lines = [f"# 每日资讯汇总 · {today}", ""]
    lines.append(f"> 自动生成：{datetime.now().strftime('%Y-%m-%d %H:%M')} · 共 {len(news)} 条")
    lines.append("")
    for i, n in enumerate(news[:args.limit], 1):
        lines.append(f"{i}. [{n['source']}] {n['title']}")
    lines.append("")
    lines.append("---")
    lines.append("下一步：接入本地部署的 Qwen3.8-27B 做摘要/分类（隐私不出域）→ 这就是可交付给客户的成品。")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ 已保存 {len(news[:args.limit])} 条 → {path}")
    print("💡 改造方向：换源/换格式/定时运行(计划任务) = 接单变现的模板")


if __name__ == "__main__":
    main()
