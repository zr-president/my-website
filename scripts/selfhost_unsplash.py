# -*- coding: utf-8 -*-
"""图片彻底自托管：
   ① 穿搭两张 → 改用已有的本地 SVG 插图（外链实拍图与标注不符）
   ② 其余 Unsplash 图全部下载到 assets/img/ 并替换为本地路径
"""
import io, sys, os, re, ssl, json, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
OUT = os.path.join(BASE, 'assets', 'img')
os.makedirs(OUT, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
from PIL import Image

FILES = ['index.html', 'daily_data.js', 'detail_content.js']
texts = {f: open(os.path.join(BASE, f), encoding='utf-8').read() for f in FILES}

# ---------- 收集所有 Unsplash URL（忽略尺寸参数，按 photo id 归一）----------
pat = re.compile(r'https://images\.unsplash\.com/(photo-[0-9a-zA-Z\-]+)\?[^\s"\'\\<>()]*')
ids = {}
for f, t in texts.items():
    for m in pat.finditer(t):
        ids.setdefault(m.group(1), set()).add(f)
print('=== 待自托管的 Unsplash 图：%d 张 ===' % len(ids))

# 已核实"与标注不符"的两张穿搭图 → 用本地 SVG
SVG_SWAP = {
 'photo-1617137968427-85924c800a22': 'img/fashion_jp.svg',
 'photo-1593030761757-71fae45fa0e7': 'img/fashion_kr.svg',
}

mapping = {}   # 整条 URL 前缀正则 -> 本地路径
for pid in ids:
    if pid in SVG_SWAP:
        mapping[pid] = SVG_SWAP[pid]
        print('  🔁 %s → %s（外链图与标注不符，改用本地插图）' % (pid[:34], SVG_SWAP[pid]))
        continue
    # 下载最大尺寸
    url = 'https://images.unsplash.com/%s?auto=format&fit=crop&w=800&q=70' % pid
    name = pid.replace('photo-', '')[:26] + '.jpg'
    path = os.path.join(OUT, name)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            d = r.read()
        open(path, 'wb').write(d)
        im = Image.open(path); im.load()
        mapping[pid] = 'assets/img/' + name
        print('  ✅ %-30s %sx%s %6.1fKB → assets/img/%s' % (pid[:30], im.size[0], im.size[1], len(d) / 1024, name))
    except Exception as e:
        print('  ❌ %-30s 下载失败: %s' % (pid[:30], str(e)[:60]))

# ---------- 替换 ----------
print()
for f in FILES:
    t = texts[f]
    n = 0
    for pid, local in mapping.items():
        # 匹配该 photo id 的整条 URL（含 query）
        rx = re.compile(re.escape('https://images.unsplash.com/' + pid) + r'\?[^\s"\'\\<>()]*')
        t, c = rx.subn(local, t)
        n += c
    if n:
        open(os.path.join(BASE, f), 'w', encoding='utf-8').write(t)
    print('  %-20s 替换 %d 处' % (f, n))

# ---------- 校验 ----------
import subprocess
for f in ['daily_data.js', 'detail_content.js']:
    r = subprocess.run(['node', '--check', os.path.join(BASE, f)], capture_output=True, text=True)
    print('  %-20s 语法 %s' % (f, 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:150]))

left = set()
for f in FILES:
    t = open(os.path.join(BASE, f), encoding='utf-8').read()
    for m in re.finditer(r'https?://images\.unsplash\.com/[^\s"\'\\<>()]+', t):
        left.add(m.group(0))
print()
print('残留 Unsplash 外链：%d' % len(left))
for u in left:
    print('   ' + u[:90])
