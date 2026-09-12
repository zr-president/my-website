# -*- coding: utf-8 -*-
"""突破二：AI 主动作战计划（规则引擎从当日数据合成 态势判断+今日3件事+风险提示）
同时实现 UI 优化点1：视觉焦点大卡片（深色渐变，首屏最显眼）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) CSS ----------
css_anchor = '/* ===== 判断台账（突破一：把信息消费转为能力资产）===== */'
css_new = """/* ===== AI 作战计划（突破二：AI主动服务 + 视觉焦点大卡片）===== */
.bp-wrap{position:relative;overflow:hidden;background:linear-gradient(135deg,#1e1b4b 0%,#312e81 55%,#4c1d95 100%);color:#fff;border-radius:14px;padding:16px 18px;margin-bottom:14px;box-shadow:0 6px 24px rgba(49,46,129,.28)}
.bp-wrap::after{content:'';position:absolute;top:-60%;right:-10%;width:55%;height:200%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);transform:rotate(18deg);animation:zhShine 9s linear infinite;pointer-events:none}
.bp-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:9px}
.bp-head h3{font-size:14px;margin:0;font-weight:800;letter-spacing:.3px}
.bp-head .bp-date{font-size:10px;opacity:.7;margin-left:auto}
.bp-stance{background:rgba(255,255,255,.11);border-radius:10px;padding:9px 12px;font-size:12px;line-height:1.75;margin-bottom:10px;border-left:3px solid #a5b4fc}
.bp-stance b{color:#fde68a}
.bp-sec-t{font-size:10px;font-weight:800;letter-spacing:1px;opacity:.72;margin:9px 0 5px}
.bp-act{display:flex;gap:8px;align-items:flex-start;background:rgba(255,255,255,.07);border-radius:9px;padding:8px 11px;margin-bottom:5px;font-size:11.5px;line-height:1.65}
.bp-act .bp-p{font-size:9px;font-weight:800;padding:1px 6px;border-radius:7px;background:#f59e0b;color:#1c1917;flex-shrink:0;margin-top:2px}
.bp-act .bp-p.p1{background:#a5b4fc;color:#1e1b4b}
.bp-act .bp-p.p2{background:rgba(255,255,255,.3);color:#fff}
.bp-risk{background:rgba(239,68,68,.16);border-left:3px solid #f87171;border-radius:9px;padding:8px 11px;font-size:11px;line-height:1.7;margin-top:9px}
.bp-foot{font-size:9px;opacity:.6;margin-top:9px;text-align:right}

""" + css_anchor
h = h.replace(css_anchor, css_new, 1)

# ---------- 2) DOM：插在 zhHero 之后（首屏最显眼）----------
dom_anchor = """	<!-- #38: 今日必看置顶聚合卡片 -->"""
dom_new = """	<!-- 突破二：AI 主动作战计划（自动合成态势+行动+风险·视觉焦点大卡片） -->
	<div id="zhBattlePlan"></div>

	<!-- #38: 今日必看置顶聚合卡片 -->"""
if dom_anchor in h:
    h = h.replace(dom_anchor, dom_new, 1)
    print('OK DOM 已插入')
else:
    print('DOM MISS')

# ---------- 3) JS 渲染函数 ----------
js_anchor = '// ===== 判断台账（突破一）====='
js_new = """// ===== AI 作战计划（突破二：规则引擎主动合成）=====
function zh_buildBattlePlan(){
  var box=document.getElementById('zhBattlePlan');
  if(!box) return;
  var today=new Date();
  var dateStr=today.getFullYear()+'/'+(today.getMonth()+1)+'/'+today.getDate()+' 周'+'日一二三四五六'.charAt(today.getDay());
  // --- 1) 态势判断（从市场情绪+市场摘要推导）---
  var ms=(typeof MARKET_SENTIMENT!=='undefined'&&MARKET_SENTIMENT.items)?MARKET_SENTIMENT.items:[];
  var breadth='', volume='', idxInfo='', strong='';
  ms.forEach(function(it){
    var L=it.label||'';
    if(L.indexOf('涨跌')>=0) breadth=(it.value||'')+' '+(it.note||'');
    else if(L.indexOf('量能')>=0) volume=(it.value||'')+' '+(it.note||'');
    else if(L.indexOf('沪指')>=0) idxInfo=(it.value||'')+' '+(it.note||'');
    else if(L.indexOf('强势')>=0) strong=(it.value||'')+' '+(it.note||'');
  });
  var stance='';
  if(breadth && (breadth.indexOf('↓')>=0 || /\\d{3,}↓/.test(breadth) || breadth.indexOf('普跌')>=0 || breadth.indexOf('11%')>=0)){
    stance='<b>普跌格局</b>——赚钱效应低，今天不适合激进操作。'+(strong?('结构主线仍在「'+strong.split(' ')[0]+'」，但别追高。'):'')+'等企稳信号（收回关键位+放量）再谈加仓。';
  } else if(idxInfo && idxInfo.indexOf('-')>=0){
    stance='<b>指数承压</b>——'+idxInfo.slice(0,40)+'。轻仓观察，回避前期涨幅大的方向。';
  } else if(idxInfo && idxInfo.indexOf('+')>=0){
    stance='<b>指数偏强</b>——'+idxInfo.slice(0,40)+'。可关注结构主线回踩机会，但别追涨停板。';
  } else {
    stance='今日先看市场情绪与板块结构，再决定动作（详见股市板块）。';
  }
  if(volume) stance+='<br>量能：'+volume.slice(0,50)+'。';
  // --- 2) 今日3件优先事（取 DAILY_DECISIONS 的 P0/P1）---
  var acts=[];
  if(typeof DAILY_DECISIONS!=='undefined' && DAILY_DECISIONS.items){
    DAILY_DECISIONS.items.forEach(function(it){
      if(it.priority==='P0'||it.priority==='P1') acts.push(it);
    });
  }
  acts=acts.slice(0,3);
  // --- 3) 风险提示（从 stock tip / 天气 提取）---
  var risk='';
  try{
    if(typeof INSIGHTS!=='undefined' && INSIGHTS.stock && INSIGHTS.stock.tip){
      var t=INSIGHTS.stock.tip;
      var m=t.match(/[^。；]*?(回避|风险|谨慎|别追|失守|跌破)[^。；]*/);
      if(m) risk=m[0].slice(0,90);
    }
  }catch(e){}
  if(!risk && typeof DAILY_DATA!=='undefined' && DAILY_DATA.weather_summary){
    risk='天气/生活：'+DAILY_DATA.weather_summary.slice(0,60);
  }
  // --- 组装 ---
  var hh='<div class="bp-wrap">';
  hh+='<div class="bp-head"><h3>🎯 今日作战计划</h3><span style="font-size:10px;padding:2px 9px;border-radius:9px;background:rgba(255,255,255,.16)">AI 自动生成</span><span class="bp-date">'+dateStr+'</span></div>';
  hh+='<div class="bp-stance">🧭 <b>今日态势</b>：'+stance+'</div>';
  if(acts.length){
    hh+='<div class="bp-sec-t">⚡ 今天优先做的 ' + acts.length + ' 件事</div>';
    acts.forEach(function(a){
      var pc = a.priority==='P0'?'':'p1';
      hh+='<div class="bp-act"><span class="bp-p '+pc+'">'+a.priority+'</span><span>'+escHtml(a.action||'')+(a.why?'<br><span style="opacity:.72">理由：'+escHtml(a.why).slice(0,80)+'</span>':'')+'</span></div>';
    });
  }
  if(risk) hh+='<div class="bp-risk">⚠️ <b>风险提示</b>：'+escHtml(risk)+'</div>';
  hh+='<div class="bp-foot">依据当日市场情绪 / 决策单 / 板块分析自动合成 · 每日更新</div>';
  hh+='</div>';
  box.innerHTML=hh;
}

// ===== 判断台账（突破一）====="""
if js_anchor in h:
    h = h.replace(js_anchor, js_new, 1)
    print('OK JS 已插入')
else:
    print('JS MISS')

# ---------- 4) onDataReady 注册 ----------
old = 'zh_renderJudgments, checkUpdateStatus'
if 'zh_buildBattlePlan, checkUpdateStatus' not in h:
    h = h.replace(old, 'zh_renderJudgments, zh_buildBattlePlan, checkUpdateStatus', 1)
    print('OK 注册')

open(FP, 'w', encoding='utf-8').write(h)
print('done')
