# -*- coding: utf-8 -*-
"""① 更新 PICKS.fitness 卡片 ② 重写 DETAIL.diet 对齐增肌目标"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

# ================= 1) PICKS.fitness =================
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

new_picks = '''  fitness: [
    {icon:"💪", title:"增肌 + 腹肌 双目标 · 新版周计划", desc:"4力量日+1有氧日 · 新增练腿(原来完全没有) · 跳绳减到1-2次 · 瘦胖子该增肌不该减脂", link:"#", video:"https://www.youtube.com/@JeremyEthier"},
    {icon:"📈", title:"12周渐进超负荷计划", desc:"适应→增肌→强化 · 俯卧撑必须加负重(60个自重已适应) · 每周只推一项(次数或重量)", link:"#", video:"https://www.youtube.com/@athleanx"}
  ],'''

# 定位 PICKS 里的 fitness 数组
m = re.search(r'  fitness: \[[\s\S]*?\n  \],', d)
if m:
    d = d[:m.start()] + new_picks + d[m.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('OK PICKS.fitness 已更新')
else:
    print('MISS PICKS.fitness')

# ================= 2) DETAIL.diet =================
H = []
A = H.append
A('<h2>🍽️ 饮食助手 · 增肌期版</h2>')
A('<p class="detail-subtitle">肾结石·甲状腺结节·增肌食谱 · 训练日约 2500 kcal / 休息日约 2300 kcal</p>')

A('<div class="callout info" style="border-left:4px solid #10b981">'
  '<strong>🔧 相比原方案的调整（因为你要增肌了）</strong><br>'
  '原方案是【轻缺口 2300 kcal】——那是减脂思路。你现在 59kg 偏瘦，'
  '继续缺口只会掉体重、长不出肌肉。<br>'
  '<b>新方案：训练日 2500 kcal（+200 盈余）/ 休息日 2300 kcal（维持）</b>，'
  '蛋白保持 110-130g。这样肌肉能长，脂肪几乎不涨。'
  '</div>')

A('<div class="callout danger"><strong>🪨 肾结石（增肌期更要严格执行）：</strong>'
  '饮水 ≥2.5L/天｜限菠菜/浓茶/巧克力/坚果｜限内脏/啤酒｜低盐 &lt;5g｜适量补钙（别完全不吃）</div>')
A('<div class="callout warn"><strong>🦋 甲状腺结节：</strong>'
  '不需限碘｜十字花科蔬菜必须煮熟｜少辛辣｜每年复查 B 超 + 甲功</div>')

A('<h3>🥗 训练日食谱（~2500 kcal · 约 120g 蛋白质）</h3>')
A('<table class="data-table"><tr><th>时间</th><th>内容</th><th>kcal</th><th>蛋白质</th><th>要点</th></tr>'
  '<tr><td>7:30</td><td>全麦面包 2 片 + 鸡蛋 2 个 + 牛奶 300ml + 香蕉</td><td>600</td><td>32g</td><td>别空腹只喝咖啡</td></tr>'
  '<tr><td>10:00</td><td>希腊酸奶 150g + 蓝莓 + 全麦饼干</td><td>300</td><td>18g</td><td>加餐防中午暴食</td></tr>'
  '<tr><td>12:30</td><td>鸡胸肉 150g + 糙米饭 1.5 碗 + 西兰花焯水 + 胡萝卜</td><td>700</td><td>42g</td><td>主食别省，下午要练</td></tr>'
  '<tr><td>16:30</td><td>香蕉 或 面包 1 片（练前 1 小时）</td><td>150</td><td>3g</td><td>练前补碳水</td></tr>'
  '<tr><td>18:30</td><td>乳清蛋白 1 勺 或 鸡蛋 3 个 + 米饭半碗（练后 30-60min）</td><td>300</td><td>25g</td><td>窗口期恢复</td></tr>'
  '<tr><td>20:00</td><td>清蒸鱼/牛肉 120g + 红薯 + 蔬菜</td><td>450</td><td>30g</td><td>睡前 3 小时吃完</td></tr>'
  '</table>')

A('<h3>🛌 休息日怎么调（约 2300 kcal）</h3>')
A('<table class="data-table"><tr><th>调整项</th><th>怎么做</th></tr>'
  '<tr><td>主食</td><td>减掉 1 碗饭 或 1 份红薯（约 -250 kcal）</td></tr>'
  '<tr><td>练前/练后加餐</td><td>去掉（不训练不需要）</td></tr>'
  '<tr><td>蛋白质</td><td><b>不要减</b>——休息日正是肌肉修复的时候</td></tr>'
  '<tr><td>16:30 加餐</td><td>换成水果或无糖酸奶（不加饼干）</td></tr>'
  '</table>')

A('<h3>📌 增肌期饮食三条铁律</h3>')
A('<div class="ex-list">'
  '<div class="ex-item c1"><span class="ex-n">体重每周涨 0.25-0.5kg</span><span class="ex-s">速度校准</span></div>'
  '<div class="ex-item c2"><span class="ex-n">蛋白 110-130g 一天不能少</span><span class="ex-s">硬指标</span></div>'
  '<div class="ex-item c3"><span class="ex-n">碳水是燃料，别怕吃</span><span class="ex-s">练得动才长</span></div>'
  '</div>')
A('<div class="callout tip">如果一周后体重完全没动 → 每天再加 200 kcal（优先加碳水和蛋白，别加零食）；'
  '如果一周涨超过 0.75kg → 每天减 200 kcal。'
  '<b>调热量只调主食，不要动蛋白质。</b></div>')

A('<h3>🔧 工具</h3><ul>'
  '<li><a href="https://www.boohee.com" target="_blank">薄荷健康</a>（查热量·记录饮食）</li>'
  '<li><a href="https://www.myfitnesspal.com" target="_blank">MyFitnessPal</a>（国际版数据库更全）</li>'
  '<li><a href="https://www.xiachufang.com" target="_blank">下厨房</a>（照做增肌餐）</li></ul>')

html = ''.join(H)
esc = html.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '')
new_line = "DETAIL.diet = '" + esc + "';"

FP2 = BASE + r'\detail_content.js'
c = open(FP2, 'r', encoding='utf-8').read()
i = c.index('DETAIL.diet')
j = c.index('DETAIL["ai-track"]')
old = c[i:j]
c = c[:i] + new_line + '\n\n' + c[j:]
open(FP2, 'w', encoding='utf-8').write(c)
print('OK DETAIL.diet 已重写')
print('  原长度:', len(old), '→ 新长度:', len(new_line))
print('  单行:', new_line.count('\n') == 0, '| 含撇号(应False):', "'" in html)
