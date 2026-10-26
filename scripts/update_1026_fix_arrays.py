# -*- coding: utf-8 -*-
"""修复：四个数组被多套了一层方括号（`key: [[...]]` → `key: [...]`）

原因：replace_array 里写成 '[' + body + ']'，但 body = json.dumps(list) 本身已带 []。
结果 highlights / words / items(learn) / items(decisions) 各变成「1 个嵌套数组」。
"""
import io, sys, os, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DP = os.path.join(P, 'daily_data.js')
s = open(DP, encoding='utf-8').read()

def array_span(s, key, search_from):
    m = re.compile(r'(["\']?' + key + r'["\']?\s*:\s*)\[').search(s, search_from)
    if not m:
        return None
    open_br = m.end() - 1
    depth = 0; i = open_br; in_str = None
    while i < len(s):
        c = s[i]
        if in_str:
            if c == '\\': i += 2; continue
            if c == in_str: in_str = None
            i += 1; continue
        if c in '"\'':
            in_str = c; i += 1; continue
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return (m.start(1), m.group(1), open_br, i, s[open_br:i+1])
        i += 1
    return None

TARGETS = [
    ('DAILY_BRIEFING', 'highlights', 8),
    ('DAILY_VOCAB', 'words', 10),
    ('DAILY_PATHS_PLACEHOLDER', None, 0),      # 占位，下面单独处理
    ('DAILY_DECISIONS', 'items', 5),
]

# 逐个处理（LEARN_PATHS 单独，因为 items 出现多次）
JOBS = [
    ('highlights', 'var DAILY_BRIEFING', 8),
    ('words', 'var DAILY_VOCAB', 10),
    ('items', 'var LEARN_PATHS', 10),
    ('items', 'var DAILY_DECISIONS', 5),
]

fixed = 0
for key, anchor, expect in JOBS:
    base = s.index(anchor)
    got = array_span(s, key, base)
    if not got:
        print('❌ %s 里找不到 %s' % (anchor, key)); continue
    pstart, prefix, ob, cb, raw = got
    try:
        val = json.loads(raw)
    except Exception as e:
        print('❌ %s/%s 不是合法 JSON：%s' % (anchor, key, e)); continue

    # 拆掉多余的嵌套
    while isinstance(val, list) and len(val) == 1 and isinstance(val[0], list):
        val = val[0]
        fixed += 1

    n = len(val) if isinstance(val, list) else -1
    status = '✅' if n == expect else '⚠️'
    print('  %s %-28s %s = %d（期望 %d）' % (status, anchor.replace('var ', ''), key, n, expect))

    # 重新生成（只包一层括号）
    body = json.dumps(val, ensure_ascii=False, indent=2)
    body = '\n' + '\n'.join('  ' + ln for ln in body.split('\n')) + '\n'
    s = s[:pstart] + prefix + body + s[cb+1:]

open(DP, 'w', encoding='utf-8').write(s)
print()
print('去掉了 %d 层多余括号' % fixed)

r = subprocess.run(['node', '--check', DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('语法：' + ('OK' if r.returncode == 0 else 'FAIL ' + (r.stderr or '')[:400]))

probe = r'''
const fs=require("fs"),vm=require("vm");const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[2],"utf8"),c);
console.log("  要闻:", c.DAILY_BRIEFING.highlights.length, "| 词汇:", c.DAILY_VOCAB.words.length,
  "| 领域:", new Set(c.DAILY_VOCAB.words.map(w=>w.category)).size,
  "| 课堂:", c.LEARN_PATHS.items.length, "| 待办:", c.DAILY_DECISIONS.items.length);
const h=c.DAILY_BRIEFING.highlights[0];
console.log("  首卡:", h ? (h.section+" / "+h.headline.slice(0,24)) : "无");
const w=c.DAILY_VOCAB.words[0];
console.log("  首词:", w ? (w.category+" / "+w.word) : "无");
const it=c.LEARN_PATHS.items[0];
console.log("  首条:", it ? (it.section+" / "+it.title.slice(0,24)) : "无");
'''
pp = os.path.join(P, '_fx.js'); open(pp, 'w', encoding='utf-8').write(probe)
r2 = subprocess.run(['node', pp, DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r2.stdout or r2.stderr)
os.remove(pp)
