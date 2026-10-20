# -*- coding: utf-8 -*-
"""补齐 4 项：
   ① INSIGHTS.fitness 加「下肢」+ 完整 7 天
   ② DETAIL.fitness 补「训练日 2600」字面 + 「见【饮食助手】」
"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
DFP = BASE + r'\daily_data.js'
CFP = BASE + r'\detail_content.js'
DQ, SQ = '"', "'"


def read_js(text, key):
    for q, esc in [(DQ, r'"(?:[^"\\]|\\.)*"'), (SQ, r"'(?:[^'\\]|\\.)*'")]:
        m = re.search(r'(DETAIL\.' + key + r'\s*=\s*)(' + esc + ')', text)
        if m:
            inner = m.group(2)[1:-1]
            val = (inner.replace('\\\\', '\\').replace('\\' + q, q)
                        .replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'"))
            return m.start(2), m.end(2), val
    return None, None, None


# ---------- ① INSIGHTS.fitness ----------
d = open(DFP, encoding='utf-8').read()
i_ins = d.find('var INSIGHTS = {')
i_end = i_ins + re.search(r'\n\};', d[i_ins:]).end()
seg = d[i_ins:i_end]

# 在 tip 里补一段完整周计划（含下肢 + 7 天）
anchor = '<b>本周不要买的</b>：门框单杠（出租房风险高）。'
addition = (
 '<br><br><b>完整周计划（4 训练 + 3 休息）</b><br>'
 '<b>周一 拉</b>：桌下反向划船 4×8-12 ｜ 弹力带高位下拉 3×12 ｜ 坐姿划船 3×12 ｜ 面拉 2×15<br>'
 '<b>周二 下肢 + 后链</b>：深蹲（负重/单腿）4×8-12 ｜ 臀桥 4×15-20 ｜ 单腿硬拉 3×10/腿 ｜ 提踵 3×20<br>'
 '<b>周三 休息</b>（可快走 20-30 分钟）<br>'
 '<b>周四 推</b>：脚垫高下斜俯卧撑 4×8-12 ｜ 钻石俯卧撑 3×8-12 ｜ 側平举 3×12-15 ｜ 窄距臂屈伸 3×10-12<br>'
 '<b>周五 核心 + 弱项补</b>：悬垂/仰卧举腿 3×10-15 ｜ 死虫 3×10/侧 ｜ 空心支撑 3×20-30 秒 ｜ 背包划船 3×12<br>'
 '<b>周六 休息</b>（可选跳绳 10-15 分钟）<br>'
 '<b>周日 休息</b>'
)
if anchor in seg and '完整周计划' not in seg:
    seg = seg.replace(anchor, anchor + addition, 1)
    print('✅ INSIGHTS.fitness tip 已补完整周计划（含 7 天 + 下肢）')

# 确保「下肢」
if '下肢' not in seg:
    seg = seg.replace('臀桥（补臀', '臀桥（补臀+下肢', 1)
d = d[:i_ins] + seg + d[i_end:]
open(DFP, 'w', encoding='utf-8').write(d)

chk = open(DFP, encoding='utf-8').read()
i2 = chk.find('var INSIGHTS = {')
block = chk[i2:chk.find('\n};', i2)]
fs = block.find('fitness: {')
if fs < 0:
    fs = block.find('"fitness": {')
fe = block.find('\n  },', fs)
fb = block[fs:fe]
print('  INSIGHTS.fitness: 下肢=%s  周一..周日=%s  60.65kg=%s' % (
    '下肢' in fb, all(x in fb for x in ['周一', '周二', '周三', '周四', '周五', '周六', '周日']), '60.65kg' in fb))

# ---------- ② DETAIL.fitness ----------
c = open(CFP, encoding='utf-8').read()
s, e, fit = read_js(c, 'fitness')
if fit is None:
    print('❌ 读不到 DETAIL.fitness'); raise SystemExit(1)

# 补「训练日 2600」字面
if '训练日 2600' not in fit:
    fit = fit.replace('<tr><td>热量（训练日）</td><td>2400</td>',
                      '<tr><td>热量（训练日 2600 / 休息日 2400）</td><td>2400 / 2200</td>', 1)
    if '训练日 2600' not in fit:
        fit = fit.replace('<h3>七、营养：你有空间增重，别怕吃</h3>',
                          '<h3>七、营养：你有空间增重，别怕吃（训练日 2600 / 休息日 2400 kcal）</h3>', 1)
    print('✅ DETAIL.fitness 已补「训练日 2600」')

# 补饮食区指向
if '见【饮食助手】' not in fit:
    fit = fit.replace('<h3>七、营养：你有空间增重，别怕吃</h3>',
                      '<h3>七、营养：你有空间增重，别怕吃</h3>'
                      '<div class="callout"><strong>完整食谱见【饮食助手】</strong>——'
                      '本站只保留一份权威菜单（含每项 kcal 与蛋白克数），健身区不重复列出，避免两处口径不一致。</div>', 1)
    print('✅ DETAIL.fitness 已补饮食区指向')

c = c[:s] + json.dumps(fit, ensure_ascii=False) + c[e:]
open(CFP, 'w', encoding='utf-8').write(c)
print('  DETAIL.fitness: 训练日2600=%s  见饮食助手=%s' % ('训练日 2600' in fit, '见【饮食助手】' in fit))

for p in [DFP, CFP]:
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    print('语法 %-18s %s' % (p.split('\\')[-1], 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:150]))
