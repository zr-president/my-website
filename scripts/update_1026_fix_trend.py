# -*- coding: utf-8 -*-
"""补：17 个分区的 trend 字段补上当日日期（10/26）

为什么必须补：skill 要求 summary / trend / tip 三个字段的内容里都要出现当日日期，
audit_freshness.py 会逐字段扫描。第 3 批写完后 trend 普遍缺日期。

做法：把日期插进 trend 首个 <b> 标签内（紧跟 <b>），保证读起来自然，
不额外加一行重复标题。
"""
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _insight_helper import make_patcher

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DP = os.path.join(P, 'daily_data.js')
DATE = '10/26（周一）'
DATE_RE = re.compile(r'10月26日|10/26|10 月 26|10-26')

# 先读出来判断哪些 trend 缺日期
import json
probe = r'''
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),c);
const out={};
Object.keys(c.INSIGHTS).forEach(k=>{ out[k]=c.INSIGHTS[k].trend; });
console.log(JSON.stringify(out));
'''
pp = os.path.join(P, '_tprobe.js')
open(pp, 'w', encoding='utf-8').write(probe)
r = subprocess.run(['node', pp, DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
os.remove(pp)
trends = json.loads(r.stdout)

missing = [k for k, v in trends.items() if not DATE_RE.search(v or '')]
print('缺日期的 trend：%d 个 → %s' % (len(missing), ', '.join(missing)))

if not missing:
    print('无需补')
    raise SystemExit(0)

# 逐条构造：把日期插进首个 <b> 内
C = {}
for k in missing:
    t = trends[k]
    m = re.search(r'<b>', t)
    if m:
        newt = t[:m.end()] + DATE + t[m.end():]
    else:
        newt = '<b>' + DATE + '</b>' + t
    # summary / tip 已经含日期，这里只改 trend → 借用 helper 时必须三字段都给，
    # 所以先取原值原样传回
    C[k] = {'summary': None, 'trend': newt, 'tip': None}

# 补回原 summary / tip（原样不动）
probe2 = r'''
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),c);
const out={};
Object.keys(c.INSIGHTS).forEach(k=>{ out[k]={s:c.INSIGHTS[k].summary,t:c.INSIGHTS[k].tip}; });
console.log(JSON.stringify(out));
'''
pp2 = os.path.join(P, '_sprobe.js')
open(pp2, 'w', encoding='utf-8').write(probe2)
r2 = subprocess.run(['node', pp2, DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
os.remove(pp2)
orig = json.loads(r2.stdout)

for k in missing:
    C[k]['summary'] = orig[k]['s']
    C[k]['tip'] = orig[k]['t']

apply = make_patcher(DP)
n = apply(C)
print('✅ 已补 %d 个字段' % n)

r3 = subprocess.run(['node', '--check', DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('   语法：' + ('OK' if r3.returncode == 0 else 'FAIL ' + (r3.stderr or '')[:300]))
