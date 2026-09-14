# -*- coding: utf-8 -*-
"""内容新旧审计：区分「日期标签已更新」与「内容确实刷新」
   启发式：抽取每段内容里的日期/时态词，判断它描述的是不是"今天"
"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

NODE = r"""
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const out={today:c.DAILY_BRIEFING.date, sections:{}};
Object.keys(c.INSIGHTS||{}).forEach(k=>{
  const s=c.INSIGHTS[k];
  out.sections[k]={updated:s.updated, summary:s.summary||'', trend:s.trend||'', tip:s.tip||''};
});
out.decisions=(c.DAILY_DECISIONS.items||[]).map(x=>x.action);
out.briefing=(c.DAILY_BRIEFING.highlights||[]).map(x=>({s:x.section,h:x.headline,m:x.summary}));
console.log(JSON.stringify(out));
"""
r = subprocess.run(['node', '-e', NODE], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
data = json.loads(r.stdout.strip().splitlines()[-1])
TODAY = data['today']
print('系统/站点日期：%s' % TODAY)
print()

# 日期模式
PAT_MD = re.compile(r'(\d{1,2})月(\d{1,2})日')
PAT_SLASH = re.compile(r'(?<!\d)(\d{1,2})/(\d{1,2})(?!\d)')
VAGUE = ['9月初', '9月中', '本周', '上周', '月初', '近日']

def dates_in(txt):
    """抽出内容里出现的所有月-日，返回 [(月,日,原文)]"""
    found = []
    for m in PAT_MD.finditer(txt):
        found.append((int(m.group(1)), int(m.group(2)), m.group(0)))
    for m in PAT_SLASH.finditer(txt):
        mo, dy = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12 and 1 <= dy <= 31:
            found.append((mo, dy, m.group(0)))
    return found

today_dt = datetime.date.fromisoformat(TODAY)

print('=== 逐分区：内容里出现的最新日期 vs 今天 ===')
stale_sections = []
for k, s in data['sections'].items():
    blob = s['summary'] + ' ' + s['trend'] + ' ' + s['tip']
    ds = dates_in(blob)
    valid = [(mo, dy) for mo, dy, _ in ds if 1 <= mo <= 12]
    if valid:
        newest = max(valid, key=lambda x: datetime.date(2026, x[0], x[1]))
        newest_dt = datetime.date(2026, newest[0], newest[1])
        lag = (today_dt - newest_dt).days
        mark = '✅' if lag <= 0 else ('⚠️' if lag <= 2 else '❌')
        if lag > 0:
            stale_sections.append((k, '%d月%d日' % newest, lag))
        print('  %s %-11s 最新内容日期 %-8s 落后 %d 天  (updated=%s)' % (mark, k, '%d月%d日' % newest, lag, s['updated']))
    else:
        has_vague = [v for v in VAGUE if v in blob]
        print('  ❓ %-11s 无明确日期%s  (updated=%s)' % (k, ('，用词：' + '/'.join(has_vague)) if has_vague else '', s['updated']))

print()
print('=== 结论：日期标签已更新，但内容日期仍滞后的分区 ===')
if stale_sections:
    for k, d, lag in stale_sections:
        print('  ❌ %s：内容最新只到 %s（落后 %d 天）' % (k, d, lag))
else:
    print('  无')

print()
print('=== 今日常规内容（要闻/待办）是否含过期表述 ===')
for i, b in enumerate(data['briefing'], 1):
    ds = dates_in(b['m'])
    old = [(mo, dy) for mo, dy, _ in ds if datetime.date(2026, mo, dy) < today_dt and (today_dt - datetime.date(2026, mo, dy)).days > 3]
    if old:
        print('  要闻%d [%s] 提到较早日期：%s' % (i, b['s'], ['%d/%d' % o for o in old][:4]))
for i, a in enumerate(data['decisions'], 1):
    if '明天' in a or '昨天' in a or '周末' in a:
        print('  待办%d 含相对时间词：%s' % (i, a[:44]))
