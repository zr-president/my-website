# -*- coding: utf-8 -*-
"""统一食谱口径：建立唯一权威版（放饮食区），健身区改为精简要点 + 指向饮食区
   并让营养数字自洽：训练日 2500 kcal / 蛋白约 130g；休息日约 2300 kcal
"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

# ============ 唯一权威食谱（训练日）============
# 核算：550+200+680+120+280+670 = 2500 kcal ；蛋白 28+12+38+4+25+24 = 131g
MEALS = [
    ("07:30", "早餐", "全麦面包 2 片 + 鸡蛋 2 个 + 牛奶 300ml", "550", "28g", "别空腹只喝咖啡"),
    ("10:30", "加餐", "无糖希腊酸奶 100g + 香蕉 1 根", "200", "12g", "防中午暴食"),
    ("12:30", "午餐", "鸡胸肉 100g + 糙米饭 1.5 碗 + 焯水西兰花 + 胡萝卜 + 1 勺油", "680", "38g", "主食别省，下午要练"),
    ("16:30", "练前", "全麦面包 1 片（练前 1 小时）", "120", "4g", "练前补碳水"),
    ("18:30", "练后", "乳清蛋白 1 勺 + 香蕉 1 根（练后 30-60 分钟）", "280", "25g", "窗口期恢复"),
    ("20:00", "晚餐", "清蒸鱼 100g + 红薯 200g + 半碗杂粮饭 + 蔬菜 + 1 勺油", "670", "24g", "睡前 3 小时吃完"),
]

# ============ 1) 重写 DETAIL.diet ============
H = []
A = H.append
A('<h2>🍽️ 饮食助手 · 增肌期版</h2>')
A('<p class="detail-subtitle">肾结石·甲状腺结节·增肌食谱 · 训练日 2500 kcal / 休息日 2300 kcal · 蛋白 110-130g</p>')

A('<div class="callout info" style="border-left:4px solid #10b981">'
  '<strong>📌 这里是全站唯一的权威食谱</strong>　健身区只给【饮食要点】，'
  '具体吃什么、吃多少以本页为准 —— 两处内容保持一致，不会出现两套食谱。<br><br>'
  '<strong>为什么是这套数字</strong>：你 170cm/59kg、体脂 15-18%，增肌期需要轻微热量盈余。'
  '训练日 2500 kcal（比维持多约 200）、休息日 2300 kcal（维持）；'
  '蛋白按 1.9-2.2g/kg 取 <b>110-130g</b>（本食谱实际约 130g），'
  '碳水训练日 50-55%、脂肪 25-30%。'
  '</div>')

A('<div class="callout danger"><strong>🪨 肾结石（增肌期更要严格执行）：</strong>'
  '饮水 ≥2.5L/天｜限菠菜/浓茶/巧克力/坚果｜限内脏/啤酒｜低盐 &lt;5g｜适量补钙（别完全不吃）</div>')
A('<div class="callout warn"><strong>🦋 甲状腺结节：</strong>'
  '不需限碘｜十字花科蔬菜必须煮熟｜少辛辣｜每年复查 B 超 + 甲功</div>')

A('<h3>🥗 训练日食谱（合计 2500 kcal · 蛋白约 130g）</h3>')
A('<table class="data-table"><tr><th>时间</th><th>餐次</th><th>内容</th><th>kcal</th><th>蛋白</th><th>要点</th></tr>')
for t, name, food, kcal, pro, tip in MEALS:
    A('<tr><td>' + t + '</td><td><b>' + name + '</b></td><td>' + food + '</td>'
      '<td>' + kcal + '</td><td>' + pro + '</td><td>' + tip + '</td></tr>')
A('<tr style="background:var(--accent-light)"><td colspan="3"><strong>合计</strong></td>'
  '<td><strong>2500</strong></td><td><strong>约 130g</strong></td><td>达标</td></tr>')
A('</table>')

A('<h3>🛌 休息日怎么调（约 2300 kcal）</h3>')
A('<table class="data-table"><tr><th>调整项</th><th>具体怎么做</th><th>热量变化</th></tr>'
  '<tr><td>去掉练前加餐</td><td>不训练就不需要练前补碳</td><td>-120</td></tr>'
  '<tr><td>去掉练后加餐</td><td>乳清蛋白挪到早餐或加餐里（蛋白总量不变）</td><td>-280</td></tr>'
  '<tr><td>午餐/晚餐各加半碗主食</td><td>糙米饭、红薯各加半份</td><td>+200</td></tr>'
  '<tr style="background:var(--accent-light)"><td colspan="2"><strong>休息日合计</strong></td>'
  '<td><strong>约 2300 kcal</strong></td></tr>'
  '</table>')
A('<div class="callout info"><strong>注意：休息日蛋白质不要减</strong> —— '
  '休息日正是肌肉修复的时间。做法是把练后那勺乳清蛋白挪到早餐或上午加餐，'
  '总蛋白仍保持约 130g。</div>')

A('<h3>📌 增肌期饮食三条铁律</h3>')
A('<div class="ex-list">'
  '<div class="ex-item c1"><span class="ex-n">体重每周涨 0.25-0.5kg</span><span class="ex-s">速度校准</span></div>'
  '<div class="ex-item c2"><span class="ex-n">蛋白 110-130g 一天不能少</span><span class="ex-s">硬指标</span></div>'
  '<div class="ex-item c3"><span class="ex-n">碳水是燃料，别怕吃</span><span class="ex-s">练得动才长</span></div>'
  '</div>')
A('<div class="callout tip">如果一周后体重完全没动 → 每天再加 200 kcal（优先加碳水和蛋白）；'
  '如果一周涨超过 0.75kg → 每天减 200 kcal。'
  '<b>调热量只调主食，不要动蛋白质。</b></div>')

A('<h3>🔧 工具</h3><ul>'
  '<li><a href="https://www.boohee.com" target="_blank">薄荷健康</a>（查热量·记录饮食）</li>'
  '<li><a href="https://www.myfitnesspal.com" target="_blank">MyFitnessPal</a>（国际版数据库更全）</li>'
  '<li><a href="https://www.xiachufang.com" target="_blank">下厨房</a>（照做增肌餐）</li></ul>')

diet_html = ''.join(H)
diet_esc = diet_html.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '')

FP2 = BASE + r'\detail_content.js'
c = open(FP2, 'r', encoding='utf-8').read()
i = c.index('DETAIL.diet')
j = c.index('DETAIL["ai-track"]')
c = c[:i] + "DETAIL.diet = '" + diet_esc + "';\n\n" + c[j:]
open(FP2, 'w', encoding='utf-8').write(c)
print('OK DETAIL.diet 已重写（唯一权威食谱，合计 2500 kcal / 130g）')

# ============ 2) 健身区：删掉重复食谱表，改为精简要点 ============
c = open(FP2, 'r', encoding='utf-8').read()
m = re.search(r"<h4 style=\"font-size:12px;margin:14px 0 6px\">一天怎么吃[\s\S]*?</table>", c)
if m:
    compact = (
        '<div class="callout info"><strong>🍽️ 具体吃什么 → 见【饮食助手】页（全站唯一权威食谱）</strong><br>'
        '健身区不重复列菜单，避免两处不一致。这里只给<b>要点</b>：<br>'
        '· <b>训练日 2500 kcal</b>（比维持多约 200）｜ <b>休息日 2300 kcal</b>（维持）<br>'
        '· <b>蛋白 110-130g/天</b>（约 1.9-2.2g/kg）｜ 碳水训练日 50-55% ｜ 脂肪 25-30%<br>'
        '· <b>练后 30-60 分钟内</b>补蛋白 + 快碳（乳清蛋白 1 勺 + 香蕉最省事）<br>'
        '· 调热量只调主食，<b>不要动蛋白质</b>；每天饮水 ≥2.5L（结石预防）'
        '</div>'
    )
    c = c[:m.start()] + compact + c[m.end():]
    open(FP2, 'w', encoding='utf-8').write(c)
    print('OK 健身区重复食谱表 → 已改为精简要点 + 指向饮食区')
else:
    print('MISS 健身区食谱表')

# ============ 3) INSIGHTS.diet 与权威食谱对齐 ============
FP3 = BASE + r'\daily_data.js'
d = open(FP3, 'r', encoding='utf-8').read()

diet_ins = {
 "summary": "9月中（转晴回温）饮食主线：【增肌热量盈余 + 高蛋白 + 补水防结石】三位一体。热量按增肌期设定为 <b>训练日 2500 / 休息日 2300 kcal</b>——59kg 的人靠热量缺口长不出肌肉，必须有轻微盈余（训练日比维持多约 200）。蛋白按 1.9-2.2g/kg 取 <b>110-130g</b>（食谱实际约 130g），碳水训练日 50-55%、脂肪 25-30%。<b>完整食谱以饮食助手页为准</b>，健身区只给要点，两处数字一致。肾结石预防照旧：饮水 ≥2.5L/天、控草酸、限盐 &lt;5g、适量补钙。",
 "trend": "增肌期饮食的三条要点：(1)<b>先看体重校准热量</b>——每周涨 0.25-0.5kg 说明合适；完全不涨就每天再加 200 kcal；涨超过 0.75kg 就减 200 kcal，调热量只调主食不动蛋白；(2)<b>蛋白分散到 4-6 餐</b>比一顿猛吃吸收更好，练后 30-60 分钟内补蛋白 + 快碳；(3)<b>碳水不是敌人</b>——它是训练燃料，增肌期把碳水压太低会练不动、恢复慢，反而拖累增肌。",
 "tip": "🥗 训练日怎么吃（合计 2500 kcal / 蛋白约 130g，完整版见饮食助手页）：\\n07:30 全麦面包2片+鸡蛋2个+牛奶300ml（550/28g）\\n10:30 无糖希腊酸奶100g+香蕉1根（200/12g）\\n12:30 鸡胸肉100g+糙米饭1.5碗+焯水西兰花+胡萝卜+1勺油（680/38g）\\n16:30 全麦面包1片·练前1小时（120/4g）\\n18:30 乳清蛋白1勺+香蕉·练后30-60min（280/25g）\\n20:00 清蒸鱼100g+红薯200g+半碗杂粮饭+蔬菜+1勺油（670/24g）\\n\\n🛌 休息日约 2300 kcal：去掉练前与练后加餐（-400），午晚餐各加半碗主食（+200）；<b>蛋白质不要减</b>——把练后那勺乳清蛋白挪到早餐即可。\\n\\n🪨 结石预防：每天 ≥2.5L 水；少菠菜/苋菜/浓茶/巧克力；限盐 <5g；吃高草酸食物配奶制品同餐。",
 "updated": "2026-09-13"
}
pat = re.compile(r"\n  diet: \{[\s\S]*?\n  \},")
m2 = pat.search(d)
if m2:
    js = '\n  diet: ' + json.dumps(diet_ins, ensure_ascii=False, indent=2).replace('\n', '\n  ') + ','
    d = d[:m2.start()] + js + d[m2.end():]
    open(FP3, 'w', encoding='utf-8').write(d)
    print('OK INSIGHTS.diet 已与权威食谱对齐')
else:
    print('MISS INSIGHTS.diet')
