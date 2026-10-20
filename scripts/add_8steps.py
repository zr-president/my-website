# -*- coding: utf-8 -*-
"""补入「AI 编程八步法」详细块"""
import io, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\index.html'
h = open(FP, encoding='utf-8').read()

ANCHOR = '<h3>三、五个提升方向</h3>'
MARK = '改原型比改代码便宜得多'

BLOCK = (
 '<div class="callout" style="margin:12px 0">'
 '<strong>📐 附：文档里的「AI 编程八步法」（第 41-54 页，最实用的一段）</strong><br><br>'
 '<b>两个前提</b>：① <b>自己想清楚</b>——谁来用 / 解决什么 / 做到哪　'
 '② <b>跟 AI 说清楚</b>——功能 / 规则 / 边界 / 验收标准<br><br>'
 '<b>八步</b>：① 聊需求（用 grill-me 这类 Skill 把需求逐条问清）'
 '② 出 PRD（背景目标 / 用户场景 / 范围优先级 / 功能流程 / 数据规则 / <b>验收标准</b>）'
 '③ 出原型（用模拟数据点一遍，<b>改原型比改代码便宜得多</b>）'
 '④ 定方案（技术方案 + 测试用例）⑤ 按模块开发 ⑥ 测试与迭代 ⑦ UI 优化 '
 '⑧ 部署上线（权限 / 备份 / 运行检查 / 维护）<br><br>'
 '<b>最值得抄走的一条</b>：测试用例要写成「用户执行什么操作 → 应该出现什么结果 → '
 '空值/重复/失败怎么处理」，而不是写「功能正常」。'
 '这和提示词的第六维度是同一个思路——<b>把验收标准前置</b>。'
 '</div>\n\n'
)

if MARK in h:
    print('ℹ️  已存在，跳过')
elif ANCHOR in h:
    h = h.replace(ANCHOR, BLOCK + ANCHOR, 1)
    open(FP, 'w', encoding='utf-8').write(h)
    print('✅ 已补入八步法详细块')
else:
    print('❌ 未找到锚点')
    i = h.find('三、五个提升方向')
    print('  相近文本:', repr(h[i-60:i+80]) if i > 0 else '未找到')

h2 = open(FP, encoding='utf-8').read()
for t in ['改原型比改代码便宜得多', '把验收标准前置', 'grill-me 这类 Skill', 'AI 编程八步法']:
    print('  含 %-24s %s' % (t, t in h2))
print('  文件大小: %.1f KB' % (len(h2.encode('utf-8')) / 1024))
