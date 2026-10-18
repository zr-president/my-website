# -*- coding: utf-8 -*-
"""收尾：WEBSITE_GUIDE + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.22。10/18（周日）更新：主题为【10 月过半的复盘窗口 —— 从跟踪转向验证】——'
       'A股 10/8 开市至今 7 个交易日，stock 区把国庆前定下的三个观察点（量能/3900/AI硬件主线）转为可打勾的验证清单，'
       '并提示 10 月下旬三季报密集披露；健身进入第 30 天/第 5 周，给出首次减载评估的三个指标；'
       '求职转入反馈期，用反馈率区分【简历问题】与【面试问题】；另有秋季新番三集法则、入秋穿搭与精酿选择、'
       '影视与楼市 10 月下旬节奏。17 个分区内容全部重写。每日一词与小白课堂各 10 个领域。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-10-18（周日 · v1.8.22）10 月过半的复盘窗口：从「跟踪」转向「验证」
- **读取系统时钟**确认为 2026-10-18（周日），站点原内容 10/7 → 落后 11 天，内容实质刷新
- **17 个 INSIGHTS 分区全部重写**（非仅改日期）：
  - **stock**：10/8 开市至今 7 个交易日，把国庆前定的三个观察点转为验证清单
    （量能能否站上 2.2 万亿 / 3900 收盘站稳+回踩不破 / AI 硬件相对强度），
    并提示 10 月下旬三季报密集披露是结构主线的试金石
  - **fitness**：增肌第 30 天 / 第 5 周，首次【减载评估】三个指标
    （体重 0.25-0.5kg/周、容量是否仍上升、睡眠 ≥7h）
  - **diet**：增肌第 5 周热量与蛋白口径，强调用【体重增长速率】判断盈余是否过头
  - **career**：秋招转入反馈期，用反馈率区分【简历问题】与【面试问题】
  - **anime**：秋季新番第 3 周，三集法则定档追番名单
  - **music / novel / learning / beer / fashion / house / life-tips / movie / ai-track / news**：
    全部换成 10 月中下旬的时间坐标与内容
- **今日要闻 8 卡**：A股复盘验证 · 增肌减载评估 · 秋招反馈率 · 新番三集法则 ·
  10 月计划复盘 · 广州入秋穿搭 · AI 转两周复盘 · 影之刃零倒计时 11 天
- **每日一词 10 条 / 10 领域**：幻觉 · 缓存 · 北极星指标 · 减载周 · 三季报 ·
  反馈率 · 资产配置 · 刻意练习 · 秋燥 · 用户故事
- **小白课堂 10 条 / 10 领域**：幻觉为何会编 / 缓存与一致性 / 北极星只能有一个 /
  减载周为何能继续进步 / 三季报与分化 / 反馈率区分问题环节 / 比例比选品重要 /
  刻意练习的边界 / 秋燥是看不见的蒸发 / 用户故事的【以便】；
  旧 10 条归档为 2026-10-07；current_day 24 → 25
- **今日待办 5 条**：三个观察点打勾 / 第 5 周减载评估 / 统计反馈率 / 学习计划复盘 / 追番定档
- **口径统一**：diet 补入 59kg 体重口径，与 fitness 保持一致
- 内容新鲜度：17 个分区全部不落后；一致性检查 22 项通过（0 提醒）
- 版本 1.8.21 → 1.8.22

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

p = os.path.join(BASE, 'daily_data.js.bak')
if os.path.exists(p):
    os.remove(p); print('已删除备份')
