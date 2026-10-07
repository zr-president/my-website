# -*- coding: utf-8 -*-
"""刷新 fitness 与 ai-track 到 2026-10-07（假期收官 + 明日开市/恢复）"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
TODAY = '2026-10-07'
d = open(FP, 'r', encoding='utf-8').read()


def js(o):
    return json.dumps(o, ensure_ascii=False)


# ---- 先取出原有内容（保留有价值的计划表/对比表）----
NODE = r"""
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const o={};
['fitness','ai-track'].forEach(k=>{const s=c.INSIGHTS[k];o[k]={verdict:s.verdict||'',summary:s.summary||'',trend:s.trend||'',tip:s.tip||'',reasoning:s.reasoning||''};});
console.log(JSON.stringify(o));
"""
r = subprocess.run(['node', '-e', NODE], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
old = json.loads(r.stdout.strip().splitlines()[-1])

# ==================== fitness ====================
fit_summary = ("🎯 <b>假期收官（10/7 更新）</b>｜10/7 是国庆假期最后一天，增肌计划第 3 周同步收官，<b>明日 10/8 恢复正式训练</b>。<br><br>"
  "回顾这次假期的训练目标：不是进步，而是<b>不断</b>。七天里只要守住了【每天最低 15 分钟自重（俯卧撑/深蹲/卷腹/平板支撑）】，"
  "肌肉的能力回落就非常有限，回健身房不需要从头开始。<b>连续性本身就是假期最重要的训练成果</b>。<br><br>"
  "背景不变：170cm/59kg、体脂约 15-18%，属典型【瘦胖子】——体脂偏高不是因为脂肪太多，而是<b>肌肉太少</b>"
  "（59kg 的人脂肪约 9.4kg，瘦体重仅 49.6kg）。所以策略是 <b>lean bulk（增肌为主 + 严格控脂）</b>，"
  "而不是继续减脂（减到 55kg 会显得更瘦弱，腹肌照样顶不出来）。")

fit_trend = ("<b>假期训练复盘 + 明日（10/8）恢复方案</b><br><br>"
  "<table class=\"data-table\"><tr><th>项目</th><th>假期期间</th><th>10/8 起恢复</th></tr>"
  "<tr><td><b>训练频率</b></td><td>每天最低 15 分钟自重（目标：不断）</td><td>回到 4 力量日 + 1 有氧日</td></tr>"
  "<tr><td><b>强度</b></td><td>不追求力竭，完成即算</td><td style=\"color:var(--red)\">用假期前 <b>70-80%</b> 的重量重新激活</td></tr>"
  "<tr><td><b>本周目标</b></td><td>维持习惯</td><td>把容量恢复到假期前水平，<b>不追求突破</b></td></tr>"
  "<tr><td><b>饮食</b></td><td>训练日 2500 / 休息日 2300 kcal</td><td>同上；蛋白 110-130g 不变</td></tr>"
  "<tr><td><b>体重</b></td><td>假期饮食不规律，暂不作准</td><td>恢复规律饮食 3 天后重新称重校准</td></tr></table><br>"
  "<b>为什么恢复期要用 70-80% 重量</b>：假期七天即使维持了自重训练，大重量的神经适应仍会下降。"
  "直接上假期前的极限重量，受伤风险明显上升，而且第一次训练的糟糕体验会影响后续坚持。"
  "用较轻重量做一组完整训练，本周内逐步加回来即可。")

fit_tip = ("<b>明日（10/8）第一练的具体安排</b><br>"
  "① 重量取假期前的 70-80%，每个动作先用 1 组热身找感觉<br>"
  "② 动作质量优先：宁可减重量，也不要借力变形<br>"
  "③ 训练后 30 分钟内补充蛋白（≥25g）+ 碳水<br>"
  "④ 本周不做组数增加，先把 4 个力量日跑通<br><br>"
  "【为什么增肌期也要控脂】lean bulk 的意思是【小幅热量盈余 + 足够蛋白 + 规律训练】。"
  "盈余过大会直接变成脂肪，所以热量只加 200-300 kcal，蛋白保持 110-130g，其余靠训练量推动。<br><br>" + old['fitness']['tip'])

fit_reasoning = old['fitness']['reasoning']
fit_verdict = old['fitness']['verdict']

# ==================== ai-track ====================
ai_summary = ("<b>假期收官（10/7 更新）</b>｜国庆七天里 AI 领域没有需要立刻行动的新变化，"
  "因此这段时间的正确用法是<b>沉淀而不是接入</b>——把 9 月积累的两条线写成分产品分析文档，明日 10/8 起直接用于投递。<br><br>"
  "<b>一、DSH 桌面端（9/25 官方预览版 · 假期沉淀）</b>：9 月 25 日晚，开发者在 DeepSeek Harness 官方仓库发现桌面端源码"
  "（<code>apps/desktop</code>），版本 <b>V0.1.7-rc.1</b>（内置更新可至 rc.2），下载源 download.deepseek.com。<br>"
  "技术上是 <b>Electron</b> 实现——官方明确说明目标不是重做一套 Harness，而是"
  "<b>直接复用现有 Web UI 以及 Agent、会话、工具、插件等运行逻辑</b>。平台为 Windows x64 与 macOS arm64（Mac 版已过 Apple 公证），<b>暂无 Linux</b>。<br>"
  "与网页版最大的差异：桌面端<b>需充值 + 需实名认证</b>；新增四种 Agent 档位（标准/PTC/极简/创造）、可视化插件面板、"
  "任务式回答区（显示 Token 数/工具调用次数/耗时）。<br><br>"
  "<b>二、Jev 决策模型（TypeSafe · 9/15 发布 · 假期沉淀）</b>：定位是<b>首个 System One Model</b>——不生成文字，只输出判断："
  "给定 <code>state</code> 与类型化的 <code>questions</code>（Choice/Score/Boolean），返回 choice/score/probability。<br>"
  "用的是 RLCD（强化学习 + 对比蒸馏）训练路线，通过 Vercel AI SDK / Gateway 接入。发布后 24 小时内被约 13% 的付费团队试用。<br>"
  "实测数据（50 条中文计算机题目）：准确率 64-65%，单题 0.73 秒、50 题约 0.002 美元；对照 DeepSeek V4 Flash 为单题 5.58 秒、成本约 2.5 倍。")

ai_trend = ("<b>节后（10/8 起）怎么用这两份分析</b><br><br>"
  "假期写完的文档不是放着看的，10/8 起有三个明确用途："
  "① <b>投递附件</b>——作为作品集的一部分随简历发出，展示架构判断力；"
  "② <b>面试素材</b>——【多端形态怎么取舍】【什么时候该用专门模型而不是通用大模型】是 AI 产品岗的高频题，你有真实的一手材料（版本号、对比维度、实测数据）；"
  "③ <b>复盘底稿</b>——三个月后回看当时的判断，检验哪些成立、哪些是当时的误判。<br><br>"
  "<b>两份文档的骨架</b>（每份两页以内）：<br>"
  "《DSH 桌面端 vs 网页版：多端形态的取舍逻辑》→ 背景 / 对比维度（成本·隐私·平台·能力复用）/ 结论与依据 / <b>改变结论的条件</b><br>"
  "《Jev 接入决策：决策模型与生成模型的边界》→ 它解决什么 / 不能解决什么 / 实测数据 / 什么条件下才该接入 / <b>两个易误读的宣传点</b><br><br>"
  "【附】假期沉淀的核心对比表：<br><br>"
  "<table class=\"data-table\"><tr><th>维度</th><th>网页版</th><th>桌面端（预览版）</th></tr>"
  "<tr><td><b>获取成本</b></td><td style=\"color:var(--green)\">注册即用，免费</td><td style=\"color:var(--red)\">需充值 + <b>需实名认证</b></td></tr>"
  "<tr><td><b>安装</b></td><td style=\"color:var(--green)\">零安装</td><td>需下载安装包</td></tr>"
  "<tr><td><b>平台</b></td><td style=\"color:var(--green)\">全平台（含 Linux/平板）</td><td>仅 Win x64 + macOS arm64</td></tr>"
  "<tr><td><b>本机文件访问</b></td><td style=\"color:var(--green)\">完全可用</td><td>同样可用</td></tr>"
  "<tr><td><b>Agent 能力</b></td><td colspan=\"2\" style=\"text-align:center\">同一套（官方复用运行逻辑）</td></tr>"
  "<tr><td><b>Agent 档位</b></td><td>—</td><td style=\"color:var(--green)\">四种：标准 / PTC / 极简 / 创造</td></tr>"
  "<tr><td><b>插件管理</b></td><td>命令行</td><td style=\"color:var(--green)\">可视化面板</td></tr>"
  "<tr><td><b>稳定性</b></td><td style=\"color:var(--green)\">已稳定</td><td style=\"color:var(--red)\">rc 预览版</td></tr></table>")

ai_tip = ("<b>10/7 收尾清单（明天就能用出去）</b><br><br>"
  "① <b>检查两份文档是否达到【可发出】标准</b>：有没有结论、有没有依据、有没有写明【改变结论的条件】。"
  "三者缺一，就还是笔记而不是作品。<br>"
  "② <b>准备一句话摘要</b>：每份文档配一句 20 字以内的说明，方便放进邮件正文或简历的项目描述里。<br>"
  "③ <b>不接入、不充值</b>——假期结束也不改变这个结论。求职期现金流优先，等你有了带后端的判断密集型系统再评估 Jev。<br><br>" + old['ai-track']['tip'])

ai_reasoning = ("为什么假期结束、结论依然不变：<br><br>"
  "<b>① 两者的适用场景你仍然不具备。</b>DSH 桌面端多出来的能力集中在插件开发与重度 Agent 流水线；"
  "Jev 需要的是一个有大量判断环节的<b>后端系统</b>。你目前是纯前端项目 + 内容产出。<br><br>"
  "<b>② 它们代表的两个产品范式值得带走。</b>DSH 桌面端体现【<b>多端复用架构</b>】——官方选择 Electron 并复用同一套运行逻辑，"
  "说明产品形态已稳定，桌面端是【入口扩展】而非【能力分叉】。Jev 体现【<b>模型分工</b>】——"
  "把写作/推理交给通用大模型，把边界清晰的小判断交给专门组件，用 0.73 秒替代 5.58 秒。<br><br>"
  "<b>③ 这两个范式恰好是 AI 产品岗的高频面试题。</b>你现在有真实的一手材料（版本号、对比维度、实测数据），"
  "把它整理成结构化的分析，比背通用答案有说服力。<br><br>"
  "<b>④ 所以节后的动作依然是【沉淀】而不是【接入】。</b>接入需要花钱花时间且当前无场景；沉淀成本几乎为零，产出直接服务求职。")

new = {
 'fitness': {'verdict': fit_verdict or ("🎯 假期收官（10/7）：增肌第 3 周结束，明日 10/8 恢复正式训练。"
    "假期守住【每天最低 15 分钟自重】即为成功——连续性比进步重要。10/8 第一练用假期前 70-80% 的重量重新激活，本周目标是把容量恢复到假期前水平。"),
    'summary': fit_summary, 'trend': fit_trend, 'tip': fit_tip, 'reasoning': fit_reasoning,
    'updated': TODAY},
 'ai-track': {'verdict': ("🎯 假期收官（10/7）：9 月 AI 两条线（DSH 桌面端 / Jev 决策模型）已完成沉淀，结论不变——"
    "① DSH 桌面端：<b>继续用网页版</b>；② Jev：<b>现在不接入</b>，列入待观察。明日 10/8 起把这两份分析用出去（投递附件 + 面试素材）。"),
    'summary': ai_summary, 'trend': ai_trend, 'tip': ai_tip, 'reasoning': ai_reasoning,
    'updated': TODAY}
}


def replace_section(text, key, obj):
    pat = re.compile(r'((?:"' + re.escape(key) + r'"|' + re.escape(key) + r')\s*:\s*\{)([\s\S]*?)(\n  \})')
    m = pat.search(text)
    if not m:
        print('  ❌ 未找到分区:', key); return text, False
    parts = []
    for f in ['verdict', 'summary', 'trend', 'tip', 'reasoning', 'updated']:
        if obj.get(f):
            parts.append('    %s: %s' % (f, js(obj[f])))
    return text[:m.start()] + m.group(1) + '\n' + ',\n'.join(parts) + m.group(3) + text[m.end():], True


for key, obj in new.items():
    d, ok = replace_section(d, key, obj)
    print(('  ✅ ' if ok else '  ❌ ') + key + ' 已重写')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
