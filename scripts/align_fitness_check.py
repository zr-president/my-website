# -*- coding: utf-8 -*-
"""对齐：① DETAIL.fitness 补「下肢」「见【饮食助手】」 ② check_consistency 常量更新到新计划"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
CFP = BASE + r'\detail_content.js'
CHK = BASE + r'\scripts\check_consistency.py'

# ---------- ① DETAIL.fitness 补内容 ----------
c = open(CFP, 'r', encoding='utf-8').read()
m = re.search(r"(DETAIL\.fitness\s*=\s*)(\"(?:[^\"\\]|\\.)*\")", c)
v = json.loads(m.group(2))
before = len(v)

# 加「下肢」表述
v = v.replace('<b>腿 + 核心</b>：深蹲 4×15-20', '<b>下肢（腿）+ 核心</b>：深蹲 4×15-20')
v = v.replace('<td><b>周三</b></td><td><b>腿 + 核心</b>', '<td><b>周三</b></td><td><b>下肢（腿）+ 核心</b>')
v = v.replace('臀桥 3×20</td><td>臀桥和死虫是改善骨盆前倾的关键',
              '臀桥 3×20</td><td>臀桥和死虫是改善骨盆前倾的关键；下肢训练别跳过')

# 加饮食区指向（单一权威食谱原则）
if '见【饮食助手】' not in v:
    v = v.replace('<h3>七、营养微调（按 60.65kg 重算）</h3>',
                  '<h3>七、营养微调（按 60.65kg 重算）</h3>'
                  '<div class="callout"><strong>完整食谱见【饮食助手】</strong>——'
                  '本站只保留一份权威菜单（含每项 kcal 与蛋白克数），健身区不重复列出，避免两处口径不一致。</div>')

c = c[:m.start(2)] + json.dumps(v, ensure_ascii=False) + c[m.end(2):]
open(CFP, 'w', encoding='utf-8').write(c)
print('✅ DETAIL.fitness：%d → %d 字' % (before, len(v)))
print('   含「下肢」:', '下肢' in v, '| 含「见【饮食助手】」:', '见【饮食助手】' in v)

# ---------- ② check_consistency 常量更新 ----------
k = open(CHK, 'r', encoding='utf-8').read()
subs = [
 # 热量口径
 ("CAL = '训练日 2500'", "CAL = '训练日 2400'"),
 ("if CAL in txt or '训练日 2500' in txt:", "if CAL in txt or '训练日 2400' in txt:"),
 ("ok(name + ' 含热量口径「训练日 2500」')", "ok(name + ' 含热量口径「训练日 2400」')"),
 ("err(name + ' 缺热量口径「训练日 2500」')", "err(name + ' 缺热量口径「训练日 2400」')"),
 ("if '训练日 2500' in fitness or '训练日 2500' in ins_fit or '训练日 +200' in fitness or '训练日+200' in fitness or '训练日 2500' in fitness:",
  "if '训练日 2400' in fitness or '训练日 2400' in ins_fit or '训练日 +200' in fitness or '训练日+200' in fitness:"),
 ("ok('健身侧含热量口径（训练日 2500 / +200）')", "ok('健身侧含热量口径（训练日 2400 / +200）')"),
 ("warn('健身侧未明确出现「训练日 2500」')", "warn('健身侧未明确出现「训练日 2400」')"),
 ("if '休息日 2300' in diet and ('休息日 2300' in ins_diet or '休息日 2300' in ins_diet):",
  "if '休息日 2200' in diet and '休息日 2200' in ins_diet:"),
 ("ok('休息日 2300 口径一致')", "ok('休息日 2200 口径一致')"),
 ("warn('休息日 2300 口径未在两处同时出现')", "warn('休息日 2200 口径未在两处同时出现')"),
 # 蛋白口径
 ("if '110-130g' in diet:", "if '125-135g' in diet:"),
 ("ok('DETAIL.diet 含蛋白口径 110-130g')", "ok('DETAIL.diet 含蛋白口径 125-135g')"),
 ("err('DETAIL.diet 缺蛋白口径 110-130g')", "err('DETAIL.diet 缺蛋白口径 125-135g')"),
 ("if '110-130g' in ins_diet:", "if '125-135g' in ins_diet:"),
 ("ok('INSIGHTS.diet 含蛋白口径 110-130g')", "ok('INSIGHTS.diet 含蛋白口径 125-135g')"),
 ("err('INSIGHTS.diet 缺蛋白口径 110-130g')", "err('INSIGHTS.diet 缺蛋白口径 125-135g')"),
 # 体重
 ("if '59kg' not in txt and '59 kg' not in txt:", "if '60.65kg' not in txt and '60.65 kg' not in txt:"),
 ("warn(name + ' 未出现体重 59kg')", "warn(name + ' 未出现体重 60.65kg')"),
 ("ok('体型数据 170cm/59kg 一致')", "ok('体型数据 170cm/60.65kg 一致')"),
]
n = 0
for a, b in subs:
    if a in k:
        k = k.replace(a, b); n += 1
print('✅ 检查脚本常量替换：%d 处' % n)

# 周计划表：兼容 data-table 形式
old_wk = ('wk = re.search(r\'<div class="wk-plan">(.*?)</div>\\s*<div class="wk-legend"\', fitness, re.S)\n'
          'if wk:')
new_wk = ('wk = re.search(r\'<div class="wk-plan">(.*?)</div>\\s*<div class="wk-legend"\', fitness, re.S)\n'
          'if not wk:\n'
          '    # 备用：data-table 形式的周计划（新版结构）\n'
          '    wk = re.search(r\'新周计划.*?(</table>)\', fitness, re.S)\n'
          'if wk:')
if old_wk in k:
    k = k.replace(old_wk, new_wk); print('✅ 周计划表检查已兼容 data-table')

open(CHK, 'w', encoding='utf-8').write(k)
r = subprocess.run(['node', '--check', CFP], capture_output=True, text=True)
print('detail 语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
