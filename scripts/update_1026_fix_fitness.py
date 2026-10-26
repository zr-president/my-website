# -*- coding: utf-8 -*-
"""修正 INSIGHTS.fitness：与 DETAIL.fitness 的真实周计划对齐

真实周计划（DETAIL.fitness）：
  周一 → 拉   周二 → 下肢 + 后链   周三 → 休息
  周四 → 推   周五 → 核心 + 弱项补   周六/日 → 休息

我第一次写的「拉类周一/周五各一次」是错的（周五其实是核心+弱项补），
一致性检查里的「下肢训练日两处不一致」也由此暴露。
"""
import io, sys, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _insight_helper import make_patcher

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DP = os.path.join(P, 'daily_data.js')
apply = make_patcher(DP)

C = {'fitness': {
'summary': '''<b>10月26日（周一）改版第 9 天 · 第一周最后一天</b><br><br>10/20 定的「只做三件事」到今天满一周。体脂 <b>12-14%</b>、体重 <b>60.65kg</b>、BMI 21.0 没变——<b>一周体重不变是正常的</b>，增肌的真实反馈要 3-4 周才看得出来。<br><br>这周的实际排法是：<b>周一拉 / 周二下肢 + 后链 / 周四推 / 周五核心 + 弱项补</b>，周三和周末休息。第一周真正要检验的是：<b>拉和下肢这两次有没有真的做</b>——它们一个管背肩宽度，一个管整体骨架，是偏瘦体型最缺的两块。''',
'trend': '''<b>第一周复盘：只问三个问题</b><br><br><b>① 周一（拉）和周二（下肢）做了吗？</b>这两次是本周的核心。做到 → 计划成立；只做了其中一次 → 差在固定时间点；两次都没做 → 动作本身有障碍（桌子不合适 / 没地方深蹲），<b>要先换动作而不是加意志力</b>。<br><b>② 下肢加了之后有没有过痛？</b>深蹲和单腿硬拉对膝和腰的要求高。<b>做完第二天如果膝前侧或腰有持续酸痛（不是肌肉酸，是关节痛），先退回到自重或减少幅度</b>。偏瘦增肌最怕的不是练得少，是练伤停两个月。<br><b>③ 每次做到目标次数了吗？</b>桌下反向划船 8-12 次、深蹲 8-12 次、臀桥 15-20 次。做不到下限就降难度（屈膝 / 自重 / 扶墙），<b>降难度保次数，别硬上</b>。''',
'tip': '''<b>10/26（周一）第一周收尾，做一次 3 问复盘（5 分钟）</b><br>① <b>周一拉、周二下肢，这两次做了吗</b>？两次都没做说明动作有障碍，要换动作不是加意志力<br>② <b>下肢后有没有关节痛</b>？膝前侧/腰的持续酸痛（不是肌肉酸）就退回自重或减幅度<br>③ <b>次数做到下限了吗</b>？划船 8-12、深蹲 8-12、臀桥 15-20。做不到就降难度保次数<br><b>下周排法不变</b>：周一拉 / 周二下肢+后链 / 周四推 / 周五核心+弱项补 —— <b>先别加新动作</b>，第一周都没稳定，加动作只会更乱。'''
}}

n = apply(C)
print('✅ INSIGHTS.fitness 已重写：%d 个字段' % n)

r = subprocess.run(['node', '--check', DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('语法：' + ('OK' if r.returncode == 0 else 'FAIL ' + (r.stderr or '')[:300]))

# 确认两处都含下肢 + 三字段含当日日期
probe = r'''
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const d=fs.readFileSync('detail_content.js','utf8');
const ctx={};vm.createContext(ctx);vm.runInContext(d,ctx);
const fit=c.INSIGHTS.fitness;
console.log('  INSIGHTS.fitness 含下肢: '+fit.summary.includes('下肢')||fit.trend.includes('下肢')||fit.tip.includes('下肢'));
console.log('  DETAIL.fitness 含下肢: '+(ctx.DETAIL.fitness||'').includes('下肢'));
console.log('  三字段含 10/26: '+[/10月26日|10\/26/.test(fit.summary),/10月26日|10\/26/.test(fit.trend),/10月26日|10\/26/.test(fit.tip)].join(','));
'''
pp = os.path.join(P, '_fv.js'); open(pp, 'w', encoding='utf-8').write(probe)
r2 = subprocess.run(['node', pp], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r2.stdout or r2.stderr)
os.remove(pp)
