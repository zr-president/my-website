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

import sys, os, re, json, argparse, subprocess, textwrap, io, requests
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
    """Build 08:00 morning briefing — concise mobile-friendly version."""
    daily = data.get("DAILY_DATA", {})
    insights = data.get("INSIGHTS", {})
    vocab = data.get("DAILY_VOCAB", {})
    profile = config.get("profile", {})
    today = datetime.now().strftime("%m/%d")
    weekday = ["周一","周二","周三","周四","周五","周六","周日"][datetime.now().weekday()]

    # Extract weather (first ~30 chars)
    weather = _safe_get(daily, "weather_summary", default="")
    weather_short = weather[:60] if weather else ""

    lines = [
        f"☀️ 早！{today} {weekday} | {_safe_get(profile, 'city', default='广州')} {weather_short}",
        "",
    ]

    # Stock — single line key data
    market = _safe_get(daily, "market_summary", default="")
    if market:
        # Extract just the first sentence (before first |)
        mkt_short = market.split("｜")[0][:80] if "｜" in market else market[:80]
        lines.append(f"📈 **股市**")
        lines.append(f"{mkt_short}")
        # Add insight trend if available
        stock_insight = _safe_get(insights, "stock", default={})
        stock_trend = _safe_get(stock_insight, "trend", default="")
        if stock_trend:
            lines.append(f"{stock_trend[:100]}")
        lines.append("")

    # AI Toolchain Radar — 用户最关心的工具链动态（Claude Code + DeepSeek + Harness）
    radar = data.get("TOOLCHAIN_RADAR", {})
    radar_items = radar.get("items", []) if isinstance(radar, dict) else []
    if radar_items:
        lines.append("🔧 **AI工具链雷达**")
        lines.append(f"🎯 {_safe_get(radar, 'headline', default='')[:80]}")
        for it in radar_items[:3]:
            if isinstance(it, dict):
                topic = _pick(it, 'topic')[:28]
                impact = _pick(it, 'impact')[:70]
                lines.append(f"· **{topic}** — {impact}")
        lines.append("")

    # AI News — top headlines, first one gets 🌟
    headlines = _safe_get(daily, "news_headlines", default=[])
    if headlines and len(headlines) > 0:
        lines.append("🤖 **AI快讯**")
        for i, h in enumerate(headlines[:3]):
            if isinstance(h, dict):
                title = _pick(h, 'title')
                title_short = title[:65] + "…" if len(title) > 65 else title
                prefix = "🌟 " if i == 0 else "· "
                lines.append(f"{prefix}{title_short}")
        lines.append("")

    # Job — compact
    job_cfg = config.get("job", {})
    if job_cfg:
        lines.append(f"💼 **求职** | 周目标{_safe_get(job_cfg, 'weekly_target', default='15')}份 | 黄金窗口9:30-11:00")
        lines.append("")

    # Daily Vocab — one-liner
    words = _safe_get(vocab, "words", default=[])
    if words and len(words) > 0:
        w = words[0] if isinstance(words[0], dict) else {}
        lines.append(f"💡 **{_pick(w, 'word')}** {_pick(w, 'emoji')}：{_pick(w, 'definition')[:80]}")
        lines.append("")

    lines.append("─" * 20)
    lines.append("📱 zr-president.github.io/my-website | ⏰12:00午间")

    return "\n".join(lines)


def build_midday(data, config):
    """Build 12:00 midday check-in — concise mobile-friendly version."""
    daily = data.get("DAILY_DATA", {})
    insights = data.get("INSIGHTS", {})
    profile = config.get("profile", {})
    dietary = _safe_get(profile, "dietary", default=[])
    today = datetime.now().strftime("%m/%d")
    weekday = ["周一","周二","周三","周四","周五","周六","周日"][datetime.now().weekday()]

    lines = [
        f"🔄 午间 | {today} {weekday}",
        "",
    ]

    # AI — trend only, short
    ai_insight = _safe_get(insights, "ai-track", default={})
    if ai_insight:
        trend = _safe_get(ai_insight, "trend", default="")
        if trend:
            lines.append(f"🤖 **AI**")
            lines.append(f"{trend[:150]}")
            lines.append("")

    # Diet — compact
    if dietary:
        notes = "、".join(dietary) if isinstance(dietary, list) else str(dietary)
        lines.append(f"🍽️ **饮食** | ⚠️{notes}")
        lines.append("🥗 高蛋白+蔬菜 | 💧 下午再喝1L水 | 🚶 饭后走动10分钟")
        lines.append("")

    # Stock — one line
    market = _safe_get(daily, "market_summary", default="")
    if market:
        mkt_short = market.split("｜")[0][:80] if "｜" in market else market[:80]
        lines.append(f"📈 **大盘** | {mkt_short}")
        lines.append("")

    lines.append("─" * 20)
    lines.append("📱 zr-president.github.io/my-website | ⏰18:00晚间")

    return "\n".join(lines)


def build_evening(data, config):
    """Build 18:00 evening picks — concise mobile-friendly version."""
    daily = data.get("DAILY_DATA", {})
    picks = data.get("PICKS", {})
    insights = data.get("INSIGHTS", {})
    profile = config.get("profile", {})
    today = datetime.now().strftime("%m/%d")
    weekday = ["周一","周二","周三","周四","周五","周六","周日"][datetime.now().weekday()]

    lines = [
        f"🌅 晚间 | {today} {weekday}",
        "",
    ]

    # Fitness — one-liner
    fitness = _safe_get(insights, "fitness", default={})
    if fitness:
        tip_short = _safe_get(fitness, "tip", default="")[:80]
        lines.append(f"🏋️ **健身** | 第{_safe_get(profile, 'fitness_week', default='?')}周·{_safe_get(profile, 'fitness_goal', default='增肌')}")
        if tip_short:
            lines.append(f"{tip_short}")
        lines.append("")

    # Picks — one line each
    lines.append("🎬 **推荐**")

    anime_picks = _safe_get(picks, "anime", default=[])
    if anime_picks and len(anime_picks) > 0:
        a = anime_picks[0] if isinstance(anime_picks[0], dict) else {}
        lines.append(f"📺 {_pick(a, 'title')} — {_pick(a, 'desc')[:60]}")

    movie = _safe_get(insights, "movie", default={})
    if movie:
        movie_short = _safe_get(movie, "summary", default="")[:80]
        if movie_short:
            lines.append(f"🎥 {movie_short}")

    music_rec = _safe_get(daily, "daily_recommendation", "music", default={})
    if isinstance(music_rec, dict):
        lines.append(f"🎵 {_pick(music_rec, 'title')} — {_pick(music_rec, 'desc')[:60]}")

    lines.append("")

    # Learning — one-liner
    learning = _safe_get(insights, "learning", default={})
    if learning:
        learn_tip = _safe_get(learning, "tip", default="")[:100]
        if learn_tip:
            lines.append(f"📚 **学习** | {learn_tip}")
            lines.append("")

    # Toolchain action suggestion — 晚间提醒：工具链决策
    radar = data.get("TOOLCHAIN_RADAR", {})
    radar_items = radar.get("items", []) if isinstance(radar, dict) else []
    if radar_items:
        lines.append("🔧 **工具链决策**")
        for it in radar_items[:2]:
            if isinstance(it, dict):
                topic = _pick(it, 'topic')[:24]
                action = _pick(it, 'action')[:80]
                lines.append(f"· **{topic}** → {action}")
        lines.append("")

    lines.append("─" * 20)
    lines.append("📱 zr-president.github.io/my-website | ⏰22:00复盘")

    return "\n".join(lines)


def build_night(data, config):
    """Build 22:00 night review — concise mobile-friendly version."""
    daily = data.get("DAILY_DATA", {})
    insights = data.get("INSIGHTS", {})
    today_updated = data.get("INSIGHTS_TODAY_UPDATED", [])
    profile = config.get("profile", {})
    today = datetime.now().strftime("%m/%d")
    weekday = ["周一","周二","周三","周四","周五","周六","周日"][datetime.now().weekday()]

    lines = [
        f"🌙 晚安 | {today} {weekday}",
        "",
    ]

    # Today's summary — weekly_focus first 150 chars
    weekly = _safe_get(daily, "weekly_focus", default="")
    if weekly:
        lines.append(f"📊 **今日要点**")
        lines.append(f"{weekly[:150]}")
        lines.append("")

    # INSIGHTS updated
    if today_updated and len(today_updated) > 0:
        lines.append(f"📖 **今日更新** | {', '.join(today_updated[:7])}")
        lines.append("")

    # Career — one-liner
    career = _safe_get(insights, "career", default={})
    if career:
        career_tip = _safe_get(career, "tip", default="")
        if career_tip:
            lines.append(f"💼 **求职** | {career_tip[:120]}")
            lines.append("")

    # Reflection
    lines.append("📝 **反思**")
    lines.append("今天投递进度？健身完成了吗？明天影之刃零预售闹钟？")
    lines.append("")

    # Tomorrow
    lines.append("🔮 **明天**")
    stock_tip = _safe_get(insights, "stock", "tip", default="")
    if stock_tip:
        lines.append(f"· {stock_tip[:120]}")
    news_trend = _safe_get(insights, "news", "trend", default="")
    if news_trend:
        lines.append(f"· {news_trend[:120]}")
    lines.append("")

    lines.append("─" * 20)
    lines.append(f"🌙 晚安{_safe_get(profile, 'name', default='钟锐')}，明天见")
    lines.append("📱 zr-president.github.io/my-website")

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
        "PICKS", "INSIGHTS_TODAY_UPDATED", "DAILY_QUIZ", "TOOLCHAIN_RADAR"
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

    # Mask token for logging
    masked = token[:8] + "***" + token[-4:] if len(token) > 12 else "***"
    print(f"[INFO] Using token: {masked}", file=sys.stderr)
    print(f"[INFO] Content length: {len(content)} chars", file=sys.stderr)
    print(f"[INFO] Sending {args.mode} briefing via PushPlus...", file=sys.stderr)
    success, msg = send_pushplus(token, title, content, args.topic)

    if success:
        print(f"[OK] Push sent successfully: {msg}", file=sys.stderr)
    else:
        print(f"[FAIL] Push failed: {msg}", file=sys.stderr)
        # Print first 200 chars of content for debugging
        print(f"[DEBUG] Content preview: {content[:200]}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
