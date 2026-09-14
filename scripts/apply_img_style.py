# -*- coding: utf-8 -*-
"""多模态驱动的图片样式优化：
   ① 生成 img_style.js（每张图的主色 / 裁切位 / 暗色滤镜）
   ② CSS：图片卡片统一设计语言（主色顶线、悬停光晕、渐变过渡、暗色自适应）
   ③ 渲染器：图片卡应用主色与 object-position
   ④ 详情页静态图片卡：注入同样的自定义属性
"""
import io, sys, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

STYLE = json.load(open(os.path.join(BASE, 'scripts', '_img_style.json'), encoding='utf-8'))

# ---------- ① 生成 img_style.js ----------
items = {}
for name, v in STYLE.items():
    items[v['dir'] + '/' + name] = {
        'c': v['accent'], 'p': v['objectPosition'], 'd': v['darkAdjust'], 'l': v['luminance']
    }
js = ('// 图片视觉属性（由 scripts/analyze_img_style2.py 从图片本身提取主色后生成）\n'
      '// c=主色  p=推荐 object-position（避免裁掉主体）  d=暗色模式滤镜  l=平均亮度\n'
      'var IMG_STYLE = ' + json.dumps(items, ensure_ascii=False, indent=1) + ';\n')
open(os.path.join(BASE, 'img_style.js'), 'w', encoding='utf-8').write(js)
print('① 已生成 img_style.js（%d 张）' % len(items))

# ---------- ② CSS ----------
FP = os.path.join(BASE, 'index.html')
h = open(FP, encoding='utf-8').read()

CSS = '''/* ===== 图片卡片统一设计语言（多模态主色驱动）===== */
.img-picks{display:grid;grid-template-columns:repeat(auto-fill,minmax(196px,1fr));gap:11px}
.img-card{position:relative;display:flex;flex-direction:column;background:var(--card);
  border:1px solid var(--border);border-top:2px solid var(--ic,var(--border));
  border-radius:12px;overflow:hidden;text-decoration:none;color:var(--text);
  transition:transform .22s cubic-bezier(.2,.7,.3,1),border-color .22s,box-shadow .28s;
  box-shadow:var(--shadow)}
.img-card:hover{transform:translateY(-4px);border-color:var(--ic,var(--accent));
  box-shadow:0 12px 30px -10px rgba(0,0,0,.28),0 0 0 1px var(--ic,var(--accent)) inset}
.img-card .img-thumb{width:100%;aspect-ratio:4/3;object-fit:cover;
  object-position:var(--ip,center 50%);background:var(--bg2);display:block;
  transition:transform .38s ease,filter .3s}
.img-card:hover .img-thumb{transform:scale(1.05)}
[data-theme="dark"] .img-card .img-thumb{filter:var(--if,none)}
/* 图片到文字的过渡：用主色做一层极淡的渐变，替代生硬的切边 */
.img-card .img-body{padding:10px 12px 11px;position:relative;
  background:linear-gradient(180deg,var(--icf,rgba(128,128,128,.05)) 0%,var(--card) 46%)}
.img-card .img-title{font-size:12.5px;font-weight:700;margin-bottom:4px;line-height:1.45}
.img-card .img-desc{font-size:10.5px;color:var(--text2);line-height:1.65}
.img-card .img-tag{display:inline-block;margin-top:6px;padding:1.5px 8px;border-radius:8px;
  font-size:9.5px;font-weight:700;background:var(--icf,rgba(128,128,128,.12));color:var(--ic,var(--accent))}
/* 竖版海报：给顶部叠一层非常淡的暗角，让标题区更稳 */
.img-card.portrait .img-thumb{mask-image:linear-gradient(180deg,#000 78%,rgba(0,0,0,.86) 100%)}
'''

if '图片卡片统一设计语言' not in h:
    # 插到 .img-thumb 原规则之后
    old_css = '<style>'
    idx = h.find('.img-picks{display:grid')
    if idx > 0:
        # 找到该段 CSS 结尾（下一个换行后的规则结束）
        end = h.find('\n', h.find('.img-thumb{', idx))
        # 覆盖旧规则：先删掉旧的三行
        seg_end = h.find('.img-thumb{width:100%;aspect-ratio:4/3;object-fit:cover;background:var(--bg2);display:block}')
        if seg_end > 0:
            seg_end += len('.img-thumb{width:100%;aspect-ratio:4/3;object-fit:cover;background:var(--bg2);display:block}')
            h = h[:seg_end] + '\n' + CSS + h[seg_end:]
            print('② 已插入图片卡片 CSS（覆盖旧规则）')
        else:
            h = h.replace('<style>', '<style>\n' + CSS, 1)
            print('② 已插入图片卡片 CSS（追加）')
    else:
        print('② MISS .img-picks')
else:
    print('② CSS 已存在')

# ---------- ③ 渲染器：应用主色 / 裁切位 ----------
old_r = ("        h+='<'+tag+' '+(hasLink?'href=\"'+p.link+'\" target=\"_blank\" ':'')+'class=\"img-card\">';\n"
         "        h+='<img class=\"img-thumb\" loading=\"lazy\" src=\"'+p.img+'\" alt=\"'+p.title+'\" onerror=\"this.style.display=\\'none\\'\">';")
new_r = ("        var st = (typeof IMG_STYLE!=='undefined' && IMG_STYLE[p.img]) ? IMG_STYLE[p.img] : null;\n"
         "        var cst = st ? ('--ic:'+st.c+';--ip:'+st.p+';--if:'+st.d+';--icf:'+st.c+'1f;') : '';\n"
         "        h+='<'+tag+' '+(hasLink?'href=\"'+p.link+'\" target=\"_blank\" ':'')+'class=\"img-card\" style=\"'+cst+'\">';\n"
         "        h+='<img class=\"img-thumb\" loading=\"lazy\" src=\"'+p.img+'\" alt=\"'+p.title+'\" onerror=\"this.style.display=\\'none\\'\">';")
if old_r in h:
    h = h.replace(old_r, new_r, 1)
    print('③ 渲染器已应用主色与裁切位')
else:
    print('③ MISS 渲染器锚点')

# 引入 img_style.js
if 'img_style.js' not in h:
    h = h.replace('<script defer src="daily_data.js', '<script defer src="img_style.js?v=1.8.15"></script>\n<script defer src="daily_data.js', 1)
    print('③ 已引入 img_style.js')

open(FP, 'w', encoding='utf-8').write(h)

# ---------- ④ 详情页静态图片卡 ----------
FP2 = os.path.join(BASE, 'detail_content.js')
t = open(FP2, encoding='utf-8').read()
n = 0


def add_style(m):
    global n
    tag = m.group(0)
    src = re.search(r'src="([^"]+)"', tag)
    if not src:
        return tag
    key = src.group(1)
    st = STYLE.get(os.path.basename(key))
    if not st:
        return tag
    n += 1
    props = '--ic:%s;--ip:%s;--if:%s;--icf:%s1f;' % (st['accent'], st['objectPosition'], st['darkAdjust'], st['accent'])
    if 'class="img-card"' in tag and 'style="' in tag:
        return tag.replace('class="img-card" style="', 'class="img-card" style="' + props, 1)
    return tag


t2 = re.sub(r'<a class="img-card"[^>]*>', add_style, t)
if t2 != t:
    open(FP2, 'w', encoding='utf-8').write(t2)
print('④ 详情页静态图片卡：%d 个已注入主色属性' % n)

# ---------- 校验 ----------
import subprocess
for f in ['daily_data.js', 'detail_content.js', 'img_style.js']:
    r = subprocess.run(['node', '--check', os.path.join(BASE, f)], capture_output=True, text=True)
    print('  %-18s %s' % (f, 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:150]))
r = subprocess.run(['node', '-e', "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=[...h.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(x=>x[1]);let bad=0;for(const s of m){try{new Function(s)}catch(e){bad++}};console.log('index inline FAIL='+bad)"],
                   capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(' ', r.stdout.strip())
