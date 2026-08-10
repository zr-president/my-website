#!/usr/bin/env python3
"""
Life OS Push Script
Reads daily_data.js + personal_config.js, formats personalized briefings,
sends via PushPlus WeChat push.

Usage:
  python scripts/life_os_push.py --mode morning    # 08:00 briefing
  python scripts/life_os_push.py --mode midday     # 12:00 check-in
  python scripts/life_os_push.py --mode evening    # 18:00 entertainment
  python scripts/life_os_push.py --mode night      # 22:00 review
  python scripts/life_os_push.py --mode test       # test (sends all-in-one)
  python scripts/life_os_push.py --mode morning --dry-run  # preview only
"""

import sys, os, re, json, argparse, subprocess, textwrap, io
from datetime import datetime

# Fix Unicode output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAILY_DATA_PATH = os.path.join(ROOT, "daily_data.js")
PERSONAL_CONFIG_PATH = os.path.join(ROOT, "personal_config.js")
PUSHPLUS_API = "https://www.pushplus.plus/send"


# ---------------------------------------------------------------------------
# JS → JSON extraction via Node.js
# ---------------------------------------------------------------------------

def _run_node(script):
    """Run a Node.js one-liner and return parsed JSON, or None on failure."""
    try:
        result = subprocess.run(
            ["node", "-e", script],
            capture_output=True, text=True, timeout=30, cwd=ROOT
        )
        if result.returncode != 0:
            print(f"[WARN] Node.js error: {result.stderr[:200]}", file=sys.stderr)
            return None
        return json.loads(result.stdout.strip())
    except Exception as e:
        print(f"[WARN] Node.js extraction failed: {e}", file=sys.stderr)
        return None


def extract_js_vars(filepath, var_names):
    """
    Extract multiple JS variables from a file as a dict {name: value}.
    Uses Node.js with the script piped via stdin to avoid encoding issues.
    """
    if not os.path.exists(filepath):
        print(f"[WARN] File not found: {filepath}", file=sys.stderr)
        return {}

    # Use forward slashes (Node.js handles both on Windows)
    abs_path = os.path.abspath(filepath).replace("\\", "/")

    var_prints = "\n".join(
        "console.log('---{}---'); console.log(JSON.stringify(typeof sandbox.{} !== 'undefined' ? sandbox.{} : null));".format(n, n, n)
        for n in var_names
    )

    js_code = """var fs = require('fs');
var vm = require('vm');
var code = fs.readFileSync('{}', 'utf8');

var sandbox = {{
    console: console,
    setTimeout: function() {{}},
    setInterval: function() {{}},
    onDataReady: function() {{}},
    renderAllPicks: function() {{}},
    renderBriefing: function() {{}},
    renderVocab: function() {{}},
    renderQuiz: function() {{}},
    renderMusicPlayer: function() {{}},
    renderModelComparison: function() {{}},
    checkUpdateStatus: function() {{}},
    renderTodos: function() {{}},
    HOME_SECTIONS: [],
    document: {{ getElementById: function() {{ return {{}}; }} }},
    window: {{}},
    fetch: function() {{}},
    XMLHttpRequest: function() {{}},
    module: {{ exports: {{}} }},
}};
vm.createContext(sandbox);

try {{
    vm.runInContext(code, sandbox);
    {}
}} catch(e) {{
    console.error('JS eval error:', e.message);
}}""".format(abs_path, var_prints)

    # Use Popen with stdin to avoid command-line encoding issues on Windows
    proc = subprocess.Popen(
        ["node"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        cwd=ROOT
    )
    stdout, stderr = proc.communicate(input=js_code, timeout=30)

    if proc.returncode != 0:
        print(f"[WARN] Node.js error: {stderr[:300]}", file=sys.stderr)
        return _extract_fallback(filepath, var_names)

    # Parse the interleaved output
    result = {}
    current_name = None
    current_json = []
    for line in stdout.split("\n"):
        if line.startswith("---") and line.endswith("---"):
            if current_name and current_json:
                try:
                    result[current_name] = json.loads("".join(current_json))
                except json.JSONDecodeError:
                    result[current_name] = None
            current_name = line.strip("-")
            current_json = []
        elif current_name:
            current_json.append(line)

    if current_name and current_json:
        try:
            result[current_name] = json.loads("".join(current_json))
        except json.JSONDecodeError:
            result[current_name] = None

    return result


def _extract_fallback(filepath, var_names):
    """Simpler extraction without vm sandbox. Uses eval() approach."""
    abs_path = os.path.abspath(filepath).replace("\\", "/")

    var_prints = "\n".join(
        "console.log('---{}---'); console.log(JSON.stringify(typeof {} !== 'undefined' ? {} : null));".format(n, n, n)
        for n in var_names
    )

    js_code = """var fs = require('fs');
globalThis.onDataReady = function() {{}};
globalThis.renderAllPicks = function() {{}};
globalThis.renderBriefing = function() {{}};
globalThis.renderVocab = function() {{}};
globalThis.renderQuiz = function() {{}};
globalThis.renderMusicPlayer = function() {{}};
globalThis.renderModelComparison = function() {{}};
globalThis.checkUpdateStatus = function() {{}};
globalThis.renderTodos = function() {{}};
globalThis.HOME_SECTIONS = [];
globalThis.document = {{ getElementById: function() {{ return {{}}; }} }};
globalThis.window = {{}};
globalThis.module = {{ exports: {{}} }};

var code = fs.readFileSync('{}', 'utf8');
eval(code);
{}""".format(abs_path, var_prints)

    proc = subprocess.Popen(
        ["node"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        cwd=ROOT
    )
    stdout, stderr = proc.communicate(input=js_code, timeout=30)

    if proc.returncode != 0:
        print(f"[WARN] Fallback extraction also failed: {stderr[:300]}", file=sys.stderr)
        return {}

    result = {}
    current_name = None
    current_json = []
    for line in stdout.split("\n"):
        if line.startswith("---") and line.endswith("---"):
            if current_name and current_json:
                try:
                    result[current_name] = json.loads("".join(current_json))
                except json.JSONDecodeError:
                    result[current_name] = None
            current_name = line.strip("-")
            current_json = []
        elif current_name:
            current_json.append(line)

    if current_name and current_json:
        try:
            result[current_name] = json.loads("".join(current_json))
        except json.JSONDecodeError:
            result[current_name] = None

    return result


# ---------------------------------------------------------------------------
# Content builders for each push mode
# ---------------------------------------------------------------------------

def _safe_get(d, *keys, default=""):
    """Safely navigate nested dicts."""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d if d is not None else default


def _pick(items, key, fallback=""):
    """Pick a field from dict, return fallback if missing."""
    if isinstance(items, dict):
        return items.get(key, fallback)
    return fallback


def build_morning(data, config):
    """Build 08:00 morning briefing."""
    daily = data.get("DAILY_DATA", {})
    briefing = data.get("DAILY_BRIEFING", {})
    insights = data.get("INSIGHTS", {})
    vocab = data.get("DAILY_VOCAB", {})
    profile = config.get("profile", {})
    watchlist = config.get("watchlist", {})

    today = datetime.now().strftime("%Y年%m月%d日")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]

    lines = [
        f"## ☀️ 早上好，{_safe_get(profile, 'name', default='钟锐')}！",
        f"**{today} {weekday}**  |  {_safe_get(profile, 'city', default='广州')} · {_safe_get(daily, 'weather_summary', default='天气数据待更新')}",
        "",
    ]

    # --- Stock Brief ---
    market = _safe_get(daily, "market_summary", default="")
    if market:
        lines.append("### 📈 股市速览")
        lines.append(market)
        lines.append("")

    # --- Top News ---
    headlines = _safe_get(daily, "news_headlines", default=[])
    if headlines and len(headlines) > 0:
        lines.append("### 📰 今日要闻")
        for h in headlines[:3]:
            if isinstance(h, dict):
                lines.append(f"- **{_pick(h, 'title')}** ({_pick(h, 'source')})")
        lines.append("")

    # --- Job Progress ---
    job_cfg = config.get("job", {})
    if job_cfg:
        lines.append("### 💼 求职追踪")
        lines.append(f"- 本周目标：投递 **{_safe_get(job_cfg, 'weekly_target', default='15')}** 份")
        lines.append(f"- 目标岗位：{' / '.join(_safe_get(profile, 'target_roles', default=['AI产品运营']))}")
        lines.append(f"- 投递窗口：上午 9:30-11:00 是黄金时间")
        lines.append("")

    # --- Daily Vocab ---
    words = _safe_get(vocab, "words", default=[])
    if words and len(words) > 0:
        w = words[0] if isinstance(words[0], dict) else {}
        lines.append("### 💡 每日一词")
        lines.append(f"**{_pick(w, 'word')}** {_pick(w, 'emoji')} — {_pick(w, 'definition')}")
        lines.append(f"> {_pick(w, 'why_matters')}")
        lines.append("")

    # --- Tip of the Day ---
    tip = _safe_get(daily, "tip_of_day", default="")
    if tip:
        # Truncate long tips
        if len(tip) > 200:
            tip = tip[:200] + "..."
        lines.append("### 💭 今日箴言")
        lines.append(f"> {tip}")
        lines.append("")

    lines.append("---")
    lines.append(f"📱 [打开个人网站](https://zr-president.github.io/my-website/) | ⏰ 下次推送：12:00 午间更新")

    return "\n".join(lines)


def build_midday(data, config):
    """Build 12:00 midday check-in."""
    daily = data.get("DAILY_DATA", {})
    insights = data.get("INSIGHTS", {})
    profile = config.get("profile", {})
    dietary = _safe_get(profile, "dietary", default=[])

    lines = [
        "## 🔄 午间更新 · 中场休息",
        "",
    ]

    # --- AI Track ---
    ai_insight = _safe_get(insights, "ai-track", default={})
    if ai_insight:
        lines.append("### 🤖 AI 行业快讯")
        lines.append(_safe_get(ai_insight, "summary", default=""))
        trend = _safe_get(ai_insight, "trend", default="")
        if trend:
            lines.append(f"📊 趋势：{trend}")
        lines.append("")

    # --- Diet Reminder ---
    if dietary:
        lines.append("### 🍽️ 饮食提醒")
        notes = "、".join(dietary) if isinstance(dietary, list) else str(dietary)
        lines.append(f"⚠️ 注意：{notes}")
        lines.append("- 🥗 午餐推荐：高蛋白 + 多蔬菜 + 适量碳水")
        lines.append("- 💧 下午目标：再喝 1L 水（全天目标 2.5L）")
        lines.append("- 🚶 饭后走动 10 分钟，别久坐")
        lines.append("")

    # --- Stock midday snapshot ---
    market = _safe_get(daily, "market_summary", default="")
    if market:
        lines.append("### 📈 午间大盘")
        lines.append(f"{market[:150]}...")
        lines.append("")

    lines.append("---")
    lines.append(f"📱 [打开个人网站](https://zr-president.github.io/my-website/) | ⏰ 下次推送：18:00 晚间推荐")

    return "\n".join(lines)


def build_evening(data, config):
    """Build 18:00 evening entertainment picks."""
    daily = data.get("DAILY_DATA", {})
    picks = data.get("PICKS", {})
    insights = data.get("INSIGHTS", {})
    prefs = config.get("preferences", {})
    profile = config.get("profile", {})

    lines = [
        "## 🌅 晚间推荐 · 放松时刻",
        "",
    ]

    # --- Fitness ---
    fitness = _safe_get(insights, "fitness", default={})
    if fitness:
        lines.append("### 🏋️ 健身提醒")
        lines.append(_safe_get(fitness, "tip", default="今日记得完成训练！"))
        lines.append(f"📌 第{_safe_get(profile, 'fitness_week', default='?')}周 · 目标：{_safe_get(profile, 'fitness_goal', default='增肌')}")
        lines.append("")

    # --- Anime/Movie/Novel picks ---
    lines.append("### 🎬 今日推荐")

    anime_picks = _safe_get(picks, "anime", default=[])
    if anime_picks and len(anime_picks) > 0:
        a = anime_picks[0] if isinstance(anime_picks[0], dict) else {}
        lines.append(f"- 📺 动漫：**{_pick(a, 'title')}** — {_pick(a, 'desc')}")

    movie = _safe_get(insights, "movie", default={})
    if movie:
        lines.append(f"- 🎥 电影：{_safe_get(movie, 'summary', default='')[:150]}")

    novel_picks = _safe_get(picks, "novel", default=[])
    if novel_picks and len(novel_picks) > 0:
        n = novel_picks[0] if isinstance(novel_picks[0], dict) else {}
        lines.append(f"- 📖 小说：**{_pick(n, 'title')}** — {_pick(n, 'desc')}")

    music_rec = _safe_get(daily, "daily_recommendation", "music", default={})
    if isinstance(music_rec, dict):
        lines.append(f"- 🎵 音乐：**{_pick(music_rec, 'title')}** — {_pick(music_rec, 'desc')}")

    lines.append("")

    # --- Learning ---
    learning = _safe_get(insights, "learning", default={})
    if learning:
        lines.append("### 📚 学习提醒")
        lines.append(_safe_get(learning, "tip", default="今日学习目标别忘记！"))
        lines.append("")

    lines.append("---")
    lines.append(f"📱 [打开个人网站](https://zr-president.github.io/my-website/) | ⏰ 下次推送：22:00 今日复盘")

    return "\n".join(lines)


def build_night(data, config):
    """Build 22:00 night review."""
    daily = data.get("DAILY_DATA", {})
    insights = data.get("INSIGHTS", {})
    vocab = data.get("DAILY_VOCAB", {})
    today_updated = data.get("INSIGHTS_TODAY_UPDATED", [])
    profile = config.get("profile", {})

    lines = [
        "## 🌙 今日复盘 · 晚安",
        "",
    ]

    # --- Today's Highlights ---
    weekly = _safe_get(daily, "weekly_focus", default="")
    if weekly:
        lines.append("### 📊 本周要点")
        lines.append(f"> {weekly[:200]}")
        lines.append("")

    # --- INSIGHTS Updated Today ---
    if today_updated and len(today_updated) > 0:
        lines.append(f"### 📖 今日分析更新（{len(today_updated)}个板块）")
        for key in today_updated[:5]:
            section = _safe_get(insights, key, default={})
            if section:
                summary = _safe_get(section, "summary", default="")
                if summary:
                    lines.append(f"- **{key}**：{summary[:120]}")
        lines.append("")

    # --- Career ---
    career = _safe_get(insights, "career", default={})
    if career:
        lines.append("### 💼 求职洞察")
        lines.append(_safe_get(career, "summary", default=""))
        tip = _safe_get(career, "tip", default="")
        if tip:
            lines.append(f"💡 {tip}")
        lines.append("")

    # --- Reflection Prompt ---
    lines.append("### 📝 今日反思")
    lines.append("- 今天完成了什么？有什么收获？")
    lines.append("- 求职投递进度如何？明天计划做什么？")
    lines.append("- 健身完成了吗？饮食注意了吗？")
    lines.append("")

    # --- Tomorrow Preview ---
    lines.append("### 🔮 明日预告")
    news_insight = _safe_get(insights, "news", default={})
    if news_insight:
        lines.append(f"- {_safe_get(news_insight, 'trend', default='持续关注AI行业动态')}")
    stock_insight = _safe_get(insights, "stock", default={})
    if stock_insight:
        lines.append(f"- {_safe_get(stock_insight, 'tip', default='关注明日大盘走势')[:150]}")
    lines.append("")

    lines.append("---")
    lines.append(f"🌙 晚安，{_safe_get(profile, 'name', default='钟锐')}。明天见！")
    lines.append(f"📱 [打开个人网站](https://zr-president.github.io/my-website/)")

    return "\n".join(lines)


def build_test(data, config):
    """Build a test message containing all 4 modes."""
    sections = [
        ("☀️ MORNING", build_morning(data, config)),
        ("🔄 MIDDAY", build_midday(data, config)),
        ("🌅 EVENING", build_evening(data, config)),
        ("🌙 NIGHT", build_night(data, config)),
    ]
    lines = ["# 🧪 Life OS 推送测试", ""]
    for title, content in sections:
        lines.append(f"## {title}")
        lines.append(content)
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# PushPlus sender
# ---------------------------------------------------------------------------

def send_pushplus(token, title, content, topic=""):
    """Send a message via PushPlus API. Returns (success, message)."""
    payload = {
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown",
    }
    if topic:
        payload["topic"] = topic

    try:
        resp = requests.post(PUSHPLUS_API, json=payload, timeout=15)
        data = resp.json()
        if data.get("code") == 200:
            return True, data.get("msg", "OK")
        else:
            return False, f"PushPlus error: {data.get('msg', resp.text)}"
    except Exception as e:
        return False, f"Network error: {e}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

BUILDERS = {
    "morning": ("☀️ 今日启动", build_morning),
    "midday": ("🔄 午间更新", build_midday),
    "evening": ("🌅 晚间推荐", build_evening),
    "night": ("🌙 今日复盘", build_night),
    "test": ("🧪 推送测试", build_test),
}


def main():
    parser = argparse.ArgumentParser(description="Life OS Push Script")
    parser.add_argument("--mode", required=True,
                        choices=["morning", "midday", "evening", "night", "test"],
                        help="Which briefing to generate")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print content to stdout instead of sending")
    parser.add_argument("--token", default="",
                        help="PushPlus token (or set PUSHPLUS_TOKEN env var)")
    parser.add_argument("--topic", default="",
                        help="PushPlus topic ID for group push")
    args = parser.parse_args()

    # --- Load data ---
    print(f"[INFO] Loading data files...", file=sys.stderr)

    data_vars = [
        "DAILY_DATA", "DAILY_BRIEFING", "INSIGHTS", "DAILY_VOCAB",
        "PICKS", "INSIGHTS_TODAY_UPDATED", "DAILY_QUIZ"
    ]
    data = extract_js_vars(DAILY_DATA_PATH, data_vars)

    config_vars = ["PERSONAL_CONFIG"]
    config_raw = extract_js_vars(PERSONAL_CONFIG_PATH, config_vars) or {}
    config = config_raw.get("PERSONAL_CONFIG", {}) or {}

    if not data.get("DAILY_DATA"):
        print("[WARN] DAILY_DATA not found — push content may be sparse", file=sys.stderr)

    # --- Build content ---
    title, builder = BUILDERS[args.mode]
    content = builder(data, config)

    # --- Output ---
    if args.dry_run:
        print("=" * 60)
        print(f"DRY RUN — {title}")
        print("=" * 60)
        print(content)
        print("=" * 60)
        print("[DRY RUN] Message NOT sent.")
        return

    # --- Send ---
    token = args.token or os.environ.get("PUSHPLUS_TOKEN", "")
    if not token:
        print("[ERROR] PushPlus token not provided. Use --token or set PUSHPLUS_TOKEN env var.", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Sending {args.mode} briefing via PushPlus...", file=sys.stderr)
    success, msg = send_pushplus(token, title, content, args.topic)

    if success:
        print(f"[OK] Push sent successfully: {msg}", file=sys.stderr)
    else:
        print(f"[FAIL] Push failed: {msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
