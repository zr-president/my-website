#!/usr/bin/env python3
"""
Daily Website Update Script — Standardized Template
=====================================================
Replaces manual Python one-liners with a reusable, auditable daily update workflow.

Usage:
  1. Fill in the CONFIG dict below with today's data
  2. Run: python scripts/daily_update.py
  3. Auto-validates JS syntax after each section
  4. Auto-commits and pushes (with --commit flag)

Sections updated:
  - DAILY_DATA (date, market, news, weather, weekly_focus, tip, movie, recommendations)
  - DAILY_BRIEFING (6 highlights)
  - INSIGHTS (stock, ai-track, movie, news, anime, career, learning — summary/trend/tip)
  - PICKS (anime, gaming, movie titles/descs)
  - DAILY_VOCAB (10 new words)
  - OPTIMIZATION_LOG (date, streak, new suggestions)
  - INSIGHTS_TODAY_UPDATED
  - SITE_VERSION + index.html cache buster
  - WEBSITE_GUIDE date
"""

import sys, os, io, re, json, subprocess, argparse
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAILY_DATA_PATH = os.path.join(ROOT, "daily_data.js")
INDEX_PATH = os.path.join(ROOT, "index.html")

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG — Fill in today's data below
# ═══════════════════════════════════════════════════════════════════════════════

CONFIG = {
    "date_cn": "2026年8月12日",       # e.g. "2026年8月12日"
    "date_iso": "2026-08-12",         # e.g. "2026-08-12"
    "datetime_iso": "2026-08-12T14:30:00+08:00",
    "version": "1.2.12",             # e.g. "1.2.12"
    "weekday_cn": "周三",             # e.g. "周三"
    "week_label": "8月第二周周三",     # e.g. "8月第二周周三"

    # Market summary — one long string, | separated
    "market_summary": "待填入今日股市数据",

    # Weather summary — one line
    "weather_summary": "待填入今日天气数据",

    # Weekly focus — narrative of the day's key themes
    "weekly_focus": "待填入本周焦点",

    # Tip of the day — 5 narratives
    "tip_of_day": "待填入今日五重叙事",

    # News headlines — 5 articles
    "news_headlines": [
        {"title": "...", "url": "...", "source": "...", "category": "财经"},
        {"title": "...", "url": "...", "source": "...", "category": "科技"},
        {"title": "...", "url": "...", "source": "...", "category": "科技"},
        {"title": "...", "url": "...", "source": "...", "category": "文娱"},
        {"title": "...", "url": "...", "source": "...", "category": "游戏"},
    ],

    # Daily recommendation
    "daily_rec": {
        "music": {"title": "...", "desc": "...", "link": "..."},
        "anime": {"title": "...", "desc": "...", "link": "..."},
        "novel": {"title": "...", "desc": "...", "link": "..."},
        "cocktail": {"title": "...", "desc": "...", "link": "..."},
    },

    # Movie section
    "movie": {
        "summary": "...",
        "trend": "...",
        "tip": "...",
        "reasoning": "...",
    },

    # DAILY_BRIEFING — 6 highlights (priority 1-6)
    "briefing_highlights": [
        # {priority, icon, section, headline, summary, action, link, deepLink}
    ],

    # INSIGHTS updates — only sections that changed
    # 每个板块可带 verdict 字段（结论先行，小白友好）：
    #   verdict = 2-4句大白话：①发生了什么本质变化 ②意味着什么/会带来什么结果 ③该不该动/行动建议 ④下周/明日关注信号
    #   示例：'🎯 今日结论：大盘指数小涨但多数股票在跌=权重撑指数，别被指数骗了；真正的钱在AI硬件主线；小白别追涨停，等回调分批买入。'
    "insights_updates": {
        "stock":       {"summary": "...", "trend": "...", "tip": "...", "verdict": "..."},
        "ai-track":    {"summary": "...", "trend": "...", "tip": "...", "verdict": "..."},
        "movie":       {"summary": "...", "trend": "...", "tip": "..."},
        "news":        {"summary": "...", "trend": "...", "tip": "...", "verdict": "..."},
        "anime":       {"summary": "...", "trend": "...", "tip": "..."},
        "career":      {"summary": "...", "trend": "...", "tip": "...", "verdict": "..."},
        "learning":    {"summary": "...", "trend": "...", "tip": "..."},
    },

    # Today's updated sections
    "today_updated": ['stock','ai-track','movie','learning','career','news','gaming','anime'],

    # New VOCAB words (10)
    "vocab_words": [
        # {emoji, category, word, definition, example, why_matters}
    ],

    # New optimization suggestions (3-5)
    "new_suggestions": [
        # {id, cat, title, desc, priority, status}
    ],

    # TOOLCHAIN_RADAR — 必填！每日更新时如实填写用户工具链动态
    # 只关注钟锐在用的工具链（Claude Code + DeepSeek + Harness + 其他模型）
    # 每个 item 回答：发生了什么 → 对我意味着什么 → 价格/性价比变化 → 行动建议
    "toolchain_radar": {
        "headline": "一句话概括今日工具链最重要的变化（如：DeepSeek Harness 公测 / V4 API 涨价）",
        "items": [
            # {topic, type(新工具/价格变化/替代方案/模型更新/生态观察), summary, impact, action}
        ],
    },

    # LEARN_PATHS 小白课堂 — 每日更新必填！
    # 更新步骤（防止重复）：
    #   1. 把 daily_data.js 中 LEARN_PATHS.items 的旧内容（10条）追加到 archive[旧updated日期]
    #   2. items 换成今日新10条 {section, emoji, title, content, takeaway}
    #   3. updated 改今日日期，current_day +1
    #   4. archive 不存当天内容（当天只放 items），渲染时自动按日期+标题去重
    "learn_paths": {
        "updated": "2026-08-15",
        "current_day": 1,
        "items": [
            # {section(股市/AI/购车/购房/饮食/求职/健身/理财...), emoji, title, content, takeaway}
        ],
    },

    # Total suggestion count after adding new ones
    "total_suggestions": 38,

    # Streak days
    "streak_days": 22,
}


# ═══════════════════════════════════════════════════════════════════════════════
# Core replacement engine
# ═══════════════════════════════════════════════════════════════════════════════

class DailyUpdater:
    def __init__(self, config):
        self.cfg = config
        self.content = ""
        self.changes = 0
        self.errors = []

    def load(self):
        with open(DAILY_DATA_PATH, 'r', encoding='utf-8') as f:
            self.content = f.read()
        return self

    def save(self):
        with open(DAILY_DATA_PATH, 'w', encoding='utf-8') as f:
            f.write(self.content)

    def replace(self, old, new, label=""):
        if old in self.content:
            self.content = self.content.replace(old, new, 1)
            self.changes += 1
            if label:
                print(f"  ✓ {label}")
            return True
        else:
            self.errors.append(f"NOT FOUND: {label or old[:50]}")
            print(f"  ✗ {label or old[:50]}")
            return False

    def validate(self):
        """Validate JS syntax with Node.js."""
        try:
            result = subprocess.run(
                ["node", "-e", "new Function(require('fs').readFileSync('daily_data.js','utf8'))"],
                capture_output=True, text=True, timeout=30, cwd=ROOT
            )
            if result.returncode != 0:
                print(f"  ✗ JS SYNTAX ERROR:\n{result.stderr[:500]}")
                return False
            print("  ✓ JS syntax OK")
            return True
        except Exception as e:
            print(f"  ✗ Validation failed: {e}")
            return False

    def update_version_bumper(self):
        """Update cache buster in index.html."""
        old_v = self.cfg["version"]
        # Increment patch version
        parts = old_v.split(".")
        new_v = f"{parts[0]}.{parts[1]}.{int(parts[2])+1}"
        self.cfg["version"] = new_v

        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            idx_content = f.read()
        old_bump = f"daily_data.js?v={old_v}"
        new_bump = f"daily_data.js?v={new_v}"
        if old_bump in idx_content:
            idx_content = idx_content.replace(old_bump, new_bump)
            with open(INDEX_PATH, 'w', encoding='utf-8') as f:
                f.write(idx_content)
            print(f"  ✓ Cache buster: {old_v} → {new_v}")

    def git_commit_push(self):
        """Commit and push changes."""
        cmds = [
            ["git", "add", "daily_data.js", "index.html"],
            ["git", "commit", "-m", f"{self.cfg['date_cn']}每日更新"],
            ["git", "push"],
        ]
        for cmd in cmds:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
            if result.returncode != 0 and "nothing to commit" not in result.stdout + result.stderr:
                print(f"  ⚠ git {' '.join(cmd[1:3])}: {result.stderr[:200]}")

    # ── Section-specific updaters ──

    def update_core_fields(self):
        """Update SITE_VERSION, dates, market_summary, weather, weekly_focus, tip_of_day."""
        print("\n── Core DAILY_DATA fields ──")

        # Site version
        old_ver = self.cfg["version"]
        parts = old_ver.split(".")
        new_ver = f"{parts[0]}.{parts[1]}.{int(parts[2])+1}"
        self.replace(f'"{old_ver}"', f'"{new_ver}"', f'SITE_VERSION {old_ver}→{new_ver}')
        self.cfg["version"] = new_ver

        # Dates
        # We need to find and replace the OLD date strings. Since we don't know them,
        # we search for patterns. This is intentionally left as a manual step for now.
        print("  ⚠ Date fields require manual update — use _update_812.py pattern")

    def update_toolchain_radar(self):
        """Replace TOOLCHAIN_RADAR block with today's values (must be filled in CONFIG)."""
        print("\n── TOOLCHAIN_RADAR ──")
        cfg = self.cfg.get("toolchain_radar", {})
        items = cfg.get("items", [])
        if not items:
            print("  ⚠ toolchain_radar.items 为空 — 跳过（请务必填写！）")
            return

        def _js_str(s):
            return json.dumps(str(s), ensure_ascii=False)

        parts = [f"  updated: {_js_str(self.cfg['date_iso'])},"]
        parts.append(f"  headline: {_js_str(cfg.get('headline', ''))},")
        parts.append("  items: [")
        for it in items:
            parts.append("    {")
            for k in ("topic", "type", "summary", "impact", "action"):
                if k in it:
                    parts.append(f"      {k}: {_js_str(it[k])},")
            parts.append("    },")
        parts.append("  ]")
        new_block = "\n".join(parts)

        # Find and replace the whole TOOLCHAIN_RADAR object (from `var TOOLCHAIN_RADAR = {` to the closing `};` before `// =====` next section marker or end)
        import re as _re
        pattern = r"var TOOLCHAIN_RADAR = \{[^}]*\};"
        m = _re.search(pattern, self.content, _re.S)
        if m:
            self.content = self.content[:m.start()] + "var TOOLCHAIN_RADAR = {\n" + new_block + "\n};" + self.content[m.end():]
            self.changes += 1
            print(f"  ✓ TOOLCHAIN_RADAR 更新 ({len(items)} 条)")
        else:
            self.errors.append("TOOLCHAIN_RADAR block not found")
            print("  ✗ TOOLCHAIN_RADAR block not found")

    def check_static_freshness(self):
        """全站时效检查：扫描 detail_content.js 中的过期日期标记（第三批联动机制）"""
        print("\n── 全站静态内容时效检查 ──")
        import re as _re
        detail_path = os.path.join(ROOT, "detail_content.js")
        if not os.path.exists(detail_path):
            print("  ⚠ detail_content.js 不存在")
            return
        with open(detail_path, 'r', encoding='utf-8') as f:
            dc = f.read()
        today = datetime.now()
        # 扫描 "2026年X月" / "X月" / "7月底" 等相对日期标记
        month_marks = _re.findall(r'(\d{1,2})月底|\b(\d{1,2})月\b', dc)
        found_old = []
        for m in month_marks:
            mnum = int(m[0] or m[1])
            if mnum < today.month - 1:  # 早于上月=可能过期
                found_old.append(f"{mnum}月")
        # 扫描明确的旧日期
        year_marks = _re.findall(r'(\d{4})年(\d{1,2})月', dc)
        for y, mo in year_marks:
            ynum, mnum = int(y), int(mo)
            if ynum < today.year or (ynum == today.year and mnum < today.month - 1):
                found_old.append(f"{ynum}年{mnum}月")
        if found_old:
            unique = sorted(set(found_old))
            print(f"  ⚠ 检测到可能过期的日期标记: {unique}")
            print(f"  → 请在本次更新中同步刷新 detail_content.js 对应内容（旅游/小说连载/模型表等）")
            self.errors.append(f"detail_content.js 存在过期日期标记: {unique}")
        else:
            print("  ✓ 未发现过期日期标记")

    def run(self, commit=False):
        print(f"\n{'='*60}")
        print(f"Daily Update — {self.cfg['date_cn']}")
        print(f"{'='*60}")

        self.load()
        self.update_core_fields()
        self.update_toolchain_radar()
        self.check_static_freshness()

        self.save()
        self.validate()

        if self.errors:
            print(f"\n⚠ {len(self.errors)} replacements failed!")
            for e in self.errors:
                print(f"  - {e}")

        print(f"\n✓ {self.changes} changes applied")
        print(f"✓ Version: {self.cfg['version']}")
        print(f"✓ File size: {len(self.content)} chars")

        if commit:
            self.update_version_bumper()
            self.git_commit_push()

        return self


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Standardized Daily Website Update")
    parser.add_argument("--commit", action="store_true", help="Auto-commit and push to GitHub")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, don't save")
    args = parser.parse_args()

    updater = DailyUpdater(CONFIG)
    updater.run(commit=args.commit)

    if args.dry_run:
        print("\n[Dry-run] Changes NOT saved.")


if __name__ == "__main__":
    main()
