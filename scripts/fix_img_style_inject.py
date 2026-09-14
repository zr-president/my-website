# -*- coding: utf-8 -*-
"""修正：详情页静态图片卡注入主色（src 在 <a> 之后的 <img> 里，需连带匹配）"""
import io, sys, os, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
STYLE = json.load(open(os.path.join(BASE, 'scripts', '_img_style.json'), encoding='utf-8'))

FP = os.path.join(BASE, 'detail_content.js')
t = open(FP, encoding='utf-8').read()
n = 0


def inject(m):
    global n
    whole = m.group(0)
    if '--ic:' in whole:          # 已处理
        return whole
    src = m.group(2)
    base = os.path.basename(src)
    st = STYLE.get(base)
    if st:
        props = '--ic:%s;--ip:%s;--if:%s;--icf:%s1f;' % (st['accent'], st['objectPosition'], st['darkAdjust'], st['accent'])
    elif src.lower().endswith('.svg'):
        # SVG 插图本身跟随主题色 → 用主题强调色
        props = '--ic:var(--accent);--ip:center 50%;--if:none;--icf:transparent;'
    else:
        return whole
    n += 1
    # 把属性插到 style=" 之后；若 <a> 没有 style 则补一个
    if re.search(r'<a class="img-card"[^>]*style="', whole):
        return whole.replace('style="', 'style="' + props, 1)
    return whole.replace('<a class="img-card"', '<a class="img-card" style="' + props + '"', 1)


t2 = re.sub(r'(<a class="img-card"[^>]*>\s*<img[^>]+src="([^"]+)")', inject, t)
if t2 != t:
    open(FP, 'w', encoding='utf-8').write(t2)
print('详情页静态图片卡：注入 %d 个' % n)

# 同时处理 index.html 里可能存在的静态 img-card
FP2 = os.path.join(BASE, 'index.html')
h = open(FP2, encoding='utf-8').read()
n2 = 0


def inject2(m):
    global n2
    whole = m.group(0)
    if '--ic:' in whole:
        return whole
    src = m.group(2)
    st = STYLE.get(os.path.basename(src))
    if st:
        props = '--ic:%s;--ip:%s;--if:%s;--icf:%s1f;' % (st['accent'], st['objectPosition'], st['darkAdjust'], st['accent'])
    elif src.lower().endswith('.svg'):
        props = '--ic:var(--accent);--ip:center 50%;--if:none;--icf:transparent;'
    else:
        return whole
    n2 += 1
    if re.search(r'<a class="img-card"[^>]*style="', whole):
        return whole.replace('style="', 'style="' + props, 1)
    return whole.replace('<a class="img-card"', '<a class="img-card" style="' + props + '"', 1)


h2 = re.sub(r'(<a class="img-card"[^>]*>\s*<img[^>]+src="([^"]+)")', inject2, h)
if h2 != h:
    open(FP2, 'w', encoding='utf-8').write(h2)
print('index.html 静态图片卡：注入 %d 个' % n2)

for f in ['detail_content.js', 'img_style.js']:
    r = subprocess.run(['node', '--check', os.path.join(BASE, f)], capture_output=True, text=True)
    print('  %-18s %s' % (f, 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:150]))
r = subprocess.run(['node', '-e', "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=[...h.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(x=>x[1]);let bad=0;for(const s of m){try{new Function(s)}catch(e){bad++}};console.log('index inline FAIL='+bad)"],
                   capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(' ', r.stdout.strip())

# 统计
cnt = len(re.findall(r'--ic:', open(FP, encoding='utf-8').read()))
print()
print('detail_content.js 中已带 --ic 的图片卡：%d 个' % cnt)
