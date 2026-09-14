# -*- coding: utf-8 -*-
"""把全站外链图片改为自托管本地路径（assets/img/），并为详情页图片补 onerror 兜底"""
import io, sys, re, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

MAP = {
 'https://image.tmdb.org/t/p/w500/a1pMK4456dF2j5B9xvkjMEGiOOw.jpg': 'assets/img/a1pMK4456dF2j5B9xvkjMEGiOOw.jpg',
 'https://image.tmdb.org/t/p/w500/tEaeXZZO7SEcDr6yRP31UrrxcX0.jpg': 'assets/img/tEaeXZZO7SEcDr6yRP31UrrxcX0.jpg',
 'https://image.tmdb.org/t/p/w500/u7LWdKmEdEr6Ui3GZMsFGlKZQBd.jpg': 'assets/img/u7LWdKmEdEr6Ui3GZMsFGlKZQBd.jpg',
 'https://image.tmdb.org/t/p/w500/8uBae3fsFRhYNrNBxuWJCXlBFKE.jpg': 'assets/img/8uBae3fsFRhYNrNBxuWJCXlBFKE.jpg',
 'https://image.tmdb.org/t/p/w500/7AjIupf0lxNKNq0p8z36jv5ZpiJ.jpg': 'assets/img/7AjIupf0lxNKNq0p8z36jv5ZpiJ.jpg',
 'https://paultan.org/cn/image/2023/11/Zeekr-007-2-e1700100010257-630x330.jpg': 'assets/img/Zeekr_007_2_e1700100010257_630x330.jpg',
 'https://c2.gasgoo.com/autonews/moblogo/News/UEditor/image/20240611/6385371600188037263856413.png': 'assets/img/xiaopeng_mona_m03.jpg',
}

total = 0
for f in ['index.html', 'daily_data.js', 'detail_content.js']:
    p = os.path.join(BASE, f)
    t = open(p, encoding='utf-8').read()
    n = 0
    for old, new in MAP.items():
        c = t.count(old)
        if c:
            t = t.replace(old, new); n += c
    if n:
        open(p, 'w', encoding='utf-8').write(t)
    print('  %-20s 替换 %d 处' % (f, n))
    total += n
print('合计替换 %d 处 → 全部改为自托管' % total)

# ---------- 详情页图片补 onerror 兜底 ----------
FP = os.path.join(BASE, 'detail_content.js')
t = open(FP, encoding='utf-8').read()
old_img = '<img class="img-thumb" loading="lazy" src="'
new_img = '<img class="img-thumb" loading="lazy" onerror="this.style.display=\'none\'" src="'
if 'onerror' not in t:
    c = t.count(old_img)
    t = t.replace(old_img, new_img)
    open(FP, 'w', encoding='utf-8').write(t)
    print('  detail_content.js：%d 个 <img> 已补 onerror 兜底' % c)
else:
    print('  detail_content.js 已有 onerror')

# ---------- 校验 ----------
import subprocess
for f in ['daily_data.js', 'detail_content.js']:
    r = subprocess.run(['node', '--check', os.path.join(BASE, f)], capture_output=True, text=True)
    print('  %-20s 语法 %s' % (f, 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:160]))
r = subprocess.run(['node', '-e', "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=[...h.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(x=>x[1]);let bad=0;for(const s of m){try{new Function(s)}catch(e){bad++}};console.log('index inline FAIL='+bad)"],
                   capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(' ', r.stdout.strip())

# 残留外链检查
left = set()
for f in ['index.html', 'daily_data.js', 'detail_content.js']:
    t = open(os.path.join(BASE, f), encoding='utf-8').read()
    for m in re.finditer(r'https?://[^\s"\'\\<>()]+?\.(?:jpg|jpeg|png|webp|gif|avif)', t, re.I):
        left.add(m.group(0))
print()
print('残留外部图片 URL：%d 个' % len(left))
for u in left:
    print('   ' + u[:100])
