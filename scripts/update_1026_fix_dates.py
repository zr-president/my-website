# -*- coding: utf-8 -*-
"""补修两处：
1) 带引号的 "updated": "2026-10-25" 没被同步（正则漏了键带引号的情况）
2) WEBSITE_GUIDE.summary 里的「版本1.8.38」没升
"""
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DP = os.path.join(P, 'daily_data.js')
TODAY = '2026-10-26'

s = open(DP, encoding='utf-8').read()

# ---------- 1) updated 字段：兼容 `updated:` 与 `"updated":` 与 `'updated':` ----------
pat = re.compile(r'((["\']?)updated\2\s*:\s*)(["\'])(2026-\d\d-\d\d)\3')
s2, n = pat.subn(lambda m: m.group(1) + m.group(3) + TODAY + m.group(3), s)
print('updated 字段同步：%d 处（含带引号键）' % n)

# ---------- 2) WEBSITE_GUIDE 版本 ----------
m = re.search(r'版本1\.8\.(\d+)', s2)
if m:
    old = m.group(0)
    s2 = s2.replace(old, '版本1.8.41', 1)
    print('WEBSITE_GUIDE 版本：%s → 版本1.8.41' % old)
else:
    print('⚠️ 未找到「版本1.8.x」写法')

open(DP, 'w', encoding='utf-8').write(s2)

# ---------- 3) 校验 ----------
r = subprocess.run(['node', '--check', DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('语法：' + ('OK' if r.returncode == 0 else 'FAIL ' + (r.stderr or '')[:300]))

probe = r'''
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),c);
const bad=Object.keys(c.INSIGHTS).filter(k=>c.INSIGHTS[k].updated!=='2026-10-26');
console.log('  INSIGHTS 仍非今日: '+(bad.length?bad.join(','):'无 ✅'));
const others=[];
if(c.LEARN_PATHS.updated!=='2026-10-26') others.push('LEARN_PATHS');
if(c.DAILY_DECISIONS.updated!=='2026-10-26') others.push('DAILY_DECISIONS');
if(c.AI_MODEL_COMPARISON.updated!=='2026-10-26') others.push('AI_MODEL_COMPARISON');
if(c.DAILY_DATA.movie && c.DAILY_DATA.movie.updated!=='2026-10-26') others.push('DAILY_DATA.movie');
console.log('  其他 updated 非今日: '+(others.length?others.join(','):'无 ✅'));
console.log('  版本: '+c.SITE_VERSION);
console.log('  GUIDE 含 1.8.41: '+((c.WEBSITE_GUIDE||{}).summary||'').includes('1.8.41'));
console.log('  archive 组数: '+Object.keys(c.LEARN_PATHS.archive).length+'（最新 '+Object.keys(c.LEARN_PATHS.archive)[0]+'）');
'''
pp = os.path.join(P, '_f.js'); open(pp, 'w', encoding='utf-8').write(probe)
r2 = subprocess.run(['node', pp, DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r2.stdout or r2.stderr)
os.remove(pp)
