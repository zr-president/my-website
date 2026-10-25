# -*- coding: utf-8 -*-
"""隐私脱敏：去掉公开内容里的诊断名称，保留功能性建议

原则：
- 删除：诊断名称（肾结石 / 甲状腺结节）
- 保留：实用建议（多喝水、草酸、十字花科要煮熟、按医嘱复查）
- 理由：他在求职，公开站点不应出现健康诊断；但饮食计划的可执行性要保持

同时清理 personal_config.js 里页面从未使用的健康字段（死数据）
"""
import io, sys, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FILES = ['personal_config.js', 'daily_data.js', 'detail_content.js', 'index.html', 'knowledge_index.js', 'knowledge_index.json']

REPL = [
 # ── personal_config.js：删死字段 ──
 ('        height_cm: 170,\n        weight_kg: 59,\n        dietary: ["肾结石预防", "甲状腺结节"],\n        fitness_goal: "增肌",\n        fitness_week: 3\n',
  '        // 健康与体况字段已移出公开文件（本地私有，不提交仓库）\n'),
 ('height_cm: 170, weight_kg: 59, dietary: ["肾结石预防", "甲状腺结节"], fitness_goal: "增肌", fitness_week: 3',
  '// 健康与体况字段已移出公开文件'),
 ('// 饮食：健康相关（肾结石/甲状腺）', '// 饮食'),

 # ── 饮食页副标题：去诊断名 ──
 ('肾结石·甲状腺结节·增肌食谱', '低草酸·高蛋白·增肌食谱'),
 ('肾结石·甲状腺结节增肌食谱', '低草酸·高蛋白·增肌食谱'),

 # ── 甲状腺结节 callout：改通用表述 ──
 ('<strong>🦋 甲状腺结节：</strong>不需要限碘；十字花科蔬菜必须煮熟；少辛辣；每年复查 B 超 + 甲功',
  '<strong>🦋 饮食注意：</strong>无需限碘；十字花科蔬菜建议煮熟食用；少辛辣；按医嘱定期复查'),
 ('<strong>🦋 甲状腺结节：</strong>', '<strong>🦋 饮食注意：</strong>'),
 ('甲状腺结节饮食细节以医嘱为准', '饮食细节以医嘱为准'),
 ('复查日历（肾结石半年B超/甲状腺结节一年一次）', '复查日历（按医嘱周期设置）'),
 ('②甲状腺结节：遵医嘱每年复查甲功+B超，十字花科蔬菜煮熟吃；', '②按医嘱定期复查，十字花科蔬菜煮熟吃；'),
 ('①肾结石：每年/半年B超复查一次，每天2.5L水+柠檬水，少草酸食物；', '①每天饮水≥2.5L（可加柠檬水），少高草酸食物，按医嘱定期复查；'),
 ('有肾结石预防需求（每天饮水≥2.5', '有饮水与饮食方面的健康约束（每天饮水≥2.5'),
 ('肾结石预防', '低草酸饮食'),
 ('甲状腺结节', '健康注意'),
]

report = []
for fn in FILES:
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        report.append((fn, '跳过（不存在）', 0)); continue
    c = open(p, encoding='utf-8').read()
    orig = c
    n = 0
    for a, b in REPL:
        if a in c:
            n += c.count(a)
            c = c.replace(a, b)
    if c != orig:
        open(p, 'w', encoding='utf-8').write(c)
        report.append((fn, '✅ 已修改', n))
    else:
        report.append((fn, '无匹配', 0))

print('=== 脱敏结果 ===')
for fn, st, n in report:
    print('  %-24s %s  %d 处' % (fn, st, n))

print()
print('=== 残留检查（诊断名称）===')
left = 0
for fn in FILES:
    p = os.path.join(BASE, fn)
    if not os.path.exists(p): continue
    c = open(p, encoding='utf-8').read()
    for kw in ['甲状腺', '肾结石']:
        for m in re.finditer(kw, c):
            left += 1
            s = max(0, m.start() - 40); e = min(len(c), m.start() + 40)
            print('  ⚠️ %s：…%s…' % (fn, c[s:e].replace('\n', ' ')))
print('  残留合计: %d 处' % left)

for fn in ['personal_config.js', 'daily_data.js', 'detail_content.js']:
    p = os.path.join(BASE, fn)
    if os.path.exists(p):
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        print('  语法 %-22s %s' % (fn, 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:150]))
