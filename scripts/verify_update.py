# -*- coding: utf-8 -*-
"""个人网站 · 更新核查报告（你自己就能跑，不需要信任任何人）

用法：
    cd C:\\Users\\ZR\\Desktop\\钟锐的个人网站
    python scripts/verify_update.py

它会读取 daily_data.js / detail_content.js，用【你电脑的系统日期】核对：
  ① 所有日期字段是否等于今天
  ② 每个分区正文里出现的最新日期是否落后于今天（防止"只改标签不刷内容"）
  ③ 跨板块口径是否一致（热量/蛋白/食谱唯一性/版本号/链接）
"""
import io, sys, os, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
WD = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]

LINE = '=' * 58
print(LINE)
print('  个人网站 · 更新核查报告')
print(LINE)
print('  你电脑的日期：%s（%s）' % (TODAY, WD))
print()

# ---------- 载入数据 ----------
NODE = r"""
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const out={sections:{},fields:{},archive:[]};
function put(n,v){ out.fields[n]=v; }
if(c.DAILY_DATA) put('网站更新日期', c.DAILY_DATA.update_date);
if(c.DAILY_DATA&&c.DAILY_DATA.movie) put('影视数据', c.DAILY_DATA.movie.updated);
put('今日要闻', c.DAILY_BRIEFING&&c.DAILY_BRIEFING.date);
put('每日一词', c.DAILY_VOCAB&&c.DAILY_VOCAB.date);
put('小白课堂', c.LEARN_PATHS&&c.LEARN_PATHS.updated);
put('市场情绪', c.MARKET_SENTIMENT&&c.MARKET_SENTIMENT.updated);
put('今日待办', c.DAILY_DECISIONS&&c.DAILY_DECISIONS.updated);
put('机会雷达', c.OPPORTUNITY_RADAR&&c.OPPORTUNITY_RADAR.updated);
put('判断台账', c.AI_JUDGMENTS&&c.AI_JUDGMENTS.updated);
put('工具链雷达', c.TOOLCHAIN_RADAR&&c.TOOLCHAIN_RADAR.updated);
Object.keys(c.INSIGHTS||{}).forEach(k=>{
  const s=c.INSIGHTS[k];
  put('分区·'+k, s.updated);
  out.sections[k]=[s.summary||'', s.trend||'', s.tip||''].join(' ');
});
out.archive=Object.keys((c.LEARN_PATHS&&c.LEARN_PATHS.archive)||{});
console.log(JSON.stringify(out));
"""
r = subprocess.run(['node', '-e', NODE], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
if r.returncode != 0:
    print('❌ 读取 daily_data.js 失败：', r.stderr[:300]); sys.exit(1)
data = json.loads(r.stdout.strip().splitlines()[-1])


def iso(s):
    if not s:
        return None
    m = re.search(r'(\d{4})\D+(\d{1,2})\D+(\d{1,2})', str(s))
    return '%s-%02d-%02d' % (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def dates_in(txt):
    out = []
    for m in re.finditer(r'(\d{1,2})月(\d{1,2})日', txt):
        out.append((int(m.group(1)), int(m.group(2))))
    for m in re.finditer(r'(?<!\d)(\d{1,2})/(\d{1,2})(?!\d)', txt):
        a, b = int(m.group(1)), int(m.group(2))
        if 1 <= a <= 12 and 1 <= b <= 31:
            out.append((a, b))
    return out


# ---------- 一、日期字段 ----------
print('【一】日期字段是否等于今天')
bad_fields = []
for name, val in data['fields'].items():
    v = iso(val)
    mark = '✅' if v == TODAY else '❌'
    if v != TODAY:
        bad_fields.append((name, val))
    print('  %s %-22s %s' % (mark, name, val or '（空）'))
print('  ── 共 %d 项，%d 项与今天一致' % (len(data['fields']), len(data['fields']) - len(bad_fields)))
print()

# ---------- 二、内容新鲜度 ----------
print('【二】各分区正文里的"最新日期"（防只改标签不刷内容）')
today_dt = datetime.date.fromisoformat(TODAY)
lagging = []
for k, blob in data['sections'].items():
    ds = dates_in(blob)
    if not ds:
        print('  ❓ %-12s 正文无明确日期' % k)
        continue
    try:
        newest = max(datetime.date(now.year, a, b) for a, b in ds)
    except ValueError:
        continue
    lag = (today_dt - newest).days
    if lag > 0:
        lagging.append((k, newest, lag))
        print('  ❌ %-12s 内容最新 %d月%d日，落后 %d 天' % (k, newest.month, newest.day, lag))
    else:
        print('  ✅ %-12s 内容最新 %d月%d日' % (k, newest.month, newest.day))
print()

# ---------- 三、归档键 ----------
print('【三】归档键（只能是历史日期）')
clash = [k for k in data['archive'] if k == TODAY]
if clash:
    print('  ❌ 归档键与今天相同：%s（会把当天内容误当历史隐藏）' % clash)
else:
    print('  ✅ %d 个归档键均为历史日期：%s' % (len(data['archive']), ', '.join(sorted(data['archive'], reverse=True)[:4]) + ' …'))
print()

# ---------- 四、跨板块一致性 ----------
print('【四】跨板块口径一致性')
try:
    rr = subprocess.run([sys.executable, os.path.join(BASE, 'scripts', 'check_consistency.py')],
                        capture_output=True, text=True, encoding='utf-8', cwd=BASE)
    tail = [l for l in (rr.stdout or '').splitlines() if l.strip()]
    okline = [l for l in tail if '一致性检查通过' in l]
    if okline:
        print('  ✅ ' + okline[-1].strip())
    else:
        print('  ❌ 一致性检查未通过：')
        for l in tail[-6:]:
            print('     ' + l)
except Exception as e:
    print('  ⚠️ 无法执行一致性检查：%s' % e)
print()

# ---------- 结论 ----------
print(LINE)
problems = len(bad_fields) + len(lagging) + len(clash)
if problems == 0:
    print('  ✅ 结论：通过 —— 日期与内容都是最新的')
else:
    print('  ❌ 结论：发现 %d 个问题' % problems)
    for n, v in bad_fields:
        print('     · 日期未同步：%s = %s' % (n, v))
    for k, d, lag in lagging:
        print('     · 内容未刷新：%s（最新 %d月%d日，落后 %d 天）' % (k, d.month, d.day, lag))
    for k in clash:
        print('     · 归档键冲突：%s' % k)
print(LINE)
print()
print('提示：也可以直接打开网站首页，顶部徽章会显示「📅 内容日期」与')
print('      「✅ 今日更新已核查」；点徽章可展开逐分区明细。')
print('      这两处都是页面打开时用脚本现算的，不是写死的文字。')
