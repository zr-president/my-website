# -*- coding: utf-8 -*-
"""PICKS 首页推荐 9/6 状态推进（精确单行替换）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP, 'r', encoding='utf-8').read()
reps = [
 # anime：追番天数 21 -> 25（9/6）
 ('{icon:"🥇", title:"Re:Zero S4 夺还篇 追番第21天 🎬", desc:"最终话9/30定档 · 夺还篇临近完结 · 486认知博弈最高潮 · 9月必追"',
  '{icon:"🥇", title:"Re:Zero S4 夺还篇 追番第25天 🎬", desc:"最终话9/30定档 · 完结倒计时24天 · 486认知博弈最高潮 · 9月必追"'),
 # music：周三 -> 周末
 ('desc:"9月新单曲预告发布 · K-Pop九月回归潮开启 · 周三通勤情绪注入"',
  'desc:"9月新单曲预告发布 · K-Pop九月回归潮第一棒 · 周末通勤情绪注入"'),
 # novel：连载第25天 -> 第29天
 ('{icon:"🔥", title:"天蚕土豆新书连载中 🔥", desc:"8月8日已开载·连载第25天·联动斗破苍穹世界观·玄幻顶流回归。"',
  '{icon:"🔥", title:"天蚕土豆新书连载中 🔥", desc:"8月8日已开载·连载第29天·联动斗破苍穹世界观·玄幻顶流回归。"'),
 # beer：雨势减弱 -> 转晴回温
 ('desc:"雨势减弱后的清爽 · 金酒+汤力水+柠檬 · 9月初解暑"',
  'desc:"秋高气爽前的清爽 · 金酒+汤力水+柠檬 · 周末聚会首选"'),
 # learning：头部换成 GPT-6 Astra
 ('{icon:"🎤", title:"科大讯飞端侧模型开源 🆕", desc:"9/1开源词元星火X2.5端侧模型·手机/车机离线AI·端侧AI国产开源再下一城"',
  '{icon:"🤖", title:"GPT-6 Astra 正式发布 🆕", desc:"9/4发布·总裁称AGI时代到来·从8月安全暂停到放行的大反转·AI安全治理成面试高频题"'),
 ('{icon:"📈", title:"A股9月开局复盘", desc:"9/2沪指收阳十字星·缩量调整·军工连日走强·9月震荡开局"',
  '{icon:"📈", title:"A股9月开局复盘", desc:"9/4沪指-0.30%收3930.12·日K连三黑·农业逆市·周一(9/8)看3930企稳+GPT-6情绪传导"'),
 ('{icon:"📊", title:"AI模型全维度对比表", desc:"智能/性价比/速度/综合百分制评分·端侧模型加入评估·每日刷新"',
  '{icon:"📊", title:"AI模型全维度对比表", desc:"智能/性价比/速度/综合百分制评分·GPT-6闭源不入表·开源阵营仍DeepSeek/Qwen/GLM"'),
 # fitness：周三 -> 周日恢复日
 ('{icon:"💪", title:"周三：肩+腹", desc:"哑铃推举→侧平举→悬垂举腿 · 增肌期第8周 · 渐进加重中"',
  '{icon:"💪", title:"周日：恢复日", desc:"快走30-40分钟+全身拉伸·泡沫轴放松·增肌期第8周收尾·周一胸+三头"'),
 # diet：周三 -> 周末备餐
 ('{icon:"🥗", title:"周三：鸡胸肉+糙米饭", desc:"650kcal · 42g蛋白质 · 增肌期热量盈余跟上 · 备餐照旧"',
  '{icon:"🥗", title:"周末：卤鸡胸肉备餐", desc:"650kcal/份 · 42g蛋白质 · 分装冷冻管一周 · 增肌热量盈余跟上"'),
 # career：周三 -> 周一黄金窗口
 ('{icon:"🎯", title:"周三黄金投递窗口 🔥", desc:"9:30-11:00回复率最高 · 金九银十招聘季·今天就是窗口"',
  '{icon:"🎯", title:"周一(9/8)黄金投递窗口 🔥", desc:"9:30-11:00回复率最高 · 周末写GPT-6行业观察+复盘投递 · 周一集中出手"'),
 ('{icon:"🎤", title:"端侧AI/语音AI岗位 🆕", desc:"科大讯飞开源端侧模型→语音AI/端侧应用人才需求上升·求职新方向"',
  '{icon:"🛡️", title:"AI安全/AI治理岗位 🆕", desc:"GPT-6 Astra事件→安全评估/红队测试/关键资安能力成岗位关键词·新增量方向"'),
 ('{icon:"📝", title:"作品集升级", desc:"用科大讯飞端侧开源+Anthropic算力大单写300字AI行业观察 · 面试加分"',
  '{icon:"📝", title:"作品集升级", desc:"用GPT-6 Astra发布写300字行业观察《AI安全与能力如何平衡》 · 面试加分"'),
 # movie：奥德赛天数含糊处理（保留但不写错天数）
 ('{icon:"🏛️", title:"奥德赛 热映第19天", desc:"8.14上映·诺兰IMAX巨制·荷马史诗改编·暑期档尾巴仍在热映"',
  '{icon:"🏛️", title:"奥德赛 IMAX热映中", desc:"8.14上映·诺兰IMAX巨制·荷马史诗改编·史诗长尾仍在"'),
 # life-tips：台风沙德尔 -> 杜鹃或将生成
 ('{icon:"⛈️", title:"台风沙德尔影响减弱", desc:"雨势逐步减弱·广东局部仍有暴雨大暴雨·出行带伞·新台风消息跟进"',
  '{icon:"⛅", title:"秋高气爽+新台风杜鹃或将生成", desc:"科罗旺已远离·广州多云到晴33C/25C·昼夜温差渐大·杜鹃路径待观察"'),
 # ai-track：头部换成 GPT-6 Astra
 ('{icon:"🎤", title:"科大讯飞端侧模型开源 🆕", desc:"9/1开源词元星火X2.5端侧模型·手机/车机离线AI·端侧AI国产开源新军"',
  '{icon:"🤖", title:"GPT-6 Astra 正式发布 🆕", desc:"9/4发布·总裁称AGI时代到来·曾因网络安全风险暂停一个月·AI安全vs能力释放成焦点"'),
 ('{icon:"🏦", title:"Anthropic 350亿算力协议 🆕", desc:"与Nvidia投资Lambda·AI算力军备竞赛升级·算力产业链确定性增强"',
  '{icon:"🏦", title:"国家AI基金注资可灵14亿 🆕", desc:"AI视频生成国家队入场·阿里更新Qwen3.8-Max·Manus恢复独立·国产AI资本产品双热"'),
]
n = 0
for old, new in reps:
    if old in c:
        c = c.replace(old, new, 1); n += 1
    else:
        print('NOT FOUND:', old[:70])
open(FP, 'w', encoding='utf-8').write(c)
print('replaced', n, '/', len(reps))
