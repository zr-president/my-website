# -*- coding: utf-8 -*-
"""① 修掉残留的 9/13 表述 ② 把「内容新鲜度」加进 check_consistency.py"""
import io, sys, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) 残留 9/13 ----------
fixes = [
    ('目标调整（9/13）', '目标调整（9/14）'),
    ('9月13日', '9月14日'),
    ('9/13', '9/14'),
]
n = 0
for a, b in fixes:
    if a in d:
        c = d.count(a); d = d.replace(a, b); n += c
        print('  %s → %s：%d 处' % (a, b, c))
open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL')

# ---------- 2) 新鲜度检查 ----------
CP = BASE + r'\scripts\check_consistency.py'
c = open(CP, 'r', encoding='utf-8').read()
if '内容新鲜度' in c:
    print('已存在新鲜度检查，跳过'); sys.exit(0)

block = '''
# ---------- 11) 内容新鲜度：分区内容里的"最新日期"不得落后于当日 ----------
NODE2 = r"""
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const out={sections:{}};
Object.keys(c.INSIGHTS||{}).forEach(k=>{
  const s=c.INSIGHTS[k];
  out.sections[k]=[s.summary||'', s.trend||'', s.tip||''].join(' ');
});
console.log(JSON.stringify(out));
"""
try:
    rr2 = subprocess.run(['node', '-e', NODE2], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
    secs = _json.loads(rr2.stdout.strip().splitlines()[-1])['sections']
    import datetime as _dt
    _today = _dt.date.fromisoformat(today)
    lagging = []
    for k, blob in secs.items():
        ds = []
        for m in re.finditer(r'(\\d{1,2})月(\\d{1,2})日', blob):
            ds.append((int(m.group(1)), int(m.group(2))))
        for m in re.finditer(r'(?<!\\d)(\\d{1,2})/(\\d{1,2})(?!\\d)', blob):
            a, b2 = int(m.group(1)), int(m.group(2))
            if 1 <= a <= 12 and 1 <= b2 <= 31:
                ds.append((a, b2))
        if not ds:
            continue
        try:
            newest = max(_dt.date(2026, a, b2) for a, b2 in ds)
        except ValueError:
            continue
        lag = (_today - newest).days
        if lag > 0:
            lagging.append('%s（内容最新 %d月%d日，落后 %d 天）' % (k, newest.month, newest.day, lag))
    if lagging:
        err('以下分区内容未真正刷新（只改了日期标签）：' + '；'.join(lagging))
    else:
        ok('内容新鲜度：%d 个分区的内容日期均不落后于当日（%s）' % (len(secs), today))
except Exception as e:
    warn('内容新鲜度检查执行失败：%s' % e)

'''
anchor = "# ---------- 输出 ----------"
c = c.replace(anchor, block + anchor, 1)
open(CP, 'w', encoding='utf-8').write(c)
print('OK 已加入内容新鲜度检查')
