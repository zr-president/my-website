# -*- coding: utf-8 -*-
"""在个人网站加入「能力训练平台进度」卡片（读取同源 localStorage: tp_summary_v1）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) HTML 容器 ----------
old_html = '''<section id="zh-growth" class="section" data-search="成长 打卡 热力 进步 学习 健身">
<div id="zhGrowthBox"></div>
</section>'''
new_html = '''<section id="zh-growth" class="section" data-search="成长 打卡 热力 进步 学习 健身 训练 能力 SQL 数据 策略运营">
<div id="zhGrowthBox"></div>
<div id="zhTrainingBox" style="margin-top:12px"></div>
</section>'''
if old_html in h:
    h = h.replace(old_html, new_html, 1)
    print('OK HTML 容器已加')
else:
    print('MISS HTML 容器')

# ---------- 2) JS 渲染函数（插在 zh_renderGrowth 之前） ----------
anchor = 'function zh_renderGrowth('
if anchor not in h:
    print('MISS JS 锚点'); sys.exit(1)

js = """// ===== 能力训练平台进度回流（同源 localStorage: tp_summary_v1）=====
// 训练平台在 zr-president.github.io/training/，与本站同源 → localStorage 共享
function zh_renderTraining(){
  var box=document.getElementById('zhTrainingBox');
  if(!box) return;
  var TRAIN_URL='https://zr-president.github.io/training/';
  var s=null;
  try{ var raw=localStorage.getItem('tp_summary_v1'); if(raw) s=JSON.parse(raw); }catch(e){}
  if(!s || !s.mods){
    box.innerHTML='<div class="card" style="padding:13px 15px">'+
      '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">'+
      '<span style="font-size:14px;font-weight:700">🎓 能力训练平台</span>'+
      '<span style="font-size:10px;color:var(--text3)">策略运营 / 用户增长 · 7 个训练模块</span>'+
      '<a href="'+TRAIN_URL+'" target="_blank" rel="noopener" style="margin-left:auto;font-size:11px;font-weight:600;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent2));padding:5px 13px;border-radius:9px;text-decoration:none">去训练 →</a>'+
      '</div>'+
      '<div style="font-size:11.5px;color:var(--text2);line-height:1.75;margin-top:7px">'+
      '还没开始练。SQL 训练场 / 数据集实验室 / 指标设计 / 实验分析 / Case 拆解 / AI Agent / 能力雷达——全部在浏览器里动手做，数据只存本机。'+
      '</div></div>';
    return;
  }
  var mods=s.mods, order=['sql','lab','metrics','abtest','case','agent'];
  var rows='';
  order.forEach(function(k){
    var m=mods[k]; if(!m) return;
    var pct=m.total?Math.round(m.done/m.total*100):0;
    var col=pct>=100?'var(--green, #10b981)':pct>0?'var(--accent)':'var(--text3)';
    rows+='<div style="display:flex;align-items:center;gap:9px;padding:5px 0;border-bottom:1px solid var(--border)">'+
      '<span style="font-size:11.5px;color:var(--text2);flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+m.name+(m.extra&&m.extra.mastery!==undefined?' <span style="font-size:9px;color:var(--text3)">一次做对率 '+m.extra.mastery+'%</span>':'')+'</span>'+
      '<span style="width:88px;height:5px;background:var(--bg2);border-radius:3px;overflow:hidden;flex:0 0 auto">'+
      '<span style="display:block;height:100%;width:'+pct+'%;background:'+col+';border-radius:3px"></span></span>'+
      '<span style="font-size:10.5px;font-family:var(--mono,monospace);color:'+col+';width:52px;text-align:right;flex:0 0 auto">'+m.done+'/'+m.total+'</span>'+
      '</div>';
  });
  var radarHtml='';
  if(s.radar){
    radarHtml='<div style="margin-top:8px;font-size:11px;color:var(--text2)">🎯 能力雷达自评 <b style="color:var(--accent)">'+s.radar.rated+'/'+s.radar.total+'</b> 项 · 达成度 <b style="color:'+(s.radar.pct>=80?'#10b981':s.radar.pct>=55?'#f59e0b':'#ef4444')+'">'+s.radar.pct+'%</b></div>';
  }
  var pctAll=s.pct||0;
  box.innerHTML='<div class="card" style="padding:13px 15px">'+
    '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:9px">'+
    '<span style="font-size:14px;font-weight:700">🎓 能力训练平台</span>'+
    '<span style="font-size:10px;color:var(--text3)">策略运营 / 用户增长</span>'+
    '<span style="font-size:10px;padding:2px 9px;border-radius:9px;background:var(--accent-light);color:var(--accent);font-weight:700">总进度 '+s.done+'/'+s.total+'（'+pctAll+'%）</span>'+
    '<a href="'+TRAIN_URL+'" target="_blank" rel="noopener" style="margin-left:auto;font-size:11px;font-weight:600;color:var(--accent);text-decoration:none">去训练 →</a>'+
    '</div>'+
    '<div style="height:7px;background:var(--bg2);border-radius:4px;overflow:hidden;margin-bottom:10px">'+
    '<div style="height:100%;width:'+pctAll+'%;background:linear-gradient(90deg,var(--accent),var(--accent2));border-radius:4px"></div></div>'+
    rows+radarHtml+
    '<div style="font-size:9.5px;color:var(--text3);margin-top:8px">数据来自训练平台（同源 localStorage，只存本机）'+(s.updated?' · 最近 '+s.updated:'')+'</div>'+
    '</div>';
}

"""
h = h.replace(anchor, js + anchor, 1)
print('OK JS 函数已插入')

# ---------- 3) 注册到 onDataReady ----------
old_task = 'zh_renderGrowth, zh_renderGrowthWorkbench, zh_renderJudgments, zh_buildBattlePlan, checkUpdateStatus'
if old_task in h:
    h = h.replace(old_task, 'zh_renderGrowth, zh_renderGrowthWorkbench, zh_renderJudgments, zh_buildBattlePlan, zh_renderTraining, checkUpdateStatus', 1)
    print('OK 已注册到 onDataReady')
else:
    # 尝试更宽松的匹配
    import re
    m = re.search(r'zh_renderJudgments,\s*zh_buildBattlePlan,\s*checkUpdateStatus', h)
    if m:
        h = h[:m.start()] + 'zh_renderJudgments, zh_buildBattlePlan, zh_renderTraining, checkUpdateStatus' + h[m.end():]
        print('OK 已注册(宽松匹配)')
    else:
        print('MISS 注册点')

open(FP, 'w', encoding='utf-8').write(h)
print('done')
