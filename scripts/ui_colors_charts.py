# -*- coding: utf-8 -*-
"""UI优化: ①分类卡片按类别配色(记忆点) ②成长打卡14天迷你柱状图(数据可视化)"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) 分类卡片配色 ----------
old1 = """        var opacity = catMaxWeight<=1 ? '0.55' : catMaxWeight===2 ? '0.8' : '1';
        h += '<div class=\\"cat-card\\" style=\\"opacity:'+opacity+'\\" onclick=\\"navigateTo(\\'category\\',\\''+k+'\\')\\">';
        h += '<div class=\\"cat-header\\"><span class=\\"cat-icon\\">'+cat.icon+'</span><span class=\\"cat-name\\">'+cat.name+'</span></div>';"""
new1 = """        var opacity = catMaxWeight<=1 ? '0.55' : catMaxWeight===2 ? '0.8' : '1';
        var catColors = {about:'#3b82f6', fun:'#a855f7', life:'#10b981', finance:'#f59e0b', tools:'#06b6d4'};
        var cc = catColors[k] || 'var(--accent)';
        h += '<div class=\\"cat-card\\" style=\\"opacity:'+opacity+';border-top:3px solid '+cc+'\\" onclick=\\"navigateTo(\\'category\\',\\''+k+'\\')\\">';
        h += '<div class=\\"cat-header\\"><span class=\\"cat-icon\\" style=\\"background:'+cc+'1f;color:'+cc+'\\">'+cat.icon+'</span><span class=\\"cat-name\\">'+cat.name+'</span></div>';"""
if old1 in h:
    h = h.replace(old1, new1, 1)
    print('OK 分类配色')
else:
    print('MISS 分类配色')

# ---------- 2) 成长打卡 14 天柱状图 ----------
old2 = """  h+='<div style="display:flex;gap:6px;flex-wrap:wrap">';
  ZH_GROWTH_TYPES.forEach(function(t){
    var on=a.indexOf(t)>=0;
    h+='<button onclick="zh_growthToggle(\\''+t+'\\')" style="padding:5px 11px;border-radius:14px;font-size:11px;font-weight:600;cursor:pointer;border:1px solid '+(on?'var(--accent)':'var(--border)')+';background:'+(on?'var(--accent)':'var(--bg)')+';color:'+(on?'#fff':'var(--text2)')+';font-family:inherit;transition:.15s">'+(on?'✓ ':'')+t+'</button>';
  });
  h+='</div></div>';"""
new2 = """  h+='<div style="display:flex;gap:6px;flex-wrap:wrap">';
  ZH_GROWTH_TYPES.forEach(function(t){
    var on=a.indexOf(t)>=0;
    h+='<button onclick="zh_growthToggle(\\''+t+'\\')" style="padding:5px 11px;border-radius:14px;font-size:11px;font-weight:600;cursor:pointer;border:1px solid '+(on?'var(--accent)':'var(--border)')+';background:'+(on?'var(--accent)':'var(--bg)')+';color:'+(on?'#fff':'var(--text2)')+';font-family:inherit;transition:.15s">'+(on?'✓ ':'')+t+'</button>';
  });
  h+='</div>';
  // 近14天打卡柱状图（数据可视化）
  var maxV=1; Object.keys(daysLog).forEach(function(k){ if(daysLog[k]>maxV) maxV=daysLog[k]; });
  var order=[]; for(var d2=13; d2>=0; d2--){ var dd=new Date(); dd.setDate(dd.getDate()-d2); order.push(dd.getFullYear()+'-'+String(dd.getMonth()+1).padStart(2,'0')+'-'+String(dd.getDate()).padStart(2,'0')); }
  h+='<div style="margin-top:10px;font-size:9px;color:var(--text3)">近14天打卡趋势（最高 '+maxV+' 次/天）</div>';
  h+='<div style="display:flex;gap:3px;align-items:flex-end;height:44px;margin-top:4px">';
  order.forEach(function(k,ix){
    var v=daysLog[k]||0;
    var hp=v>0?Math.round(v/maxV*100):6;
    var isToday=(ix===order.length-1);
    var bg=v===0?'var(--bg2)':(v>=3?'linear-gradient(180deg,#8b5cf6,#a78bfa)':'linear-gradient(180deg,#6366f1,#818cf8)');
    h+='<div title="'+k+'：'+v+'次" style="flex:1;height:'+hp+'%;background:'+bg+';border-radius:2px;'+(isToday?'outline:1px solid var(--accent)':'')+'"></div>';
  });
  h+='</div>';
  h+='</div>';"""
if old2 in h:
    h = h.replace(old2, new2, 1)
    print('OK 成长柱状图')
else:
    print('MISS 成长柱状图')

open(FP, 'w', encoding='utf-8').write(h)
print('done')
