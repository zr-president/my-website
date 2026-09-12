# -*- coding: utf-8 -*-
"""修复 DETAIL.fitness：上次多行拼接缺 + 导致内容截断，改用「单个转义字符串」方式重写"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\detail_content.js'
c = open(FP, 'r', encoding='utf-8').read()

HTML = """<h2>💪 健身方案 · 8周腹肌专项</h2><p class="detail-subtitle">跳绳 · 俯卧撑 · 拉力绳 · 平板支撑</p>
<div class="callout warn" style="border-left:4px solid #e11d48"><strong>🎯 目标：练出腹肌（8周专项）</strong><br><strong>你的情况</strong>：170cm / 59kg · 能摸出腹肌轮廓但有赘肉 → 体脂率约 15-18%（瘦胖子）｜目标体脂 ≤12-15%<br><strong>你的基础</strong>：俯卧撑 60 个 / 平板支撑 2分半 → 可直接上强度<br><strong>核心策略</strong>：跳绳控脂 + 腹肌增厚 + 俯卧撑变式 + 蛋白质提升（<b>不能靠饿</b>——已偏瘦，饿会掉肌肉）</div>
<h3>💡 三个关键认知</h3>
<div class="ex-list"><div class="ex-item c1"><span class="ex-n">腹肌是「厨房里练出来的」</span></div><div class="ex-item c2"><span class="ex-n">局部减脂不存在（只能整体降）</span></div><div class="ex-item c3"><span class="ex-n">看腰围，不看体重</span></div></div>
<p style="font-size:11px;color:var(--text2);margin:-4px 0 12px">体脂率决定腹肌可见度；练腹只让腹肌变厚，消不掉覆盖的脂肪；体重可能不变（肌肉增加）但腰围会降。</p>
<h3>📅 周训练计划表</h3>
<div class="wk-plan"><div class="wk-day cardio"><div class="wk-w">周一</div><div class="wk-i">🪢</div><div class="wk-t">跳绳HIIT</div><div class="wk-m">+ 腹肌A<br>35-40min</div></div><div class="wk-day strength"><div class="wk-w">周二</div><div class="wk-i">💪</div><div class="wk-t">俯卧撑变式</div><div class="wk-m">+ 拉力绳背<br>35min</div></div><div class="wk-day rest"><div class="wk-w">周三</div><div class="wk-i">🚶</div><div class="wk-t">恢复日</div><div class="wk-m">快走30min<br>拉伸</div></div><div class="wk-day cardio"><div class="wk-w">周四</div><div class="wk-i">🪢</div><div class="wk-t">跳绳HIIT</div><div class="wk-m">+ 腹肌B<br>35-40min</div></div><div class="wk-day strength"><div class="wk-w">周五</div><div class="wk-i">🎗️</div><div class="wk-t">拉力绳全身</div><div class="wk-m">+ 平板变式<br>35min</div></div><div class="wk-day cardio"><div class="wk-w">周六</div><div class="wk-i">🏃</div><div class="wk-t">稳态有氧</div><div class="wk-m">跳绳/快走<br>40min</div></div><div class="wk-day rest"><div class="wk-w">周日</div><div class="wk-i">😴</div><div class="wk-t">完全休息</div><div class="wk-m">泡沫轴<br>拉伸</div></div></div>
<div class="wk-legend"><span><i style="background:#f59e0b"></i>有氧/跳绳</span><span><i style="background:#8b5cf6"></i>腹肌专项</span><span><i style="background:#3b82f6"></i>力量/拉力绳</span><span><i style="background:#cbd5e1"></i>休息恢复</span></div>
<h3>🏋️ 每日动作清单</h3>
<table class="data-table"><tr><th>训练日</th><th>动作</th><th>组×次</th></tr>
<tr style="background:var(--accent-light)"><td rowspan="4"><strong>周一</strong><br><span style="font-size:9px;color:var(--text3)">跳绳+腹肌A</span></td><td>跳绳（见下方配速表）</td><td>15-20min</td></tr>
<tr style="background:var(--accent-light)"><td>拉力绳跪姿卷腹</td><td>4×15</td></tr>
<tr style="background:var(--accent-light)"><td>平板支撑变式（负重/单腿）</td><td>3×90秒</td></tr>
<tr style="background:var(--accent-light)"><td>仰卧抬腿 + 死虫式</td><td>4×15 / 3×12侧</td></tr>
<tr><td rowspan="4"><strong>周二</strong><br><span style="font-size:9px;color:var(--text3)">俯卧撑+背</span></td><td>宽距俯卧撑</td><td>4×20</td></tr>
<tr><td>钻石俯卧撑（三头）</td><td>4×12</td></tr>
<tr><td>下斜俯卧撑（上胸）</td><td>4×15</td></tr>
<tr><td>拉力绳高位下拉 + 面拉</td><td>4×15 / 3×15</td></tr>
<tr style="background:var(--accent-light)"><td rowspan="4"><strong>周四</strong><br><span style="font-size:9px;color:var(--text3)">跳绳+腹肌B</span></td><td>跳绳（见下方配速表）</td><td>15-20min</td></tr>
<tr style="background:var(--accent-light)"><td>拉力绳伐木式（腹斜肌）</td><td>3×12/侧</td></tr>
<tr style="background:var(--accent-light)"><td>侧平板支撑</td><td>3×45秒/侧</td></tr>
<tr style="background:var(--accent-light)"><td>反向卷腹 + 俄罗斯转体</td><td>4×15 / 3×20</td></tr>
<tr><td rowspan="3"><strong>周五</strong><br><span style="font-size:9px;color:var(--text3)">拉力绳全身</span></td><td>拉力绳坐姿划船</td><td>3×15</td></tr>
<tr><td>拉力绳站姿推举（肩）</td><td>3×12</td></tr>
<tr><td>平板支撑 + 爆发俯卧撑</td><td>3×90秒 / 3×8-10</td></tr>
<tr style="background:var(--accent-light)"><td><strong>周六</strong><br><span style="font-size:9px;color:var(--text3)">有氧</span></td><td>稳态跳绳 或 快走（可户外）</td><td>40min</td></tr>
<tr><td><strong>周日</strong><br><span style="font-size:9px;color:var(--text3)">休息</span></td><td>泡沫轴放松 + 全身静态拉伸</td><td>20min</td></tr>
</table>
<h3>📈 8周强度进阶表</h3>
<table class="data-table"><tr><th>阶段</th><th>周次</th><th>跳绳配速</th><th>腹肌组数</th><th>俯卧撑</th></tr>
<tr style="background:var(--accent-light)"><td><strong>建立节奏</strong></td><td>第1-2周</td><td>30秒跳+30秒休×10组</td><td>3组/动作</td><td>变式各3组</td></tr>
<tr style="background:var(--accent-light)"><td><strong>强度提升</strong></td><td>第3-5周</td><td>40秒跳+20秒休×12组</td><td>4组/动作</td><td>变式各4组</td></tr>
<tr style="background:var(--accent-light)"><td><strong>冲刺期</strong></td><td>第6-8周</td><td>60秒跳+30秒休×10组（穿插双摇）</td><td>4组+负重</td><td>加负重/爆发</td></tr>
</table>
<div class="callout tip">跳绳膝盖不适 → 改「无绳跳」或「开合跳」；穿有缓冲的鞋，落地用前脚掌。腹肌动作做到「最后2次很吃力」才有效。</div>
<h3>🍽️ 饮食清单（决定成败·80%效果在这里）</h3>
<div class="ex-list"><div class="ex-item c1"><span class="ex-n">热量 2300-2500 kcal</span><span class="ex-s">轻缺口</span></div><div class="ex-item c2"><span class="ex-n">蛋白质 106-130g/天</span><span class="ex-s">1.8-2.2g/kg</span></div><div class="ex-item c3"><span class="ex-n">碳水循环（训练日55%/休息日40%）</span><span class="ex-s">控脂</span></div><div class="ex-item c4"><span class="ex-n">戒含糖饮料/夜宵/精制糖</span><span class="ex-s">最快见效</span></div><div class="ex-item c1"><span class="ex-n">补水≥2.5L + 柠檬水</span><span class="ex-s">兼顾结石预防</span></div><div class="ex-item c2"><span class="ex-n">睡眠 7-8h</span><span class="ex-s">控皮质醇</span></div></div>
<div class="callout warn">控草酸（菠菜/苋菜/浓茶/巧克力）——你有肾结石预防需求，高蛋白饮食必须配足量水。</div>
<h3>📏 每周追踪表（抄下来填）</h3>
<table class="data-table"><tr><th>周次</th><th>腰围(cm)</th><th>体重(kg)</th><th>正面照</th><th>备注</th></tr>
<tr><td>第0周(9/12)</td><td>____</td><td>59</td><td>☐ 已拍（基线）</td><td>起始</td></tr>
<tr><td>第2周</td><td>____</td><td>____</td><td>☐</td><td></td></tr>
<tr><td>第4周</td><td>____</td><td>____</td><td>☐</td><td>无变化则查饮食</td></tr>
<tr><td>第6周</td><td>____</td><td>____</td><td>☐</td><td></td></tr>
<tr><td>第8周</td><td>____</td><td>____</td><td>☐</td><td>预期腰围-2~4cm</td></tr>
</table>
<div class="callout tip">每周固定时间量腰围（早晨空腹·肚脐水平）。<strong>腰围减少 = 真的减脂</strong>；体重不变甚至略增（肌肉增加）是好事。</div>
<h3>🧬 增肌原理（打底知识）</h3>
<div class="highlight-box"><p><strong>三个变量缺一不可：</strong>①机械张力 ②代谢压力(泵感) ③肌肉损伤(休息时修复)。每组8-15次是增肌黄金区间。</p></div>
<div class="callout info"><strong>为什么俯卧撑要改变式：</strong>标准俯卧撑你能做60个，说明已高度适应 → 继续做只练耐力不长肌肉。加难度（变式/负重）才能持续刺激。</div>
<div class="callout info"><strong>为什么练背能让腹肌更显：</strong>背阔肌变宽 → 视觉上腰变细（倒三角）→ 腹肌轮廓更突出；面拉还能改善圆肩驼背。</div>
<h3>🎥 博主推荐</h3>
<div class="resource-card"><div class="rc-icon">🏋️</div><div class="rc-info"><div class="rc-name">Jeremy Ethier (YouTube)</div><div class="rc-desc">科学健身第一人，每期论文支撑</div></div><a href="https://www.youtube.com/@JeremyEthier" target="_blank" class="rc-link">打开 →</a></div>
<div class="resource-card"><div class="rc-icon">💀</div><div class="rc-info"><div class="rc-name">Athlean-X (YouTube)</div><div class="rc-desc">解剖学视角讲动作，纠正细节</div></div><a href="https://www.youtube.com/@athleanx" target="_blank" class="rc-link">打开 →</a></div>
<div class="resource-card"><div class="rc-icon">🇨🇳</div><div class="rc-info"><div class="rc-name">闫帅奇（B站）</div><div class="rc-desc">家庭健身·拉力绳/徒手训练中文讲解</div></div><a href="https://search.bilibili.com/all?keyword=%E9%97%AB%E5%B8%85%E5%A5%87%E5%AE%B6%E5%BA%AD%E5%81%A5%E8%BA%AB" target="_blank" class="rc-link">打开 →</a></div>
<div class="callout warn">⚠️ 安全提醒：热身5分钟｜检查拉力绳固定｜关节疼立刻停｜每周休息≥2天</div>"""

# 转义为 JS 单引号字符串（压成一行，避免拼接错误）
js_str = HTML.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '')

i = c.find('DETAIL.fitness = ')
j = c.find('\nDETAIL.', i+10)
if i < 0 or j < 0:
    print('MISS'); sys.exit()
c = c[:i] + "DETAIL.fitness = '" + js_str + "';" + c[j:]
open(FP, 'w', encoding='utf-8').write(c)
print('OK 已重写（单字符串方式）')
