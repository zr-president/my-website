# -*- coding: utf-8 -*-
"""收尾：WEBSITE_GUIDE + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.20。10/1（周四 · 国庆节）更新：主题从【节前准备】切换为【假期执行】——'
       'A股 10/1-10/7 休市、10/8 开市，stock 分区重写为 9 月月度复盘 + 10 月三个观察点（量能/3900/主线）'
       '与假期跳空风险的应对；ai-track 沉淀为两份产品分析的写作框架（DSH 桌面端取舍 / Jev 接入边界）；'
       '健身进入第3周并给出假期最低训练量；给出假期三条边界（训练15分钟 / 作息浮动≤1小时 / 学习40分钟）。'
       '每日一词与小白课堂各刷新为 10 个领域。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-10-01（周四 · 国庆节 · v1.8.20）假期第 1 天：从"节前准备"到"假期执行"
- **读取系统时钟**确认为 2026-10-01（周四 · 国庆节），站点原内容 9/27 → 落后 4 天，内容实质刷新
- **今日要闻 8 卡**：国庆节假期三条边界 · A股 10/1-10/7 休市（10/8 开市）·
  增肌第3周与假期最低训练量 · Re:Zero 最终话已播（9/30）· 求职（假期做材料/节后投递）·
  假期学习最低维持量 · 健康作息（只守起床时间）· AI 两条线沉淀
- **stock 分区重写**：9 月月度复盘（指数震荡 + 结构分化 + 存量博弈 1.8-2 万亿）+
  10 月三个观察点表（量能能否站上 2.2 万亿 / 3900 能否有效站稳 / AI 硬件主线是否延续）+
  假期跳空风险的应对逻辑；tip 给出假期复盘五步法（区分【判断对且逻辑成立】与【靠运气】）
- **ai-track 分区重写**：沉淀为两份产品分析的写作框架 ——
  ① DSH 桌面端 vs 网页版（9 行对比表 + PTC 技术点）
  ② Jev 决策模型（System One Model / 实测数据 / 两个易误读宣传点）；
  强调【改变结论的条件】才是产品分析的核心；reasoning 说明为何理解价值 > 使用价值
- **每日一词 10 条 / 10 领域**：推理成本 · 冷启动 · 留存曲线 · 训练容量 · 跳空缺口 ·
  STAR法则 · 复利 · 主动回忆 · 社交时差 · A/B测试
- **小白课堂 10 条 / 10 领域**：推理成本为何不能都用大模型 / 冷启动 /
  留存曲线看平在哪 / 训练容量加什么 / 跳空缺口与节前定仓位 / STAR法则 /
  复利（时间的杠杆 > 收益率的杠杆）/ 主动回忆 / 社交时差 / A/B测试指标选错；
  旧 10 条归档为 2026-09-27；current_day 22 → 23
- **今日待办 5 条**：假期三条边界 / 增肌假期第1练 / 学习最低量跑通 /
  DSH+Jev 写成产品文档 / A股假期复盘
- **修正内容过时**：stock 与 ai-track 原停在 9/27，已真正重写（非仅改日期）
- 内容新鲜度：17 个分区全部不落后；一致性检查 22 项通过
- 版本 1.8.19 → 1.8.20

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

p = os.path.join(BASE, 'daily_data.js.bak')
if os.path.exists(p):
    os.remove(p); print('已删除备份')
