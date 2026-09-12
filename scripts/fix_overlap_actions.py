# -*- coding: utf-8 -*-
"""修复三项：
①AI_JUDGMENTS 每条加 action(推荐行动)
②作战计划改为「判断层」不再重复决策单的行动(解决重叠)
③渲染时显示 action
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ========== A. daily_data.js: 判断加 action ==========
FP1 = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP1, 'r', encoding='utf-8').read()

reps = [
 ("evidence:'9/10 DeepSeek V4.1 Flash 发布——多个benchmark超Claude Opus 5与GPT-5.6 Sol，MIT开源、API峰值$0.3/$1.2，验证了判断（比预期更快）'}",
  "evidence:'9/10 DeepSeek V4.1 Flash 发布——多个benchmark超Claude Opus 5与GPT-5.6 Sol，MIT开源、API峰值$0.3/$1.2，验证了判断（比预期更快）', action:'✓已应验：①把这次判断写成行业观察《开源追平闭源意味着什么》②升级工具链 Harness+V4.1 Flash 实测 ③继续跟踪下一个开源发布(Qwen/GLM)是否延续'}"),
 ("evidence:'9/9-9/11 美国加州签署AI安全法案（Anthropic/OpenAI支持）；OpenAI系统卡披露推理可监控性下降引发安全研究者关注——安全治理确实进入政策议程'}",
  "evidence:'9/9-9/11 美国加州签署AI安全法案（Anthropic/OpenAI支持）；OpenAI系统卡披露推理可监控性下降引发安全研究者关注——安全治理确实进入政策议程', action:'✓已应验：①简历技能栏补『AI安全治理/AI合规认知』②了解红队测试/安全评估术语 ③关注国内AI监管政策(工信部人工智能+软件)'}"),
 ("evidence:'9/11 覆铜板+4.31%/元件+1.80%/MLCC+1.76% 逆势走强（沪指-1.18%），初步验证中'}",
  "evidence:'9/11 覆铜板+4.31%/元件+1.80%/MLCC+1.76% 逆势走强（沪指-1.18%），初步验证中', action:'📌今天要做：①留意覆铜板/元件/光通信是否继续跑赢大盘 ②若连续3日跑赢→记入观察清单(不追高) ③9/18验证日复盘：涨跌对比 + 判断对错归档'}"),
 ("evidence:'V4.1 Flash AutomationBench-AA 超 GPT-6 Astra 拿第一（事务Agent）；Agents API 标准化中'}",
  "evidence:'V4.1 Flash AutomationBench-AA 超 GPT-6 Astra 拿第一（事务Agent）；Agents API 标准化中', action:'📌本周要做：①用 Harness+V4.1 Flash 跑一个真实自动化任务(如每日资讯汇总)，记录耗时与成本 ②把过程写成『Agent降本实测』作品 ③Q4观察：市面上是否出现低价Agent产品'}"),
 ("evidence:'OpenAI Agents API公开测试；无问芯穹发布Agent-Native模型NeoHorse；招聘侧待观察'}",
  "evidence:'OpenAI Agents API公开测试；无问芯穹发布Agent-Native模型NeoHorse；招聘侧待观察', action:'📌每周要做：①在BOSS直聘搜『AI Agent产品/策略运营』记录岗位数量变化 ②收藏3个目标岗位JD做能力对标 ③把『Agent-Native/AutomationBench』等术语补进知识库'}")
]
n=0
for old,new in reps:
    if old in c:
        c = c.replace(old, new, 1); n+=1
    else:
        print('MISS:', old[:50])
print('判断action已加:', n, '/5')
open(FP1,'w',encoding='utf-8').write(c)

# ========== B. index.html: 渲染显示 action + 作战计划改造 ==========
FP2 = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP2, 'r', encoding='utf-8').read()

# B1. 判断卡片显示 action
old_render = """    if(j.evidence) h+='<div class="jd-ev">🔍 '+escHtml(j.evidence)+'</div>';"""
new_render = """    if(j.evidence) h+='<div class="jd-ev">🔍 '+escHtml(j.evidence)+'</div>';
    if(j.action) h+='<div style="font-size:10px;line-height:1.65;margin-top:4px;padding:5px 8px;background:var(--accent-light);border-radius:6px;color:var(--accent);font-weight:600">👉 '+escHtml(j.action)+'</div>';"""
if old_render in h:
    h = h.replace(old_render, new_render, 1); print('OK 渲染action')
else:
    print('MISS 渲染action')

# B2. 作战计划：去掉与决策单重复的"3件事"，改为「AI判断提醒」
old_bp = """  if(acts.length){
    hh+='<div class="bp-sec-t">⚡ 今天优先做的 ' + acts.length + ' 件事</div>';
    acts.forEach(function(a){
      var pc = a.priority==='P0'?'':'p1';
      hh+='<div class="bp-act"><span class="bp-p '+pc+'">'+a.priority+'</span><span>'+escHtml(a.action||'')+(a.why?'<br><span style="opacity:.72">理由：'+escHtml(a.why).slice(0,80)+'</span>':'')+'</span></div>';
    });
  }"""
new_bp = """  // ② 待验证判断提醒（与今日决策单分工：这里给「判断/提醒」，决策单给「行动清单」）
  var pendingJ=[];
  try{
    if(typeof AI_JUDGMENTS!=='undefined' && AI_JUDGMENTS.items){
      AI_JUDGMENTS.items.forEach(function(j){ if(j.status!=='已验证') pendingJ.push(j); });
    }
    var mineJ=[]; try{ mineJ=JSON.parse(localStorage.getItem('myJudgments')||'[]'); }catch(e){}
    mineJ.forEach(function(j){ if(j.status!=='已验证') pendingJ.push(j); });
  }catch(e){}
  if(pendingJ.length){
    hh+='<div class="bp-sec-t">⚖️ 待验证判断（今天留意这些信号）</div>';
    pendingJ.slice(0,2).forEach(function(j){
      hh+='<div class="bp-act"><span class="bp-p p1">判断</span><span>'+escHtml(j.topic||'')+'：'+escHtml((j.judgment||'').slice(0,60))+
          (j.action?'<br><span style="opacity:.8">👉 '+escHtml(j.action).slice(0,90)+'</span>':'')+'</span></div>';
    });
  }"""
if old_bp in h:
    h = h.replace(old_bp, new_bp, 1); print('OK 作战计划改造')
else:
    print('MISS 作战计划改造')

# B3. 作战计划底部加"决策单指引"
old_foot = """  hh+='<div class="bp-foot">依据当日市场情绪 / 决策单 / 板块分析自动合成 · 每日更新</div>';"""
new_foot = """  var decCount=0;
  try{ if(typeof DAILY_DECISIONS!=='undefined'&&DAILY_DECISIONS.items) decCount=DAILY_DECISIONS.items.length; }catch(e){}
  hh+='<div class="bp-foot">🧭 本卡=AI判断层（态势/判断提醒/风险）｜行动清单见下方「📌 今日决策单」'+(decCount?('（'+decCount+' 件事）'):'')+' · 每日更新</div>';"""
if old_foot in h:
    h = h.replace(old_foot, new_foot, 1); print('OK 底部指引')
else:
    print('MISS 底部指引')

open(FP2,'w',encoding='utf-8').write(h)
print('done')
