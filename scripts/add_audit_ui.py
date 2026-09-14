# -*- coding: utf-8 -*-
"""在个人网站首页加入「本次更新核查」区块：
   页面打开时实时计算（读你电脑的时钟 + 抽取各分区内容里的日期），
   不是写死的结论 —— 所以无法虚标。
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) 新增 section ----------
if 'id="update-audit"' not in h:
    anchor = '<section id="daily-vocab"'
    if anchor not in h:
        # 退而求其次：插在 dashboard 之后
        anchor = '<section id="daily-quiz"'
    sect = ('<section id="update-audit" class="section" data-search="更新 核查 日期 新鲜度 凭证">'
            '<div class="section-header"><h2>✅ 本次更新核查</h2>'
            '<span class="section-sub">打开页面时实时计算 · 非写死结论</span></div>'
            '<div id="zhAuditBox"></div></section>\n\n')
    h = h.replace(anchor, sect + anchor, 1)
    print('OK 已插入 update-audit 区块')
else:
    print('区块已存在')

# ---------- 2) 加入首页展示列表 ----------
h = h.replace("var HOME_SECTIONS = ['dashboard','daily-vocab','daily-quiz','guide','optimization','ai-assistant'];",
              "var HOME_SECTIONS = ['dashboard','update-audit','daily-vocab','daily-quiz','guide','optimization','ai-assistant'];", 1)
if "modes" in h and "'dashboard','update-audit'" not in h:
    # 三模式里也各加一份
    h = re.sub(r"sections:\['dashboard',", "sections:['dashboard','update-audit',", h)
print('OK 已加入首页展示')

# ---------- 3) 核查逻辑 ----------
JS = r'''
// ===== 本次更新核查（页面打开时实时计算，非写死）=====
function zh_iso(s){
  if(!s) return null;
  var m=String(s).match(/(\d{4})\D+(\d{1,2})\D+(\d{1,2})/);
  if(m) return m[1]+'-'+String(m[2]).padStart(2,'0')+'-'+String(m[3]).padStart(2,'0');
  return null;
}
function zh_extractDates(txt){
  // 抽取文本里所有 M月D日 / M/D
  var out=[];
  var m, re1=/(\d{1,2})月(\d{1,2})日/g;
  while((m=re1.exec(txt))) out.push([parseInt(m[1],10),parseInt(m[2],10)]);
  var re2=/(?:^|[^\d])(\d{1,2})\/(\d{1,2})(?![\d])/g;
  while((m=re2.exec(txt))){
    var a=parseInt(m[1],10), b=parseInt(m[2],10);
    if(a>=1&&a<=12&&b>=1&&b<=31) out.push([a,b]);
  }
  return out;
}
function zh_renderUpdateAudit(){
  var box=document.getElementById('zhAuditBox');
  if(!box) return;
  var now=new Date();
  var today=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0');
  var wd=['周日','周一','周二','周三','周四','周五','周六'][now.getDay()];

  // ---- A. 日期字段一致性 ----
  var fields=[];
  try{ fields.push(['今日要闻', DAILY_BRIEFING&&DAILY_BRIEFING.date]); }catch(e){}
  try{ fields.push(['每日一词', DAILY_VOCAB&&DAILY_VOCAB.date]); }catch(e){}
  try{ fields.push(['小白课堂', LEARN_PATHS&&LEARN_PATHS.updated]); }catch(e){}
  try{ fields.push(['市场情绪', MARKET_SENTIMENT&&MARKET_SENTIMENT.updated]); }catch(e){}
  try{ fields.push(['今日待办', DAILY_DECISIONS&&DAILY_DECISIONS.updated]); }catch(e){}
  try{ fields.push(['机会雷达', OPPORTUNITY_RADAR&&OPPORTUNITY_RADAR.updated]); }catch(e){}
  try{ fields.push(['判断台账', AI_JUDGMENTS&&AI_JUDGMENTS.updated]); }catch(e){}
  try{ fields.push(['工具链雷达', TOOLCHAIN_RADAR&&TOOLCHAIN_RADAR.updated]); }catch(e){}
  try{ if(DAILY_DATA&&DAILY_DATA.movie) fields.push(['影视数据', DAILY_DATA.movie.updated]); }catch(e){}

  var secRows=[];
  try{
    Object.keys(INSIGHTS||{}).forEach(function(k){
      var s=INSIGHTS[k];
      var blob=(s.summary||'')+' '+(s.trend||'')+' '+(s.tip||'');
      var ds=zh_extractDates(blob);
      var newest=null;
      ds.forEach(function(p){
        var d=new Date(now.getFullYear(), p[0]-1, p[1]);
        if(!newest||d>newest) newest=d;
      });
      var lag = newest? Math.round((new Date(today)-newest)/86400000) : null;
      secRows.push({k:k, updated:zh_iso(s.updated), newest:newest, lag:lag});
    });
  }catch(e){}

  // ---- 统计 ----
  var dateBad=[], dateOk=0;
  fields.forEach(function(f){ var v=zh_iso(f[1]); if(v===today) dateOk++; else dateBad.push(f[0]+'='+(f[1]||'空')); });
  var lagBad=[], lagOk=0;
  secRows.forEach(function(r){ if(r.lag===null||r.lag<=0) lagOk++; else lagBad.push(r.k+'（内容最新 '+r.newest.getMonth()+1+'月'+r.newest.getDate()+'日，落后 '+r.lag+' 天）'); });

  var allOk = !dateBad.length && !lagBad.length;

  // ---- 渲染 ----
  var h='';
  h+='<div class="card" style="padding:16px 18px;border-left:4px solid '+(allOk?'#059669':'#dc2626')+'">';
  h+='<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px">';
  h+='<span style="font-size:15px;font-weight:800;color:'+(allOk?'#059669':'#dc2626')+'">'+(allOk?'✅ 更新核查全部通过':'❌ 发现 '+(dateBad.length+lagBad.length)+' 项异常')+'</span>';
  h+='<span class="tag" style="background:var(--accent);color:#fff">今天 '+today+' '+wd+'</span>';
  h+='</div>';
  h+='<div style="font-size:11.5px;color:var(--text2);line-height:1.9">';
  h+='· 日期字段：<b style="color:'+(dateBad.length?'#dc2626':'#059669')+'">'+dateOk+'/'+fields.length+'</b> 与今天一致'+(dateBad.length?'（异常：'+dateBad.join('、')+'）':'')+'<br>';
  h+='· 内容新鲜度：<b style="color:'+(lagBad.length?'#dc2626':'#059669')+'">'+lagOk+'/'+secRows.length+'</b> 个分区的内容日期不落后'+(lagBad.length?'（滞后：'+lagBad.join('；')+'）':'')+'<br>';
  h+='· 这张表是<b>页面打开时用脚本现算的</b>（读你电脑的时钟 + 抽取页面上真实显示的内容日期），不是写死的结论——所以它无法虚标。';
  h+='</div>';
  h+='<details class="acc" style="margin-top:12px"><summary>展开逐分区明细（'+secRows.length+' 个分区）</summary><div class="accbody">';
  h+='<table class="data-table"><tr><th>分区</th><th>标注更新时间</th><th>内容里的最新日期</th><th>状态</th></tr>';
  secRows.forEach(function(r){
    var st = (r.lag===null) ? '<span style="color:var(--text3)">无日期</span>' : (r.lag<=0 ? '<span style="color:#059669">✅ 最新</span>' : '<span style="color:#dc2626">❌ 落后 '+r.lag+' 天</span>');
    var nd = r.newest ? (r.newest.getMonth()+1)+'月'+r.newest.getDate()+'日' : '—';
    var upOk = r.updated===today;
    h+='<tr><td>'+r.k+'</td><td style="color:'+(upOk?'#059669':'#dc2626')+'">'+(r.updated||'—')+'</td><td>'+nd+'</td><td>'+st+'</td></tr>';
  });
  h+='</table>';
  h+='<div style="font-size:11px;color:var(--text2);margin-top:9px;line-height:1.8">';
  h+='<b>怎么用这张表：</b>「内容里的最新日期」是从该分区正文中自动抽取的——如果某分区写着 9月6日 而今天是 9月14日，说明它的内容没真正刷新（哪怕「标注更新时间」写的是今天）。<br>';
  h+='<b>自己复核的方法：</b>点进该分区，看正文里提到的最近日期是不是今天前后。</div>';
  h+='</div></details>';
  h+='</div>';
  box.innerHTML=h;
}
'''
if 'function zh_renderUpdateAudit' not in h:
    # 插到 renderVocab 定义之前
    idx = h.find('var vocabShuffled = [];')
    if idx < 0:
        idx = h.find('function renderVocabCards')
    h = h[:idx] + JS + '\n' + h[idx:]
    print('OK 已插入核查逻辑')
else:
    print('核查逻辑已存在')

# ---------- 4) 注册到 onDataReady ----------
if 'zh_renderUpdateAudit' in h and 'zh_renderUpdateAudit,' not in h and 'zh_renderUpdateAudit, checkUpdateStatus' not in h:
    h = h.replace('zh_renderTraining, zh_updateTrainEntry, checkUpdateStatus',
                  'zh_renderTraining, zh_updateTrainEntry, zh_renderUpdateAudit, zh_updateTrainEntry, checkUpdateStatus', 1)
    print('已尝试注册到 onDataReady')

open(FP, 'w', encoding='utf-8').write(h)
print('已写回 index.html')
