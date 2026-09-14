# -*- coding: utf-8 -*-
"""重写 DETAIL.fitness：从「8周腹肌专项（减脂向）」改为「增肌+腹肌 双目标（增肌向）」
   用户现状：170cm/59kg · 体脂 15-18% → 典型瘦胖子（skinny fat）
   核心判断：不该继续减脂，应该增肌——肌肉变厚腹肌才会显，同时体脂率自然下降
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\detail_content.js'

H = []
A = H.append

A('<h2>💪 健身方案 · 增肌 + 腹肌 双目标</h2>')
A('<p class="detail-subtitle">170cm/59kg 瘦胖子体型 · 增肌为主，腹肌自然显现 · 12周计划</p>')

A('<div class="callout warn" style="border-left:4px solid #10b981">'
  '<strong>🎯 结论：对你来说，「练腹肌」和「增肌」不是两件事，是同一件事。</strong><br><br>'
  '<strong>你的情况</strong>：170cm / 59kg · 体脂约 15-18% → 典型【瘦胖子】<br>'
  '<strong>关键判断</strong>：你的体脂率偏高，<b>不是因为脂肪太多，而是因为肌肉太少</b>。'
  '59kg 的人继续减脂 → 掉到 55kg，看起来更瘦弱，腹肌照样不明显（腹肌本身太薄，顶不出来）。<br>'
  '<strong>正确策略</strong>：<b>增肌为主 + 严格控脂</b>（lean bulk）。'
  '腹肌厚度增加 → 腹肌顶出来；肌肉量上升 → 体脂率自然下降。<br>'
  '<strong>不能做的事</strong>：继续按减脂思路练（大量跳绳 + 热量缺口）——那会让你越练越瘦、越练越没型。'
  '</div>')

A('<h3>📊 三条路线 · 12 周后你会是什么样</h3>')
A('<table class="data-table">'
  '<tr><th>路线</th><th>怎么做</th><th>12周后</th><th>体脂率</th><th>腹肌</th><th>评价</th></tr>'
  '<tr><td><strong>继续减脂</strong></td><td>热量缺口 + 大量跳绳</td><td>55-56kg</td><td>约12%</td><td>隐约可见</td>'
  '<td style="color:var(--red)">❌ 更瘦弱，脱衣没料</td></tr>'
  '<tr><td><strong>放开吃增肌</strong></td><td>大幅盈余 + 不控饮食</td><td>65kg+</td><td>19-20%</td><td>看不到</td>'
  '<td style="color:var(--red)">❌ 壮但糊，之后还要再减一轮</td></tr>'
  '<tr style="background:var(--accent-light)"><td><strong>增肌+控脂 ✅</strong></td><td>轻微盈余 + 力量为主</td>'
  '<td><b>62-63kg</b></td><td>13-14%</td><td><b>清晰</b></td>'
  '<td style="color:var(--green)">✅ 精瘦有型（推荐）</td></tr>'
  '</table>')
A('<div class="callout tip">按每周增重 <b>0.25-0.5kg</b> 的速度（每月 1-2kg），12 周就是 3-5kg 肌肉。'
  '这个速度慢，但长的是肌肉不是肥肉——腹肌才会【看起来是练出来的】，而不是【饿出来的】。</div>')

A('<h3>🔧 相比你现在的计划，必须改 3 处</h3>')
A('<div class="ex-list">'
  '<div class="ex-item c4"><span class="ex-n">① 加练腿（原来完全没有）</span><span class="ex-s">最重要</span></div>'
  '<div class="ex-item c1"><span class="ex-n">② 跳绳 3天 → 1-2天</span><span class="ex-s">减量</span></div>'
  '<div class="ex-item c3"><span class="ex-n">③ 热量 缺口 → 轻微盈余</span><span class="ex-s">+200 kcal</span></div>'
  '</div>')
A('<div class="callout info">'
  '<strong>① 为什么练腿最重要？</strong>腿部是全身最大肌群，占全身肌肉量一半以上。'
  '不练腿 = 增肌效率直接砍半，而且会练成【上身壮、下身细】的失衡体型。'
  '你的下肢动作：深蹲 → 保加利亚分腿蹲 → 臀桥 → 提踵，全部可徒手起步，再用拉力绳或装书的背包加重。<br><br>'
  '<strong>② 为什么要减跳绳？</strong>长时间有氧会消耗本该用于增肌的热量与恢复能力（干扰效应）。'
  '跳绳保留 1-2 次即可——它对你仍有用：心肺、小腿、控制体脂，而且是你喜欢的项目。<br><br>'
  '<strong>③ 为什么改热量？</strong>59kg 的人靠【缺口】无法长肌肉——没原料。'
  '轻微盈余（每天多 200 kcal）+ 高蛋白，才能让肌肉长、脂肪几乎不涨。'
  '</div>')

A('<h3>📅 新版周训练计划（增肌版 · 4 力量日 + 1 有氧日）</h3>')
A('<div class="wk-plan">'
  '<div class="wk-day strength"><div class="wk-w">周一</div><div class="wk-i">💪</div>'
  '<div class="wk-t">上肢推 + 腹肌A</div><div class="wk-m">俯卧撑/推举<br>40min</div></div>'
  '<div class="wk-day legs"><div class="wk-w">周二</div><div class="wk-i">🦵</div>'
  '<div class="wk-t">下肢力量</div><div class="wk-m">深蹲/分腿蹲<br>40min</div></div>'
  '<div class="wk-day rest"><div class="wk-w">周三</div><div class="wk-i">🚶</div>'
  '<div class="wk-t">恢复日</div><div class="wk-m">快走+拉伸<br>30min</div></div>'
  '<div class="wk-day strength"><div class="wk-w">周四</div><div class="wk-i">🎗️</div>'
  '<div class="wk-t">上肢拉 + 腹肌B</div><div class="wk-m">划船/下拉<br>40min</div></div>'
  '<div class="wk-day legs"><div class="wk-w">周五</div><div class="wk-i">🍑</div>'
  '<div class="wk-t">下肢臀 + 核心</div><div class="wk-m">单腿/臀桥<br>40min</div></div>'
  '<div class="wk-day cardio"><div class="wk-w">周六</div><div class="wk-i">🪢</div>'
  '<div class="wk-t">轻有氧</div><div class="wk-m">跳绳/快走<br>25-30min</div></div>'
  '<div class="wk-day rest"><div class="wk-w">周日</div><div class="wk-i">😴</div>'
  '<div class="wk-t">完全休息</div><div class="wk-m">泡沫轴<br>拉伸</div></div>'
  '</div>')
A('<div class="wk-legend">'
  '<span><i style="background:#3b82f6"></i>上肢力量</span>'
  '<span><i style="background:#10b981"></i>下肢力量</span>'
  '<span><i style="background:#8b5cf6"></i>腹肌专项</span>'
  '<span><i style="background:#f59e0b"></i>有氧/跳绳</span>'
  '<span><i style="background:#cbd5e1"></i>休息恢复</span>'
  '</div>')

A('<h3>🏋️ 每日动作清单（含加重方案）</h3>')
A('<table class="data-table">'
  '<tr><th>训练日</th><th>动作</th><th>组×次</th><th>怎么加重</th></tr>')


def rows(day, note, acts, hl=True):
    bg = ' style="background:var(--accent-light)"' if hl else ''
    out = ''
    for k, (a, s, w) in enumerate(acts):
        head = ''
        if k == 0:
            head = ('<td rowspan="' + str(len(acts)) + '"><strong>' + day + '</strong><br>'
                    '<span style="font-size:9px;color:var(--text3)">' + note + '</span></td>')
        out += '<tr' + bg + '>' + head + '<td>' + a + '</td><td>' + s + '</td><td>' + w + '</td></tr>'
    return out


A(rows('周一', '上肢推+腹肌A', [
    ('负重俯卧撑（背包装书）', '4×8-12', '每2周加2-3kg'),
    ('下斜俯卧撑（上胸）', '4×10-12', '抬高双脚'),
    ('拉力绳站姿推举（肩）', '3×12-15', '换更短绳/双绳'),
    ('拉力绳跪姿卷腹 + 死虫式', '4×15 / 3×12', '加组数'),
]))
A(rows('周二', '下肢力量', [
    ('深蹲（自重→负重）', '4×12-15', '抱书/拉力绳'),
    ('保加利亚分腿蹲', '3×10/腿', '手持负重'),
    ('臀桥（单腿进阶）', '4×15', '单腿→负重'),
    ('提踵', '4×20', '单腿'),
], hl=False))
A(rows('周四', '上肢拉+腹肌B', [
    ('拉力绳坐姿划船', '4×12-15', '缩短绳长'),
    ('拉力绳高位下拉', '4×12', '双绳叠加'),
    ('面拉（改善圆肩）', '3×15', '加组数'),
    ('仰卧抬腿 + 俄罗斯转体', '4×15 / 3×20', '加负重'),
]))
A(rows('周五', '下肢臀+核心', [
    ('单腿硬拉（徒手→负重）', '3×10/腿', '手持负重'),
    ('侧弓步', '3×12/腿', '负重'),
    ('单腿臀桥', '4×12/腿', '脚下垫高'),
    ('平板支撑变式 + 侧平板', '3×90秒 / 3×45秒', '负重/单腿'),
], hl=False))
A(rows('周六', '轻有氧', [('跳绳间歇 或 快走（可户外）', '25-30min', '别当HIIT练')]))
A(rows('周日', '休息', [('泡沫轴放松 + 全身静态拉伸', '20min', '—')], hl=False))
A('</table>')
A('<div class="callout tip">跳绳膝盖不适 → 改【无绳跳】或【开合跳】；穿有缓冲的鞋，落地用前脚掌。'
  '每个力量动作做到【最后 2-3 次很吃力但动作不变形】才算有效组。</div>')

A('<h3>📈 渐进超负荷（增肌的唯一开关）</h3>')
A('<table class="data-table">'
  '<tr><th>阶段</th><th>周次</th><th>上肢推</th><th>下肢</th><th>腹肌</th><th>跳绳</th></tr>'
  '<tr style="background:var(--accent-light)"><td><strong>适应期</strong></td><td>第1-2周</td>'
  '<td>自重变式 3×12（留2次余力）</td><td>自重 3×12</td><td>3组/动作</td><td>10min×1次</td></tr>'
  '<tr style="background:var(--accent-light)"><td><strong>增肌期</strong></td><td>第3-8周</td>'
  '<td>背包负重 4×8-12 至力竭</td><td>负重 4×10-12</td><td>4组 + 负重</td><td>15min×2次</td></tr>'
  '<tr style="background:var(--accent-light)"><td><strong>强化期</strong></td><td>第9-12周</td>'
  '<td>负重+爆发 4×6-10</td><td>单腿+负重 4×8-10</td><td>5组/动作</td><td>20min×2次</td></tr>'
  '</table>')
A('<div class="callout info"><strong>加重原则（每周只推一项，别同时加）：</strong><br>'
  '① <b>次数先涨</b>：同样负重从 8 次练到 12 次 → ② <b>加重再回落</b>：加 2-3kg，次数掉回 8 次，再往上练。'
  '这样循环就是持续超负荷。<br>'
  '<strong>参照物：</strong>你标准俯卧撑能一口气做 60 个，说明自重已经完全适应——'
  '继续做自重只练耐力、不长肌肉。<b>必须加负重或改更难变式</b>，这是你最需要改变的一点。</div>')

A('<h3>🍽️ 饮食调整（增肌版 · 与原计划的关键差异）</h3>')
A('<table class="data-table">'
  '<tr><th>项目</th><th>原计划（减脂向）</th><th>新方案（增肌向）</th><th>为什么改</th></tr>'
  '<tr><td><strong>热量</strong></td>'
  '<td>2300-2500 kcal<br><span style="font-size:9px;color:var(--red)">轻缺口</span></td>'
  '<td><b>2400-2600 kcal</b><br><span style="font-size:9px;color:var(--green)">训练日+200 / 休息日持平</span></td>'
  '<td>59kg 没原料长肌肉；缺口只会掉体重</td></tr>'
  '<tr><td><strong>蛋白质</strong></td><td>106-130g</td>'
  '<td><b>110-130g</b>（1.9-2.2g/kg）</td><td>增肌期更不能少，保持高位</td></tr>'
  '<tr><td><strong>碳水</strong></td><td>训练日55% / 休息日40%</td>'
  '<td><b>训练日 50-55% / 休息日 45%</b></td><td>碳水是训练燃料，降太低练不动</td></tr>'
  '<tr><td><strong>脂肪</strong></td><td>未特别规定</td><td>25-30%（约 70-85g）</td>'
  '<td>激素合成需要，不要低于 0.8g/kg</td></tr>'
  '<tr><td><strong>有氧</strong></td><td>跳绳 3-4 次/周</td><td><b>跳绳 1-2 次/周</b></td>'
  '<td>过量有氧抢走增肌的热量与恢复</td></tr>'
  '<tr><td><strong>加餐</strong></td><td>不强调</td><td><b>训练后 30-60min 内</b>补蛋白+快碳</td>'
  '<td>恢复更快，下次训练更有劲</td></tr>'
  '</table>')

A('<h4 style="font-size:12px;margin:14px 0 6px">一天怎么吃（约 2500 kcal / 蛋白约 120g）</h4>')
A('<table class="data-table">'
  '<tr><th>时间</th><th>内容</th><th>蛋白</th><th>要点</th></tr>'
  '<tr><td>07:30 早餐</td><td>鸡蛋 2 个 + 全麦面包 2 片 + 牛奶 300ml</td><td>约25g</td><td>别空腹只喝咖啡</td></tr>'
  '<tr><td>10:30 加餐</td><td>无糖酸奶 + 香蕉</td><td>约10g</td><td>防中午暴食</td></tr>'
  '<tr><td>12:30 午餐</td><td>米饭 1.5 碗 + 鸡胸/牛肉 150g + 蔬菜</td><td>约40g</td><td>主食别省，下午要练</td></tr>'
  '<tr><td>16:30 训练前</td><td>香蕉 或 面包 1 片</td><td>约3g</td><td>练前 1 小时补碳水</td></tr>'
  '<tr><td>18:30 训练后</td><td>乳清蛋白 1 勺 或 鸡蛋 3 个 + 米饭</td><td>约25g</td><td>练后 30-60min 内</td></tr>'
  '<tr><td>20:00 晚餐</td><td>杂粮饭 + 鱼/鸡腿 + 大量蔬菜</td><td>约30g</td><td>睡前 3 小时吃完</td></tr>'
  '</table>')
A('<div class="callout warn"><strong>🪨 肾结石预防（你的固定需求，增肌期尤其重要）：</strong>'
  '高蛋白饮食必须配足量水 → <b>每天 ≥2.5L</b>；控草酸（少菠菜/苋菜/浓茶/巧克力/坚果，'
  '要吃就配奶制品同餐）；限盐 &lt;5g；适量补钙（不要因为怕结石而完全不吃钙）。</div>')
A('<div class="callout warn"><strong>🦋 甲状腺结节：</strong>不需要限碘；'
  '十字花科蔬菜（西兰花/卷心菜）必须煮熟再吃；少辛辣；每年复查。</div>')

A('<h3>📏 追踪表（6 个指标 · 别只看体重）</h3>')
A('<table class="data-table">'
  '<tr><th>周次</th><th>体重(kg)</th><th>腰围(cm)</th><th>胸围(cm)</th><th>大腿(cm)</th><th>俯卧撑最大次数</th><th>照片</th></tr>'
  '<tr><td>第0周（9/13）</td><td>59</td><td>____</td><td>____</td><td>____</td><td>60</td><td>☐ 基线</td></tr>'
  '<tr><td>第4周</td><td>____</td><td>____</td><td>____</td><td>____</td><td>____</td><td>☐</td></tr>'
  '<tr><td>第8周</td><td>____</td><td>____</td><td>____</td><td>____</td><td>____</td><td>☐</td></tr>'
  '<tr><td>第12周</td><td>____</td><td>____</td><td>____</td><td>____</td><td>____</td><td>☐</td></tr>'
  '</table>')
A('<div class="callout tip"><strong>增肌期怎么读数据：</strong><br>'
  '· 体重 <b>每周涨 0.25-0.5kg</b> = 速度合适 ✅<br>'
  '· 体重完全不涨 = 吃少了 → 每天再加 200 kcal<br>'
  '· 体重涨太快（&gt;0.75kg/周）= 脂肪在涨 → 每天减 200 kcal<br>'
  '· <b>腰围涨、但胸围/大腿也涨</b> = 正常（肌肉+少量脂肪）<br>'
  '· 腰围涨但其它围度不动 = 吃多了 → 收紧热量<br>'
  '· 早晨空腹、肚脐水平量腰围，每周固定同一时间</div>')

A('<h3>🔀 12 周后怎么判断下一步</h3>')
A('<table class="data-table">'
  '<tr><th>12 周后的情况</th><th>下一步怎么做</th></tr>'
  '<tr><td>腹肌轮廓明显、体重 62kg 以上</td><td>进入 <b>4-6 周轻度减脂</b>（热量 -300），把腹肌【擦干净】</td></tr>'
  '<tr><td>腹肌仍不明显、体重涨到 63kg 以上</td><td><b>继续增肌 4-8 周</b>——腹肌显现靠【肌肉更厚】，不是靠更瘦</td></tr>'
  '<tr><td>体重没涨（仍在 60kg 以下）</td><td>说明吃不够：每天再加 200-300 kcal，优先加碳水和蛋白</td></tr>'
  '<tr><td>腰围涨了 3cm 以上但腹肌没变化</td><td>盈余过大 → 回到维持热量，并把有氧加回 2-3 次</td></tr>'
  '</table>')

A('<h3>🧬 三个必须记住的认知</h3>')
A('<div class="ex-list">'
  '<div class="ex-item c1"><span class="ex-n">腹肌是【厨房+铁】练出来的</span></div>'
  '<div class="ex-item c2"><span class="ex-n">局部减脂不存在（只能整体降）</span></div>'
  '<div class="ex-item c3"><span class="ex-n">看围度进步，不看体重</span></div>'
  '</div>')
A('<p style="font-size:11px;color:var(--text2);margin:-4px 0 12px">'
  '腹肌可见度 = 腹肌厚度 ÷ 体脂率。你现在要做的是把<b>分子</b>做大（增肌），'
  '而不是拼命压<b>分母</b>（减脂）——分母已经不大，再压就变成纸片人了。'
  '增肌后体重可能涨到 62kg，但腰围反而可能不变甚至更细（肌肉密度大于脂肪）。</p>')
A('<div class="highlight-box"><p><strong>增肌三要素（缺一不可）：</strong>'
  '①机械张力（渐进超负荷）②代谢压力（泵感）③肌肉损伤（休息时修复）。'
  '每组 8-15 次做到接近力竭 = 增肌黄金区间。你现在的问题是第①项长期没变过。</p></div>')
A('<div class="callout info"><strong>为什么练背能让腹肌更显：</strong>'
  '背阔肌变宽 → 视觉上腰变细（倒三角）→ 腹肌轮廓更突出；面拉还能改善圆肩驼背。'
  '这也是为什么你的计划里【拉】和【推】必须一样多。</div>')

A('<h3>🎥 博主推荐</h3>')
for icon, name, desc, url in [
    ('🏋️', 'Jeremy Ethier (YouTube)', '科学健身第一人，每期都有论文支撑', 'https://www.youtube.com/@JeremyEthier'),
    ('💀', 'Athlean-X (YouTube)', '解剖学视角讲动作，纠正细节', 'https://www.youtube.com/@athleanx'),
    ('🇨🇳', '闫帅奇（B站）', '家庭健身·拉力绳/徒手训练中文讲解',
     'https://search.bilibili.com/all?keyword=%E9%97%AB%E5%B8%85%E5%A5%87%E5%AE%B6%E5%BA%AD%E5%81%A5%E8%BA%AB'),
]:
    A('<div class="resource-card"><div class="rc-icon">' + icon + '</div>'
      '<div class="rc-info"><div class="rc-name">' + name + '</div>'
      '<div class="rc-desc">' + desc + '</div></div>'
      '<a href="' + url + '" target="_blank" class="rc-link">打开 →</a></div>')

A('<div class="callout warn">⚠️ 安全提醒：热身 5 分钟 ｜ 检查拉力绳固定 ｜ 关节疼立刻停 ｜ '
  '每周休息 ≥2 天 ｜ 增肌期睡眠 ≥7 小时（睡不够等于白练）</div>')

html = ''.join(H)
esc = html.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '').replace('\r', '')
new_line = "DETAIL.fitness = '" + esc + "';"

d = open(FP, 'r', encoding='utf-8').read()
i = d.index('DETAIL.fitness')
j = d.index('DETAIL.diet')
old = d[i:j]
d = d[:i] + new_line + '\n\n' + d[j:]
open(FP, 'w', encoding='utf-8').write(d)

print('OK 已重写 DETAIL.fitness')
print('  原长度:', len(old), '字符')
print('  新长度:', len(new_line), '字符')
print('  单行:', new_line.count('\n') == 0)
print('  含中文单引号(应False):', ('\u2018' in html or '\u2019' in html))
print('  含英文撇号(应False):', ("'" in html))
