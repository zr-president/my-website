#!/usr/bin/env python3
"""
AI 自动每日更新脚本（替代手动更新模式）
============================================
- 读取昨日 daily_data.js（昨日内容）+ CLAUDE.md 质量规则
- 调用 DeepSeek API 生成今日更新内容（【状态推进】模式：明日→今日、追番第N天→第N+1天、已发生事件→持续状态）
- 结构化写入 daily_data.js + knowledge_base 新文件
- node 语法校验 → git commit + push

用法:
  python scripts/auto_update.py               # 只更新内容不提交
  python scripts/auto_update.py --commit      # 更新 + git commit + push
  python scripts/auto_update.py --dry-run     # 只打印将替换的字段（不写文件）

环境变量（必填）:
  DEEPSEEK_API_KEY   DeepSeek API Key
  本地: set DEEPSEEK_API_KEY=sk-xxx  (Windows) / export DEEPSEEK_API_KEY=sk-xxx (Mac/Linux)
  GitHub Actions 中通过 Secrets.DEEPSEEK_API_KEY 注入

失败安全: API 调用失败或 JSON 解析失败时不改动任何文件，退出码非 0。
"""

import sys, os, io, re, json, subprocess, argparse, requests, shutil
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAILY_DATA_PATH = os.path.join(ROOT, "daily_data.js")
INDEX_PATH = os.path.join(ROOT, "index.html")
KB_DIR = os.path.join(ROOT, "knowledge_base")
DEEPSEEK_API = "https://api.deepseek.com/chat/completions"
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# 17 个必更新板块
ALL_SECTIONS = ['stock','ai-track','movie','news','gaming','career','anime','music',
                'novel','learning','beer','fashion','fitness','diet','car','house','life-tips']
VERDICT_SECTIONS = ['stock','ai-track','news','career']  # 必须带 verdict 的板块


def js_escape(s):
    """把 Python 字符串安全地嵌入 JS 单引号字符串（转义反斜杠/双引号/换行）。"""
    return str(s).replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', '\\n')


# ════════════════════════════════════════════════════════════════════
# 核心替换引擎（复用 daily_update.py 的设计）
# ════════════════════════════════════════════════════════════════════

class Updater:
    def __init__(self):
        self.content = ""
        self.errors = []
        self.changed = []

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
            self.changed.append(label or old[:40])
            print(f"  ✓ {label or old[:40]}")
            return True
        self.errors.append(f"NOT FOUND: {label or old[:50]}")
        print(f"  ✗ 未找到替换目标: {label or old[:50]}")
        return False

    def validate(self):
        try:
            r = subprocess.run(
                ["node", "-e", "new Function(require('fs').readFileSync('daily_data.js','utf8'))"],
                capture_output=True, text=True, timeout=60, cwd=ROOT
            )
            if r.returncode != 0:
                print(f"  ✗ JS 语法错误:\n{r.stderr[:500]}")
                return False
            print("  ✓ JS 语法校验通过")
            return True
        except Exception as e:
            print(f"  ✗ 校验失败: {e}")
            return False

    # #88: 更新前自动备份 + 失败回滚（防数据全损事故）
    def backup(self):
        """更新前备份 daily_data.js 与 index.html，供失败时回滚。"""
        self.backup_files = []
        for p in (DAILY_DATA_PATH, INDEX_PATH):
            if os.path.exists(p):
                bak = p + ".bak-" + datetime.now().strftime("%Y%m%d")
                try:
                    shutil.copy2(p, bak)
                    self.backup_files.append((p, bak))
                    print(f"  📦 已备份 {os.path.basename(p)} → {os.path.basename(bak)}")
                except Exception as e:
                    print(f"  ✗ 备份 {os.path.basename(p)} 失败: {e}")

    def rollback(self):
        """从备份恢复文件（备份不存在则回退 git checkout）。"""
        print("  🔄 回滚中…")
        restored = False
        if hasattr(self, "backup_files"):
            for src, bak in self.backup_files:
                if os.path.exists(bak):
                    try:
                        shutil.copy2(bak, src)
                        print(f"  ✅ 已从备份恢复 {os.path.basename(src)}")
                        restored = True
                    except Exception as e:
                        print(f"  ✗ 恢复 {os.path.basename(src)} 失败: {e}")
        if not restored:
            subprocess.run(["git", "checkout", "--", "daily_data.js", "index.html"], cwd=ROOT)
            print("  ✅ 已 git checkout 回滚 daily_data.js + index.html")


# ════════════════════════════════════════════════════════════════════
# AI 调用
# ════════════════════════════════════════════════════════════════════

def call_ai(system, user, temperature=0.7, max_tokens=6000):
    if not API_KEY:
        print("✗ 缺少环境变量 DEEPSEEK_API_KEY（本地: set DEEPSEEK_API_KEY=sk-xxx）")
        sys.exit(2)
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    try:
        r = requests.post(DEEPSEEK_API, json=payload, headers=headers, timeout=180)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"✗ API 请求失败: {e}")
        sys.exit(3)
    except (KeyError, IndexError, ValueError) as e:
        print(f"✗ API 返回异常: {e}\n{e.args if hasattr(e,'args') else ''}")
        sys.exit(3)


def extract_json(text):
    """剥离 markdown 围栏后解析 JSON。"""
    t = text.strip()
    t = re.sub(r'^```(?:json)?\s*', '', t)
    t = re.sub(r'\s*```$', '', t)
    # 找到第一个 { 到最后一个 }
    s, e = t.find('{'), t.rfind('}')
    if s == -1 or e == -1:
        raise ValueError("AI 输出中没有 JSON 对象")
    return json.loads(t[s:e+1])


# ════════════════════════════════════════════════════════════════════
# 昨日内容摘要（给 AI 的上下文，避免塞入整个 180KB 文件）
# ════════════════════════════════════════════════════════════════════

def summarize_yesterday(content):
    """提取昨日关键字段作为 AI 上下文（约 4-6K 字符）。"""
    out = []

    def grab(pattern, label, limit=500):
        m = re.search(pattern, content, re.S)
        if m:
            out.append(f"【{label}】\n{m.group(1)[:limit]}")

    grab(r'"update_date":\s*"([^"]+)"', "昨日日期")
    grab(r'"market_summary":\s*"([^"]+)"', "昨日市场摘要", 900)
    grab(r'"weather_summary":\s*"([^"]+)"', "昨日天气", 400)
    grab(r'"weekly_focus":\s*"([^"]+)"', "昨日周焦点", 700)
    grab(r'"tip_of_day":\s*"([^"]+)"', "昨日每日叙事", 700)
    # 新闻头条标题
    titles = re.findall(r'\{"title":\s*"([^"]+)"', content)
    if titles:
        out.append("【昨日新闻头条】\n" + "\n".join(titles[:5]))
    # 今日必看（briefing 头条）
    b = re.search(r'headline:\s*"([^"]+)"', content)
    if b:
        out.append(f"【昨日今日必看】\n{b.group(1)[:300]}")
    # INSIGHTS 各板块 summary 首句 + updated
    for sec in ALL_SECTIONS:
        m = re.search(re.escape(sec) + r':\s*\{\s*summary:\s*[\'"]([^\'"]+)', content)
        if m:
            s = m.group(1).replace('\\n', ' ')
            out.append(f"【板块 {sec} 昨日摘要】\n{s[:220]}")
        u = re.search(re.escape(sec) + r':\s*\{[\s\S]*?updated:\s*[\'"]([0-9-]+)', content)
        if u:
            out.append(f"【板块 {sec} updated】{u.group(1)}")
    # 工具链雷达
    g = re.search(r'TOOLCHAIN_RADAR = \{[\s\S]*?headline:\s*"([^"]+)"', content)
    if g:
        out.append(f"【昨日工具链雷达头条】\n{g.group(1)}")
    # 决策单
    d = re.findall(r'action:\s*"([^"]{5,80})"', content)
    if d:
        out.append("【昨日决策单】\n" + "\n".join(d[:5]))
    return "\n\n".join(out)


# ════════════════════════════════════════════════════════════════════
# Prompt 构建
# ════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """你是「钟锐的个人网站」的每日更新编辑。这是一个单HTML+数据文件（daily_data.js）的个人数字空间网站，部署在 GitHub Pages，有 17 个信息板块，每天自动更新。

【每日更新目标】把网站内容从昨天【状态推进】到今天，不是全新创作，而是基于昨日内容的延续刷新。

【状态推进规则】（最重要的规则）
1. 昨日写「明日X」「即将X」「倒计时N天」→ 今天写「今日X」「已X」「追更中/预售中」
2. 昨日写「追番第N天」「开播第N天」→ 今天写「第N+1天」
3. 昨日写「X天后发售」→ 核对日历，今天正好发售则写「今日发售」，未到则写「还有N-1天」
4. 无法确认的新事件：禁止编造具体数字/点位/票房，用「持续」「保持」或基于昨日主线的合理延续
5. 天气/季节：按昨日天气合理推进（如台风停编后高温持续）
6. 股市：如果今天是交易日，基于昨日趋势写【今日展望/操作预案】，不得编造当日收盘点位

【硬规则】
1. 17 个板块全部更新：stock/ai-track/movie/news/gaming/career/anime/music/novel/learning/beer/fashion/fitness/diet/car/house/life-tips
2. 每个板块 summary/trend/tip 必须与昨日有实质差异（状态推进），不能原样复制
3. stock/news/ai-track/career 四板块必须带 verdict 字段（🎯 今日结论：2-4句大白话：发生了什么→意味着什么→该不该动→关注信号）
4. 禁止使用中文单引号 ''，需要强调时用【】
5. 禁止任何个人隐私（存款/收入/失业状态/具体健康数据）
6. 内容必须具体、有信息量，禁止泛泛而谈（如「市场波动需关注」这种空话）
7. tip 字段必须是「今天/本周能做什么」的可行动建议
8. 所有 updated 字段 = 今天日期"""


def build_core_user(today, yesterday):
    return f"""今天是 {today}。
以下是昨日网站内容摘要（你必须在此基础上做状态推进，而不是重写全新内容）：

{yesterday}

请输出今日更新内容的 JSON（只输出 JSON，不要其他文字），结构如下：
{{
  "update_date": "{today}",
  "market_summary": "今日市场/休市摘要（交易日给今日展望，周末给周度复盘+下周展望）",
  "weather_summary": "今日广州天气",
  "weekly_focus": "本周焦点（基于昨日推进）",
  "tip_of_day": "今日N重叙事",
  "news_headlines": [{{"title": "标题", "url": "https://…", "source": "来源", "category": "财经/科技/文娱/游戏"}} × 5],
  "briefing": [{{"priority": 1, "icon": "emoji", "section": "短名", "headline": "头条标题", "summary": "80-150字", "action": "按钮文字", "link": "#板块id", "deepLink": "https://…"}} × 6],
  "decisions": [{{"icon": "emoji", "action": "做什么", "why": "为什么现在", "how": "怎么做", "priority": "P0/P1"}} × 3-5],
  "toolchain": {{"headline": "工具链雷达头条", "items": [{{"topic": "主题", "type": "新工具/价格变化/替代方案/模型更新/生态观察", "summary": "发生了什么", "impact": "对我意味着什么", "action": "我要不要行动"}} × 3-5]}}
}}
注意：briefing 的 link 用 #stock/#ai-track/#movie/#gaming/#career/#news 等真实板块锚点。"""


def build_insights_user(today, yesterday):
    return f"""今天是 {today}。
以下是昨日 17 个板块的摘要（基于此做状态推进，updated 全部改为 {today}）：

{yesterday}

请输出 17 个板块的今日内容 JSON（只输出 JSON），结构如下：
{{
  "insights": {{
    "stock": {{"verdict": "🎯 今日结论（小白版）：…", "summary": "…", "trend": "…", "tip": "…", "reasoning": "🔍发生了什么→🤔为什么→📊术语解释→💡启示 四层精简版", "updated": "{today}"}},
    "anime": {{"summary": "…", "trend": "…", "tip": "…", "updated": "{today}"}},
    …共17个板块（stock/ai-track/movie/news/gaming/career/anime/music/novel/learning/beer/fashion/fitness/diet/car/house/life-tips）
  }}
}}
要求：
- stock/news/ai-track/career 必须带 verdict
- summary 控制在 100-200 字，trend/tip 各 80-150 字，reasoning 四层各 1-2 句
- 每个板块 tip 给「今天/本周能做什么」的可行动建议
- 娱乐板块（anime/gaming/movie/music/novel）即使没有大事件也要刷新为「当前状态」（如「追番中/已开播/预售中」），禁止留空"""


def build_learning_user(today, yesterday):
    return f"""今天是 {today}。
以下是昨日内容摘要（基于此做状态推进）：

{yesterday}

请输出今日学习类内容 JSON（只输出 JSON），结构如下：
{{
  "vocab": [{{"emoji": "…", "category": "AI/金融/科技/游戏/影视/健身/生活", "word": "术语", "definition": "定义+类比", "example": "结合今日热点举例", "why_matters": "为什么重要"}} × 10],
  "learn": [{{"section": "股市/AI/求职/健身/饮食/影视/游戏/理财/生活", "emoji": "…", "title": "科普标题", "content": "80-150字讲解", "takeaway": "一句话记忆点"}} × 10],
  "opt": [{{"cat": "内容优化/体验优化/稳定性/性能优化/数据优化", "title": "优化建议标题", "desc": "建议描述（注明 ✅今日已实施 或 待办）", "priority": "P0/P1/P2/P3", "status": "已完成/待办"}} × 3-5],
  "picks": {{
    "anime": [{{"icon": "🥇", "title": "…", "desc": "…", "link": "https://…", "video": "https://search.bilibili.com/…"}}],
    "gaming": [...],
    "movie": [...],
    "music": [...],
    "novel": [...],
    "beer": [...],
    "learning": [...],
    "ai-track": [...]
  }}
}}
要求：
- vocab/learn 不得与昨日重复（昨日摘要中出现的标题请换新知识点）
- opt 新增建议从 #71 开始编号（说明：当前最大编号是 70）
- picks 每板块 3-7 条，desc 带日期状态（如「预售中」「追番第N天」）"""


# ════════════════════════════════════════════════════════════════════
# 写入逻辑
# ════════════════════════════════════════════════════════════════════

def apply_core(u, d, today):
    """写入 DAILY_DATA 头部 + briefing + decisions + toolchain。"""
    date_cn = d.get("update_date", today)
    # 头部日期（动态正则匹配，不硬编码具体日期——否则跨月/跨年后无法匹配）
    m_date = re.search(r'"update_date":\s*"[^"]*"', u.content)
    if m_date:
        u.content = u.content.replace(m_date.group(0), f'"update_date": "{date_cn}"', 1)
        u.changed.append("update_date")
        print("  ✓ update_date")
    m_time = re.search(r'"update_time":\s*"[^"]*"', u.content)
    if m_time:
        u.content = u.content.replace(m_time.group(0), f'"update_time": "{today}T10:30:00+08:00"', 1)
        u.changed.append("update_time")
        print("  ✓ update_time")
    # --- 整体替换 market_summary ---
    m = re.search(r'"market_summary":\s*"[^"]*"', u.content)
    if m and d.get("market_summary"):
        u.content = u.content.replace(m.group(0), f'"market_summary": "{d["market_summary"]}"', 1)
        u.changed.append("market_summary")
        print("  ✓ market_summary")
    # weather / weekly / tip
    for key, label in [("weather_summary", "weather_summary"), ("weekly_focus", "weekly_focus"), ("tip_of_day", "tip_of_day")]:
        if d.get(key):
            m = re.search(r'"' + key + r'":\s*"[^"]*"', u.content)
            if m:
                u.content = u.content.replace(m.group(0), f'"{key}": "{d[key]}"', 1)
                u.changed.append(label)
                print(f"  ✓ {label}")
    # news_headlines
    if d.get("news_headlines"):
        m = re.search(r'"news_headlines":\s*\[[\s\S]*?\n  \]', u.content)
        if m:
            new_headlines = '"news_headlines": [\n' + ",\n".join(
                '    {"title": "%s", "url": "%s", "source": "%s", "category": "%s"}' % (
                    js_escape(h["title"]), js_escape(h["url"]), js_escape(h["source"]), js_escape(h["category"]))
                for h in d["news_headlines"]) + '\n  ]'
            u.content = u.content.replace(m.group(0), new_headlines, 1)
            u.changed.append("news_headlines")
            print("  ✓ news_headlines")
    # briefing date + highlights
    if d.get("briefing"):
        m = re.search(r'var DAILY_BRIEFING = \{[\s\S]*?\n\};', u.content)
        if m:
            new_brief = 'var DAILY_BRIEFING = {\n  date: "' + today + '",\n  highlights: [\n' + ",\n".join(
                '    {priority:%d, icon:"%s", section:"%s", headline:"%s", summary:"%s", action:"%s", link:"%s", deepLink:"%s"}' % (
                    h["priority"], js_escape(h["icon"]), js_escape(h["section"]), js_escape(h["headline"]),
                    js_escape(h["summary"]), js_escape(h.get("action", "查看详情")),
                    js_escape(h.get("link", "#ai-track")), js_escape(h.get("deepLink", "https://example.com")))
                for h in d["briefing"]) + '\n  ]\n\n};'
            u.content = u.content.replace(m.group(0), new_brief, 1)
            u.changed.append("DAILY_BRIEFING")
            print("  ✓ DAILY_BRIEFING")
    # decisions
    if d.get("decisions"):
        m = re.search(r'var DAILY_DECISIONS = \{[\s\S]*?\n\};', u.content)
        if m:
            new_dec = 'var DAILY_DECISIONS = {\n  updated: "' + today + '",\n  items: [\n' + ",\n".join(
                '    {icon:"%s", action:"%s", why:"%s", how:"%s", priority:"%s"}' % (
                    js_escape(x["icon"]), js_escape(x["action"]), js_escape(x["why"]), js_escape(x["how"]), js_escape(x["priority"]))
                for x in d["decisions"]) + '\n  ]\n};'
            u.content = u.content.replace(m.group(0), new_dec, 1)
            u.changed.append("DAILY_DECISIONS")
            print("  ✓ DAILY_DECISIONS")
    # toolchain radar
    if d.get("toolchain"):
        m = re.search(r'var TOOLCHAIN_RADAR = \{[\s\S]*?\n\};', u.content)
        if m:
            items = ",\n".join(
                '    {\n      topic: "%s",\n      type: "%s",\n      summary: "%s",\n      impact: "%s",\n      action: "%s"\n    }' % (
                    js_escape(it["topic"]), js_escape(it["type"]), js_escape(it["summary"]),
                    js_escape(it["impact"]), js_escape(it["action"]))
                for it in d["toolchain"]["items"])
            new_radar = 'var TOOLCHAIN_RADAR = {\n  updated: "' + today + '",\n  headline: "' + js_escape(d["toolchain"]["headline"]) + '",\n  items: [\n' + items + '\n  ]\n};'
            u.content = u.content.replace(m.group(0), new_radar, 1)
            u.changed.append("TOOLCHAIN_RADAR")
            print("  ✓ TOOLCHAIN_RADAR")


def apply_insights(u, d, today):
    """写入 INSIGHTS 17 板块。"""
    insights = d.get("insights", {})
    if not insights:
        print("  ! AI 未返回 insights，跳过")
        return
    for sec in ALL_SECTIONS:
        sec_data = insights.get(sec)
        if not sec_data:
            print(f"  ✗ 缺少板块 {sec}")
            u.errors.append(f"missing section {sec}")
            continue
        # 用正则定位该板块对象并整块替换
        pattern = re.compile(
            r'(?<=\n)  ' + re.escape(sec) + r':\s*\{[\s\S]*?(?=\n  \w[\w-]*: \{\n|^\})',
        )
        # 简化：定位 "sec": { 到下一个顶层 key 或 INSIGHTS 结束
        m = re.search(re.escape(sec) + r':\s*\{', u.content)
        if not m:
            print(f"  ✗ 未找到板块 {sec}")
            u.errors.append(f"section {sec} not found")
            continue
        start = m.start()
        # 从 start 找匹配的大括号
        depth = 0
        i = u.content.find('{', start)
        j = i
        while j < len(u.content):
            if u.content[j] == '{':
                depth += 1
            elif u.content[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        old_block = u.content[start:j+1]
        # 组装新块
        parts = [f'  {sec}: {{']
        if sec in VERDICT_SECTIONS and sec_data.get("verdict"):
            parts.append("    verdict: '" + js_escape(sec_data["verdict"]) + "',")
        for k in ["summary", "trend", "tip", "reasoning"]:
            if sec_data.get(k):
                v = js_escape(sec_data[k])
                parts.append(f"    {k}: '{v}',")
        parts.append(f"    updated: '{today}'")
        parts.append("  },")
        new_block = "\n".join(parts)
        u.content = u.content[:start] + new_block + u.content[j+1:]
        u.changed.append(f"INSIGHTS.{sec}")
        print(f"  ✓ INSIGHTS.{sec}")
    # 更新 INSIGHTS_TODAY_UPDATED 为全部 17 板块
    m = re.search(r"var INSIGHTS_TODAY_UPDATED = \[[^\]]*\]", u.content)
    if m:
        u.content = u.content.replace(m.group(0), "var INSIGHTS_TODAY_UPDATED = " + json.dumps(ALL_SECTIONS, ensure_ascii=False), 1)
        u.changed.append("INSIGHTS_TODAY_UPDATED")
        print("  ✓ INSIGHTS_TODAY_UPDATED")


def apply_learning(u, d, today):
    """写入 DAILY_VOCAB + LEARN_PATHS（archive 迁移）+ OPTIMIZATION_LOG 新增 + PICKS。"""
    # --- DAILY_VOCAB ---
    if d.get("vocab"):
        m = re.search(r'var DAILY_VOCAB = \{[\s\S]*?\n\};', u.content)
        if m:
            words = ",\n".join(
                '    {emoji:"%s", category:"%s", word:"%s", definition:"%s", example:"%s", why_matters:"%s"}' % (
                    js_escape(w["emoji"]), js_escape(w["category"]), js_escape(w["word"]),
                    js_escape(w["definition"]), js_escape(w["example"]), js_escape(w["why_matters"]))
                for w in d["vocab"])
            new_vocab = 'var DAILY_VOCAB = {\n  date: "' + today + '",\n  words: [\n' + words + '\n  ]\n};'
            u.content = u.content.replace(m.group(0), new_vocab, 1)
            u.changed.append("DAILY_VOCAB")
            print("  ✓ DAILY_VOCAB")

    # --- LEARN_PATHS：archive 迁移 + 新 items ---
    if d.get("learn"):
        m = re.search(r'var LEARN_PATHS = \{[\s\S]*?\n\};', u.content)
        if m:
            old_block = m.group(0)
            old_date = re.search(r'updated:\s*"([0-9-]+)"', old_block).group(1)
            # 提取旧 items
            items_m = re.search(r'items:\s*\[([\s\S]*?)\n  \],', old_block)
            old_items_raw = items_m.group(1) if items_m else ""
            # 提取旧 current_day
            cd = re.search(r'current_day:\s*(\d+)', old_block)
            new_day = int(cd.group(1)) + 1 if cd else 1
            # 组装新 LEARN_PATHS：旧 items 放进 archive[old_date]，新 items 放 items
            new_items = ",\n".join(
                '    {section:"%s", emoji:"%s", title:"%s", content:"%s", takeaway:"%s"}' % (
                    js_escape(x["section"]), js_escape(x["emoji"]), js_escape(x["title"]),
                    js_escape(x["content"]), js_escape(x["takeaway"]))
                for x in d["learn"])
            new_block = ('var LEARN_PATHS = {\n'
                         '  updated: "' + today + '",\n'
                         '  current_day: ' + str(new_day) + ',           // 当前学到第几天\n'
                         '  items: [\n' + new_items + '\n  ],\n'
                         '  // 历史累积库：archive 只存【历史】日期（当天内容放 items，不进 archive）\n'
                         '  // 更新流程：每次更新时 ①把 items 追加到 archive[旧日期] ②items 换成新10条 ③updated 更新为新日期\n'
                         '  // 渲染时自动排除 archive 中与 updated 同日的条目 + 按标题去重，不会重复显示\n'
                         '  archive: {\n'
                         '    "' + old_date + '": [\n' + old_items_raw + '\n    ]\n'
                         '  }\n};')
            u.content = u.content.replace(m.group(0), new_block, 1)
            u.changed.append("LEARN_PATHS")
            print("  ✓ LEARN_PATHS (archive 迁移 → " + old_date + ")")

    # --- OPTIMIZATION_LOG：新增建议 + totals ---
    if d.get("opt"):
        m = re.search(r'var OPTIMIZATION_LOG = \{[\s\S]*?\n\};', u.content)
        if m:
            block = m.group(0)
            total_m = re.search(r'total_suggestions:\s*(\d+)', block)
            cur_total = int(total_m.group(1)) if total_m else 0
            max_id = max([int(x) for x in re.findall(r'\{id:(\d+)', block)] or [cur_total])
            new_entries = []
            for x in d["opt"]:
                max_id += 1
                new_entries.append('    {id:%d, cat:"%s", title:"%s", desc:"%s", priority:"%s", status:"%s"}' % (
                    max_id, js_escape(x["cat"]), js_escape(x["title"]), js_escape(x["desc"]),
                    js_escape(x["priority"]), js_escape(x["status"])))
            # 在最后一个 ] 前插入
            new_block = block.rstrip()
            new_block = new_block[:new_block.rfind(']')] + ",\n" + ",\n".join(new_entries) + "\n  ]\n};"
            new_block = re.sub(r'total_suggestions:\s*\d+', f'total_suggestions: {cur_total + len(new_entries)}', new_block, count=1)
            # streak +1
            new_block = re.sub(r'streak_days:\s*\d+', lambda mm: f'streak_days: {int(mm.group(0).split(":")[1]) + 1}', new_block, count=1)
            # date 更新
            new_block = re.sub(r'date:\s*"[0-9-]+"', f'date: "{today}"', new_block, count=1)
            u.content = u.content.replace(m.group(0), new_block, 1)
            u.changed.append("OPTIMIZATION_LOG")
            print(f"  ✓ OPTIMIZATION_LOG (+{len(new_entries)} 条新建议)")

    # --- PICKS 部分板块 ---
    if d.get("picks"):
        for key, items in d["picks"].items():
            if not items:
                continue
            m = re.search(r'  ' + re.escape(key) + r':\s*\[', u.content)
            if not m:
                continue
            start = m.start()
            depth = 0
            i = u.content.find('[', start)
            j = i
            while j < len(u.content):
                if u.content[j] == '[':
                    depth += 1
                elif u.content[j] == ']':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            old_block = u.content[start:j+1]
            rows = []
            for it in items:
                parts = ['    {icon:"%s", title:"%s", desc:"%s", link:"%s"' % (
                    js_escape(it["icon"]), js_escape(it["title"]), js_escape(it["desc"]), js_escape(it["link"]))]
                if it.get("video"):
                    parts.append(' video:"%s"' % js_escape(it["video"]))
                parts.append("},")
                rows.append("".join(parts))
            new_block = f'  {key}: [\n' + "\n".join(rows) + '\n  ]'
            u.content = u.content.replace(old_block, new_block, 1)
            u.changed.append(f"PICKS.{key}")
            print(f"  ✓ PICKS.{key}")


def bump_version(u):
    """版本号三处同步：SITE_VERSION + index.html 缓存符 + WEBSITE_GUIDE。"""
    m = re.search(r'var SITE_VERSION = "(\d+)\.(\d+)\.(\d+)"', u.content)
    if not m:
        print("  ✗ 找不到 SITE_VERSION")
        return
    ma, mi, pa = int(m.group(1)), int(m.group(2)), int(m.group(3))
    pa += 1
    if pa > 9:
        pa = 0
        mi += 1
    if mi > 9:
        mi = 0
        ma += 1
    new_v = f"{ma}.{mi}.{pa}"
    old_v = m.group(0)
    u.content = u.content.replace(old_v, f'var SITE_VERSION = "{new_v}"', 1)
    print(f"  ✓ SITE_VERSION → {new_v}")
    # index.html 缓存符
    try:
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            idx = f.read()
        old_bump = f"daily_data.js?v={old_v.split('\"')[1]}"
        new_bump = f"daily_data.js?v={new_v}"
        if old_bump in idx:
            idx = idx.replace(old_bump, new_bump)
            with open(INDEX_PATH, 'w', encoding='utf-8') as f:
                f.write(idx)
            print(f"  ✓ index.html 缓存符 → {new_v}")
    except Exception as e:
        print(f"  ✗ index.html 缓存符更新失败: {e}")
    # WEBSITE_GUIDE summary 中的版本号
    m2 = re.search(r'(版本)[\d.]+', u.content)
    if m2:
        u.content = u.content.replace(m2.group(0), f"版本{new_v}", 1)
        print(f"  ✓ WEBSITE_GUIDE 版本号 → {new_v}")


def write_kb(d, today):
    """写入 knowledge_base 当日文件（核心板块）。"""
    sections_kb = {
        "ai": ["Qwen/DeepSeek/Claude 等 AI 动态"],
        "stock": ["股市"],
        "news": ["综合新闻"],
        "learning": ["学习"],
        "career": ["求职"],
    }
    for name, _ in sections_kb.items():
        path = os.path.join(KB_DIR, name, f"{today}.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            continue
        # 从 AI 输出中无法直接获得 KB 文本，写一个结构化摘要（从简报/insights 提炼）
        lines = [f"# {name} · {today}", ""]
        content_today = d.get("briefing", [])
        for h in content_today[:6]:
            lines.append(f"## {h['section']}: {h['headline']}")
            lines.append(h["summary"])
            lines.append("")
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print(f"  ✓ knowledge_base/{name}/{today}.md")


def git_commit_push(msg):
    cmds = [
        ["git", "add", "-A"],
        ["git", "commit", "-m", msg],
        ["git", "push"],
    ]
    for c in cmds:
        r = subprocess.run(c, capture_output=True, text=True, cwd=ROOT)
        print("  " + " ".join(c), "→", r.returncode)
        if r.returncode != 0 and "nothing to commit" not in r.stderr:
            print(r.stderr[:500])
            return False
    return True


# ════════════════════════════════════════════════════════════════════
# main
# ════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="AI 自动每日更新")
    ap.add_argument("--commit", action="store_true", help="更新后自动 git commit + push")
    ap.add_argument("--dry-run", action="store_true", help="只打印将执行的替换，不写文件")
    ap.add_argument("--today", default="", help="指定今日日期 YYYY-MM-DD（默认取系统日期）")
    args = ap.parse_args()

    if args.today:
        today = args.today
    else:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

    print(f"🚀 AI 自动更新开始 — 目标日期 {today}")

    u = Updater().load()
    # #88: 更新前自动备份（daily_data.js + index.html）
    u.backup()
    yesterday_summary = summarize_yesterday(u.content)
    if not yesterday_summary:
        print("✗ 无法提取昨日内容摘要")
        sys.exit(1)

    # 1) 核心简报
    print("\n[1/3] 生成核心简报…")
    core_json = call_ai(SYSTEM_PROMPT, build_core_user(today, yesterday_summary))
    d_core = extract_json(core_json)
    apply_core(u, d_core, today)

    # 2) INSIGHTS 17 板块
    print("\n[2/3] 生成 17 板块 INSIGHTS…")
    ins_json = call_ai(SYSTEM_PROMPT, build_insights_user(today, yesterday_summary), temperature=0.7, max_tokens=8000)
    d_ins = extract_json(ins_json)
    apply_insights(u, d_ins, today)

    # 3) 学习类 + 优化日记 + picks
    print("\n[3/3] 生成词汇/课堂/优化建议…")
    learn_json = call_ai(SYSTEM_PROMPT, build_learning_user(today, yesterday_summary), temperature=0.7, max_tokens=8000)
    d_learn = extract_json(learn_json)
    apply_learning(u, d_learn, today)

    # 版本号三处
    print("\n[版本] 同步版本号…")
    bump_version(u)

    if args.dry_run:
        print("\n[dry-run] 检测到 --dry-run，不写文件。将替换的字段：")
        for c in u.changed:
            print("  -", c)
        if u.errors:
            print("\n错误：", u.errors)
        return

    # 校验 + 保存
    u.save()
    print("\n[校验] node 语法校验…")
    if not u.validate():
        print("✗ 语法校验失败——从备份恢复文件（daily_data.js + index.html）")
        u.rollback()
        sys.exit(4)

    # knowledge_base
    print("\n[知识库] 生成当日文件…")
    write_kb(d_core, today)

    # 提交推送
    if args.commit:
        print("\n[提交] git commit + push…")
        date_cn = today.replace("-", "年", 1).replace("-", "月", 1) + "日"
        ok = git_commit_push(f"AI自动更新 {date_cn}")
        if not ok:
            print("✗ 提交失败（可能无变更或无推送权限）")
            sys.exit(5)
    else:
        print("\n✅ 内容已更新（未提交）。用 --commit 可自动提交推送。")

    print(f"\n✅ 完成！共替换 {len(u.changed)} 处。错误 {len(u.errors)} 处。")
    if u.errors:
        print("注意以下未找到的目标（可能已是最新）：")
        for e in u.errors:
            print("  -", e)


if __name__ == "__main__":
    main()
