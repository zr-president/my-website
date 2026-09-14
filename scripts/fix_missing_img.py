# -*- coding: utf-8 -*-
"""修复缺图卡片：
   ① 渲染器：无 img 时输出设计感占位块（同高，保持网格整齐），不再产生 src=undefined
   ② .img-card::after 只作用于"确实含图"的卡片（:has）
"""
import io, sys, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- ① 渲染器 ----------
old = ("        h+='<img class=\"img-thumb\" loading=\"lazy\" src=\"'+p.img+'\" alt=\"'+p.title+'\" onerror=\"this.style.display=\\'none\\'\">';")
new = ("        if(p.img){\n"
       "          h+='<img class=\"img-thumb\" loading=\"lazy\" src=\"'+p.img+'\" alt=\"'+p.title+'\" onerror=\"this.style.display=\\'none\\'\">';\n"
       "        } else {\n"
       "          /* #多模态：该卡片没有配图 → 用同高的设计感占位块，保持网格整齐且不出现破图 */\n"
       "          h+='<div class=\"img-ph\"><span>'+(p.icon||'📌')+'</span><em>'+(p.tag||'')+'</em></div>';\n"
       "        }")
if old in h:
    h = h.replace(old, new, 1)
    print('① 渲染器已修复：缺图卡片改用占位块')
else:
    print('① MISS 渲染器锚点')

# ---------- CSS：占位块样式 + :has 限定 ----------
CSS3 = '''/* 无配图卡片的设计感占位块（与图片同为 4:3，保持网格整齐） */
.img-card .img-ph{width:100%;aspect-ratio:4/3;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:6px;
  background:linear-gradient(135deg,var(--accent-light) 0%,var(--bg2) 70%,var(--card) 100%)}
.img-card .img-ph span{font-size:36px;line-height:1;filter:drop-shadow(0 3px 6px rgba(0,0,0,.10))}
.img-card .img-ph em{font-style:normal;font-size:9.5px;font-weight:700;letter-spacing:.4px;
  color:var(--accent);opacity:.85}
.img-card:hover .img-ph span{transform:scale(1.08);transition:transform .3s ease}
'''
if 'img-ph' not in h:
    anchor = '/* ===== 图片统一色调 + 加载淡入'
    if anchor in h:
        h = h.replace(anchor, CSS3 + anchor, 1)
        print('② 已加占位块样式')
    else:
        h = h.replace('<style>', '<style>\n' + CSS3, 1)
        print('② 已加占位块样式（追加）')

# :has 限定 ::after 只作用于含图卡片
n = h.count('.img-card::after{content:')
if n:
    h = h.replace('.img-card::after{content:', '.img-card:has(.img-thumb)::after{content:')
    print('③ ::after 已限定为仅含图卡片（%d 处）' % n)

open(FP, 'w', encoding='utf-8').write(h)

r = subprocess.run(['node', '-e', "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=[...h.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(x=>x[1]);let bad=0;for(const s of m){try{new Function(s)}catch(e){bad++;console.log(e.message)}};console.log('index inline FAIL='+bad)"],
                   capture_output=True, text=True, encoding='utf-8', cwd=r'C:\Users\ZR\Desktop\钟锐的个人网站')
print(r.stdout.strip())
