# -*- coding: utf-8 -*-
"""修正 LEARN_PATHS：旧 items 归档为 2026-09-12，items 换成 9/13 的 10 条"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


learn_items = [
 {"section":"健身","emoji":"🧍","title":"瘦胖子是什么？为什么体脂率会被【肌肉少】推高？","content":"同样 59kg，肌肉多的人体脂率可以只有 10%，肌肉少的人却会到 16%——因为体脂率 = 脂肪 ÷ 体重，而肌肉也是体重的一部分。瘦胖子的体重正常，但瘦体重偏低，于是脂肪占比被动升高。所以问题不是【脂肪太多要减】，而是【肌肉太少要加】。","takeaway":"体脂率是个比值。可以通过降分子（减脂）改善，也可以通过升分母（增肌）改善——瘦胖子应该选后者。"},
 {"section":"健身","emoji":"🔁","title":"为什么减脂和增肌很难同时做？","content":"减脂需要热量缺口，增肌需要热量盈余，两者能量方向相反。能做到【重组】的前提是：训练新手、体脂中等、蛋白质充足、睡眠足够。满足这些条件时身体会优先用脂肪供能、用食物蛋白合成肌肉，效果慢但真实存在。","takeaway":"重组适合新手与瘦胖子；训练 2 年以上、体脂又低的人，最好分增肌期与减脂期来做。"},
 {"section":"健身","emoji":"📈","title":"渐进超负荷：增肌唯一必需的变量","content":"肌肉增长的信号是【机械张力】——肌肉必须在超出以往的水平下发力。如果重量、次数、节奏长期不变，身体就没有理由继续长肌肉，只会提高神经效率与耐力。所以同样一组动作，必须持续加重量、加次数或加难度。","takeaway":"判断训练有没有效，先问一句：这周的负重或次数比上周多了吗？没有就是在原地踏步。"},
 {"section":"健身","emoji":"⏸️","title":"为什么自重训练会【失效】？适应原理","content":"身体对重复刺激会产生适应：同样的俯卧撑做到第 4 周，神经与肌肉都已习惯，此后每组做得再多也只是提升耐力。这就是为什么能一口气做 60 个俯卧撑的人，胸肌往往并不大。","takeaway":"自重不是不能增肌，而是必须不断升级难度（负重、单侧、慢离心、爆发）才能维持刺激。"},
 {"section":"健身","emoji":"🦵","title":"练腿为什么能提升全身增肌效率？","content":"腿部肌群体量占全身一半以上，大重量深蹲等复合动作会带来更强的全身性激素与代谢反应，同时显著提高整体训练容量。不练腿的另一后果是体型失衡：上身壮、下身细，视觉上并不好看。","takeaway":"想增肌却不练腿，等于只用一半的引擎——效率与观感都会打折。"},
 {"section":"健身","emoji":"⚖️","title":"干扰效应：为什么有氧做多了影响增肌？","content":"有氧与力量训练争夺同一批恢复资源（糖原、氨基酸、恢复时间），并且有氧会激活 AMPK 通路、抑制肌肉合成的 mTOR 通路。每周 1-2 次中等强度有氧影响不大，但 4 次以上高强度有氧 + 热量缺口，增肌基本停滞。","takeaway":"增肌期有氧要【够用就好】：控心肺与体脂靠 1-2 次，不要当主力练。"},
 {"section":"营养","emoji":"🔥","title":"热量盈余该加多少？lean bulk 的 +200 逻辑","content":"肌肉合成速度有上限：新手每月约 1-2kg，训练久了更低。盈余太大，多出来的热量只能变成脂肪。每天 +200 kcal 左右（每周增重 0.25-0.5kg）是兼顾增肌与控脂的常用区间。","takeaway":"增肌速度慢不是失败，是生理上限。追求每周涨 1kg 的人，涨的大部分是脂肪。"},
 {"section":"营养","emoji":"🥩","title":"蛋白质 1.6-2.2g/kg 这个区间是怎么来的？","content":"多项剂量-反应研究显示：增肌期蛋白质摄入从 1.6g/kg 起收益明显，到 2.2g/kg 左右趋于平台，再往上没有额外增肌收益。区间下限对应维持，上限对应热量缺口较大或训练量很高的情况。","takeaway":"59kg 的你，110-130g 就够了。把蛋白分散到 4-6 餐比一顿猛吃吸收更好。"},
 {"section":"健身","emoji":"🧪","title":"身体重组适合谁？怎么判断自己在不在状态","content":"适合：训练新手、体脂 15-25% 的男性、长期节食后代谢偏低者、以及【体重正常但肌肉少】的瘦胖子。判断依据：训练是否持续加重、蛋白是否达标、睡眠是否 ≥7 小时、体重是否缓慢上升或持平但围度改善。","takeaway":"重组不是玄学，它有明确适用人群与可验证指标——围度与力量，而不是体重秤。"},
 {"section":"健身","emoji":"📏","title":"为什么增肌期【看围度不看体重】？","content":"增肌期体重上涨是必然的：除了肌肉，还有糖原与结合水（每 1g 糖原约带 3g 水）。所以头几周体重快速上涨大多是水分，而真实进步体现在腰围不变、胸围与大腿增加、同重量能多做几次。","takeaway":"只看体重会误判为【变胖】从而错误减量，最后既没长肌肉也没瘦——这是增肌期最常见的自我破坏。"}
]

lm = re.search(r'var LEARN_PATHS = \{([\s\S]*?)\n\};', d)
if not lm:
    print('MISS LEARN_PATHS'); sys.exit(1)
body = lm.group(1)

im = re.search(r'items:\s*\[([\s\S]*?)\n  \],', body)
am = re.search(r'archive:\s*\{([\s\S]*)\}\s*$', body)
if not (im and am):
    print('MISS items/archive:', bool(im), bool(am)); sys.exit(1)

old_items = im.group(1).strip()
old_archive = am.group(1).strip()
# 去掉 archive 末尾多余逗号
old_archive = re.sub(r',\s*$', '', old_archive)

new_body = ('\n  updated: "2026-09-13",\n  current_day: 8,           // 当前学到第几天\n'
            '  items: ' + j(learn_items) + ',\n'
            '  // 历史累积库：archive 只存【历史】日期（当天内容放 items，不进 archive）\n'
            '  archive: {\n'
            '    "2026-09-12": [\n' + old_items + '\n    ]'
            + (',\n' + old_archive if old_archive else '') + '\n  }\n')

d = d[:lm.start()] + 'var LEARN_PATHS = {' + new_body + '};' + d[lm.end():]
open(FP, 'w', encoding='utf-8').write(d)
print('OK LEARN_PATHS 已更新')
