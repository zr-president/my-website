# -*- coding: utf-8 -*-
"""给 ai-track.trend 追加 10/20 的模型竞争观察（修成文件形式避免转义问题）"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

ADD = ('<br><br><b>10月20日（周二）补充：竞争焦点已经换成「单任务成本」</b><br>'
  '10 月的几次更新有一条共同主线——厂商不再只报跑分，而是直接给出【完成一个任务花多少钱】：<br>'
  '① <b>Claude Sonnet 5.5（9/30）</b>Terminal-Bench 4.0 达 70.6%，<b>高于旗舰 Opus 5.5 的 66.4%</b>，'
  '价格只有一半（$2/$10）——「中杯打大杯」第一次在代码任务上成立。<br>'
  '② <b>Claude Opus 5.5（9/22）</b>输出 token 是 GPT-6 Astra 的 4 倍多（约 119k vs 27k），'
  '但单任务成本持平，同时降价 20%。<br>'
  '③ <b>Gemini 4 Argon（10/13）</b>发布即 API 五折，官方刻意不谈参数量。<br>'
  '<b>对你的影响</b>：日常主力仍是 DeepSeek V4.1-Flash-1017（综合 91、闲时再减半），'
  '但【性价比 Coding】这一格已被 Sonnet 5.5 拿走——以后要写更复杂的代码任务，它值得进候选。<br>'
  '<b>判断方法</b>：算三样——完成任务需要多少 token、单价、重试次数。只看单价会被误导。')

i_ins = d.find('var INSIGHTS = {')
i_end = i_ins + re.search(r'\n\};', d[i_ins:]).end()
seg = d[i_ins:i_end]

pat = re.compile(r'((?:"ai-track"|ai-track)\s*:\s*\{)([\s\S]*?)(\n  \})')
m = pat.search(seg)
if not m:
    print('❌ 未找到 ai-track 段'); raise SystemExit(1)
body = m.group(2)

tm = re.search(r'("?trend"?\s*:\s*)(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', body)
if not tm:
    print('❌ 未找到 trend 字段'); raise SystemExit(1)

raw = tm.group(0)
colon = raw.index(':', 1)
val = raw[colon + 1:].strip()
print('原 trend 引号类型: %s，长度 %d' % (val[0], len(val)))

inner = val[1:-1]
# 还原 JS 转义（只处理常见几种）
inner_py = (inner.replace('\\\\', '\\')
                 .replace('\\"', '"')
                 .replace("\\'", "'")
                 .replace('\\n', '\n'))

new_val = json.dumps(inner_py + ADD, ensure_ascii=False)
nb = body[:tm.start()] + tm.group(1) + new_val + body[tm.end():]
seg = seg[:m.start()] + m.group(1) + nb + m.group(3) + seg[m.end():]
d = d[:i_ins] + seg + d[i_end:]

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:300])

v = subprocess.run(['node', '-e', r"""
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const t=c.INSIGHTS['ai-track'].trend;
console.log('新 trend 长度:', t.length);
console.log('含 10月20日:', t.includes('10月20日'));
console.log('含 单任务成本:', t.includes('单任务成本'));
console.log('含 REA vs Jev:', t.includes('REA vs Jev'));
"""], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(v.stdout or v.stderr[:300])
