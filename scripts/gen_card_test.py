# -*- coding: utf-8 -*-
"""生成测试页：在 index.html 的 <head> 后注入 localStorage 种子数据（同源）"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
h = open(BASE + r'\index.html', 'r', encoding='utf-8').read()

summary = {
    "updated": "2026-09-12", "v": 1, "done": 23, "total": 56, "pct": 41,
    "mods": {
        "sql": {"name": "SQL 训练场", "done": 12, "total": 20, "pct": 60, "extra": {"mastery": 58, "runs": 31}},
        "lab": {"name": "数据集实验室", "done": 3, "total": 8, "pct": 38},
        "metrics": {"name": "指标设计工坊", "done": 4, "total": 6, "pct": 67},
        "abtest": {"name": "实验分析训练", "done": 2, "total": 6, "pct": 33},
        "case": {"name": "Case 拆解训练", "done": 1, "total": 5, "pct": 20},
        "agent": {"name": "AI Agent 实操", "done": 1, "total": 9, "pct": 11}
    },
    "radar": {"rated": 9, "total": 9, "sum": 26, "target": 37, "pct": 70}
}
seed = ("<style>#zhHero,#zhBattlePlan,#featuredCard,#dailyBriefing,#dashboard,#daily-vocab,#homeCategoryGrid,#schedulePanel,#dailyDecisions,#learnPathBox{display:none!important}</style>"
        + "<script>try{localStorage.setItem('tp_summary_v1'," + json.dumps(json.dumps(summary, ensure_ascii=False)) + ");}catch(e){}</script>")

i = h.find('<head>')
if i < 0:
    print('MISS head'); sys.exit(1)
out = h[:i + 6] + '\n' + seed + h[i + 6:]
open(BASE + r'\_t_card.html', 'w', encoding='utf-8').write(out)
print('OK 已生成 _t_card.html')
