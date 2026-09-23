# -*- coding: utf-8 -*-
"""网站更新收尾：WEBSITE_GUIDE 摘要 + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.17。9/23（周三）更新：AI动态追踪改为 Jev 专题——TypeSafe 9/15 发布的首个【System One Model】，'
       '不生成文字只输出判断与概率，实测准确率并不突出（64-65%）但速度成本优势明显（0.73秒/题·50题0.002美元）；'
       '并拆解两个易被误读的宣传点（零幻觉只保证输出结构、概率输出在阈值附近仍会波动）。'
       '每日一词与小白课堂全量刷新为 8/7 个领域；健身进入增肌第2周；A股 3900 关口进入第二周争夺。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-09-23（周三 · v1.8.17）Jev 决策模型专题
- **读取系统时钟**确认为 2026-09-23，站点原内容 9/19 → 落后 4 天，内容实质刷新
- **AI 动态追踪重写为 Jev 专题**：TypeSafe 9/15 发布的首个【System One Model】
  - 用法：给 state + 预声明答案类型的 questions → 直接返回选择/评分/真假 + 概率，不生成文字
  - 与 LLM 的四个区别：输出形态 / 服务对象 / 速度成本 / 准确率并不占优
  - 实测数据：准确率 64-65%（便宜小模型组第二），0.73 秒/题，50 题 0.002 美元
  - 两个易被误读的宣传点：「零幻觉」只保证输出结构不保证判断正确；概率输出在阈值附近仍会波动（1.99 vs 2.00）
- **今日要闻 8 卡**：3 张 Jev（发布/实测/技术理解）+ 求职素材 + A股周中 + 健身第2周 + 动漫倒计时 + 秋分生活
- **每日一词 10 条 / 8 领域**：System One Model、概率校准、模型路由、阈值陷阱、训练容量、结构性行情、
  转化漏斗、机会成本、昼夜节律、技术理解深度
- **小白课堂 10 条 / 7 领域**：含 4 条 Jev/产品（Jev 是什么 / 零幻觉真相 / 阈值陷阱 / 模型路由）；
  旧 10 条归档为 2026-09-19；current_day 13 → 17
- **今日待办 5 条**：把 Jev 写成 300 字行业观察（面试素材）/ 增肌第2周加重 / 称重校准 / 补训练平台 / A股周中复盘
- **news 分区**更新为 9/23 资讯（Jev 持续发酵、A股结构市、求职考核重心转移）
- **修正内容过时**：stock 分区的「下周（9/21起）预案」已过期 → 改本周口径；ai-track 补当日框架
- 内容新鲜度：17 个分区全部不落后；一致性检查 22 项通过
- 版本 1.8.16 → 1.8.17

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

p = os.path.join(BASE, 'daily_data.js.bak')
if os.path.exists(p):
    os.remove(p); print('已删除备份')
