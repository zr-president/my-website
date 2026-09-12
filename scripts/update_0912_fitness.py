# -*- coding: utf-8 -*-
"""在 DETAIL.fitness 顶部插入「8周腹肌专项计划」（用户专属：俯卧撑60/平板2.5min·跳绳+拉力绳）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\detail_content.js'
c = open(FP, 'r', encoding='utf-8').read()

anchor = """DETAIL.fitness = '<h2>💪 健身方案</h2><p class="detail-subtitle">家庭健身也能练出薄肌</p>'+
'<h3>🧬 增肌原理</h3>"""

plan = """DETAIL.fitness = '<h2>💪 健身方案</h2><p class="detail-subtitle">增肌基础 + 8周腹肌专项计划（跳绳·俯卧撑·拉力绳·平板）</p>'+

'<div class="callout warn" style="border-left:4px solid #e11d48"><strong>🎯 当前目标：练出腹肌（8周专项·9/12启动）</strong><br>'
'<strong>你的情况：</strong>170cm/59kg 偏瘦、能摸出腹肌轮廓但仍有赘肉 → 判断为【体脂率约15-18%的瘦胖子】(skinny fat)。<br>'
'<strong>核心矛盾：</strong>腹肌可见的关键是<b>体脂率</b>（男性需 ≤12-15%），而不是腹肌练得多——练腹只能让腹肌变厚，不能消掉覆盖它的脂肪。<br>'
'<strong>为什么不能靠饿：</strong>你59kg已偏瘦，大减重会掉肌肉、变成「更瘦但更松」→ 正确做法是<b>控脂同时增加肌肉量</b>（腹肌厚度+背部宽度，背宽了腰显细）。<br>'
'<strong>你的基础：</strong>俯卧撑一口气 60 个（优秀）· 平板支撑 2分半（很强）→ 可以直接上强度。<br>'
'<strong>策略：</strong>跳绳HIIT控脂 + 腹肌增厚 + 俯卧撑变式升级 + 蛋白质提升（四轨并行）。</div>'+

'<h3>📅 每周训练结构（4练+2轻有氧+1休）</h3>'+
'<table class="data-table"><tr><th>星期</th><th>训练内容</th><th>时长</th></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>周一</strong></td><td>跳绳HIIT + 腹肌专项A</td><td>35-40min</td></tr>'+
'<tr><td><strong>周二</strong></td><td>俯卧撑变式（胸/三头）+ 拉力绳背</td><td>35min</td></tr>'+
'<tr><td><strong>周三</strong></td><td>休息 / 快走30min（主动恢复）</td><td>30min</td></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>周四</strong></td><td>跳绳HIIT + 腹肌专项B</td><td>35-40min</td></tr>'+
'<tr><td><strong>周五</strong></td><td>拉力绳全身 + 平板支撑变式</td><td>35min</td></tr>'+
'<tr><td><strong>周六</strong></td><td>有氧40min（跳绳/快走，稳态）</td><td>40min</td></tr>'+
'<tr><td><strong>周日</strong></td><td>休息 + 全身拉伸/泡沫轴</td><td>20min</td></tr>'+
'</table>'+

'<h3>🪢 跳绳（减脂主力·每周3-4次·每次15-20分钟）</h3>'+
'<div class="highlight-box"><p>燃脂效率极高（每小时约600-1000kcal），是整体降体脂的核心手段（局部减脂不存在，只能整体降）。<br>'
'<strong>初阶（第1-2周）：</strong>30秒快跳 + 30秒休息 × 10组<br>'
'<strong>进阶（第3-5周）：</strong>40秒跳 + 20秒休息 × 12组<br>'
'<strong>高阶（第6-8周）：</strong>60秒跳 + 30秒休息 × 10组，中途穿插双摇（Double Under）<br>'
'<strong>注意：</strong>膝盖不适改「无绳跳」或「开合跳」；穿有缓冲的鞋；落地用前脚掌。</p></div>'+

'<h3>🔥 腹肌专项A（上腹+整体·每周2次）</h3>'+
'<table class="data-table"><tr><th>动作</th><th>组次</th><th>要点</th></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>拉力绳跪姿卷腹</strong></td><td>4×15</td><td>绳固定高处，跪姿向下卷腹，感受上腹收缩（不是用手拉）</td></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>平板支撑变式</strong></td><td>3×90秒</td><td>你已能做2.5min → 升级为「负重平板」(背上放书)或「单腿抬起平板」</td></tr>'+
'<tr><td><strong>仰卧抬腿</strong></td><td>4×15</td><td>下腹重点，腿下放时不要触地，全程腹肌发力</td></tr>'+
'<tr><td><strong>死虫式</strong></td><td>3×12/侧</td><td>对侧手脚伸展，腰部贴地不拱起</td></tr>'+
'</table>'+

'<h3>⚡ 腹肌专项B（下腹+侧腹·每周2次）</h3>'+
'<table class="data-table"><tr><th>动作</th><th>组次</th><th>要点</th></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>拉力绳伐木式</strong></td><td>3×12/侧</td><td>斜向拉动（高→低/低→高），转体用腹斜肌发力</td></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>侧平板支撑</strong></td><td>3×45秒/侧</td><td>侧腹，身体成一条直线不塌腰</td></tr>'+
'<tr><td><strong>反向卷腹</strong></td><td>4×15</td><td>下腹关键动作，用腹肌把骨盆卷起（不是甩腿）</td></tr>'+
'<tr><td><strong>俄罗斯转体</strong></td><td>3×20</td><td>可抱书/水瓶负重，转体时眼睛跟着手走</td></tr>'+
'</table>'+

'<h3>💪 俯卧撑升级（你已60个·必须加难度才继续进步）</h3>'+
'<table class="data-table"><tr><th>变式</th><th>组次</th><th>针对性</th></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>宽距俯卧撑</strong></td><td>4×20</td><td>胸外侧</td></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>钻石俯卧撑</strong></td><td>4×12</td><td>三头肌（手臂线条）</td></tr>'+
'<tr><td><strong>下斜俯卧撑</strong></td><td>4×15</td><td>上胸（脚垫高）</td></tr>'+
'<tr><td><strong>爆发/击掌俯卧撑</strong></td><td>3×8-10</td><td>爆发力+核心稳定</td></tr>'+
'</table>'+
'<div class="callout tip"><strong>为什么改变式：</strong>标准俯卧撑你能做60个，说明已高度适应→继续做只会练耐力不会长肌肉。加难度（变式/负重）才能持续刺激。</div>'+

'<h3>🎗️ 拉力绳（补背+改善体态·让腹肌更显）</h3>'+
'<table class="data-table"><tr><th>动作</th><th>组次</th><th>作用</th></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>高位下拉</strong></td><td>4×15</td><td>背阔肌（视觉宽度，腰显细）</td></tr>'+
'<tr style="background:var(--accent-light)"><td><strong>面拉</strong></td><td>3×15</td><td>后肩+改善圆肩驼背（体态好腹肌更突出）</td></tr>'+
'<tr><td><strong>坐姿划船</strong></td><td>3×15</td><td>中背厚度</td></tr>'+
'<tr><td><strong>站姿推举</strong></td><td>3×12</td><td>肩部（衣架子）</td></tr>'+
'</table>'+

'<h3>🍽️ 饮食（决定成败·80%的效果在这里）</h3>'+
'<div class="callout warn"><strong>腹肌是「厨房里练出来的」——饮食不调整，练再多也看不到腹肌。</strong><br>'
'① <strong>热量</strong>：维持 2300-2500kcal（轻缺口约200即可）——<b>不要大开缺口</b>，你会掉肌肉变成更瘦更松；<br>'
'② <strong>蛋白质提到 106-130g/天</strong>（1.8-2.2g/kg，比增肌期更重要）——鸡胸/鱼/蛋/乳清；<br>'
'③ <strong>碳水循环</strong>：训练日碳水占55%、休息日降到40%（加速控脂）；<br>'
'④ <strong>戒含糖饮料/夜宵/精制糖</strong>——这是最快见效的一步，2周就能看到腰围变化；<br>'
'⑤ <strong>补水 ≥2.5L + 柠檬水</strong>（你有肾结石预防需求，同时控草酸：菠菜/苋菜/浓茶/巧克力）；<br>'
'⑥ <strong>睡眠 7-8h</strong>——皮质醇偏高会让脂肪优先堆在腹部。</div>'+

'<h3>📏 监测与预期（看腰围·不看体重）</h3>'+
'<div class="highlight-box"><p><strong>每周固定时间量腰围</strong>（早晨空腹·肚脐水平）——腰围减少才是真的减脂；体重可能不变甚至略增（肌肉增加），这是好事。<br>'
'<strong>每周拍一张正面照片</strong>（同一光线/姿势）——视觉对比比体重秤真实。<br>'
'<strong>8周预期：</strong>执行到位 → 体脂率降 2-4 个百分点、腹肌轮廓明显、腰围减少 2-4cm。<br>'
'<strong>如果4周没变化：</strong>优先检查饮食（80%概率是吃的问题，而不是练得不够）。</p></div>'+

'<h3>🧬 增肌原理</h3>"""

if anchor in c:
    c = c.replace(anchor, plan, 1)
    open(FP, 'w', encoding='utf-8').write(c)
    print('OK DETAIL.fitness 腹肌计划已插入')
else:
    print('ANCHOR MISS')
