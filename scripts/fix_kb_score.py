# -*- coding: utf-8 -*-
"""修 kbScore 的相关性 bug：单字关键词被子串匹配放大
   现象：查「拿铁」命中关键词「铁」（铁元素），因为 "拿铁".indexOf("铁") = 1 ≥ 0 → 85 分。
   修法：
   - kw === qLower 仍给 100（精确）
   - 子串匹配要求 kw.length >= 2（单字关键词只允许精确命中）
   - info 包含要求 qLower.length >= 2（避免单字全文扫）
   - token 匹配也要求 token.length >= 2
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, encoding='utf-8').read()

OLD = """function kbScore(entry, qLower, tokens){
  var kw = String(entry.keyword||'').toLowerCase();
  var info = String(entry.info||'').toLowerCase();
  var s = 0;
  if(kw === qLower) s = 100;
  else if(qLower.indexOf(kw) >= 0 || kw.indexOf(qLower) >= 0) s = 85;
  else if(info.indexOf(qLower) >= 0) s = 70;
  else {
    var hit = 0;
    for(var i=0;i<tokens.length;i++){
      var t = tokens[i];
      if(kw.indexOf(t) >= 0) hit += 2;
      else if(info.indexOf(t) >= 0) hit += 1;
    }
    if(hit > 0) s = Math.min(60, 20 + hit * 8);
  }
  return s;
}"""

NEW = """function kbScore(entry, qLower, tokens){
  var kw = String(entry.keyword||'').toLowerCase();
  var info = String(entry.info||'').toLowerCase();
  var s = 0;
  if(kw === qLower) s = 100;
  /* 子串匹配要求关键词至少 2 个字：否则单字关键词（如「铁」）会被
     「拿铁」这类查询误命中，相关性直接崩掉 */
  else if(kw.length >= 2 && (qLower.indexOf(kw) >= 0 || kw.indexOf(qLower) >= 0)) s = 85;
  else if(qLower.length >= 2 && info.indexOf(qLower) >= 0) s = 70;
  else {
    var hit = 0;
    for(var i=0;i<tokens.length;i++){
      var t = tokens[i];
      if(t.length < 2) continue;
      if(kw.indexOf(t) >= 0) hit += 2;
      else if(info.indexOf(t) >= 0) hit += 1;
    }
    if(hit > 0) s = Math.min(60, 20 + hit * 8);
  }
  return s;
}"""

if 'kw.length >= 2' in h:
    print('ℹ️  已修过')
elif OLD in h:
    h = h.replace(OLD, NEW, 1)
    open(FP, 'w', encoding='utf-8').write(h)
    print('✅ kbScore 已修复')
else:
    print('❌ 未匹配到 kbScore 原文')
    i = h.find('function kbScore')
    print(repr(h[i:i+700]) if i > 0 else '未找到')

h2 = open(FP, encoding='utf-8').read()
print()
for k in ['kw.length >= 2', "if(t.length < 2) continue", 'qLower.length >= 2']:
    print('  含 %-26s %s' % (k, k in h2))
