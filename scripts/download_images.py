# -*- coding: utf-8 -*-
"""下载全站图片到 assets/img/ 并输出视觉复核清单
   关键：HTTP 200 + 合法 JPEG ≠ 真图（可能是"图片过期"占位图），必须看图
"""
import io, sys, os, re, ssl, json, hashlib, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
OUT = os.path.join(BASE, 'assets', 'img')
os.makedirs(OUT, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

from PIL import Image

MANIFEST = json.load(open(os.path.join(BASE, 'scripts', '_image_manifest.json'), encoding='utf-8'))
ok = [m for m in MANIFEST if m['status'] == 200 and m['ctype'].startswith('image')]

# 旧图（含失效的 gasgoo）
targets = [(m['url'], None) for m in ok]
targets.append(('https://c2.gasgoo.com/autonews/moblogo/News/UEditor/image/20240611/6385371600188037263856413.png', 'xiaopeng_m03'))

REPORT = []
for url, forced_name in targets:
    name = forced_name or re.sub(r'[^A-Za-z0-9]+', '_', url.split('/')[-1].rsplit('.', 1)[0])[:40]
    ext = '.jpg' if url.lower().endswith(('.jpg', '.jpeg')) else ('.png' if url.lower().endswith('.png') else '.jpg')
    path = os.path.join(OUT, name + ext)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': url.split('/')[0] + '//' + url.split('/')[2] + '/'})
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            data = r.read()
            ctype = r.headers.get('Content-Type', '')
        if not ctype.startswith('image'):
            raise ValueError('Content-Type=%s' % ctype)
        open(path, 'wb').write(data)
        im = Image.open(path); im.load()
        # 启发式"疑似占位图"判定：尺寸固定 640x480 且体积极小
        suspect = (len(data) < 15000) or (im.size == (640, 480) and len(data) < 20000)
        REPORT.append({'name': name + ext, 'url': url, 'path': path, 'kb': round(len(data) / 1024, 1),
                       'size': im.size, 'md5': hashlib.md5(data).hexdigest()[:10], 'suspect': suspect})
        print('  %s %-34s %sx%s %6.1fKB %s' % ('⚠️' if suspect else '✅', name + ext, im.size[0], im.size[1], len(data) / 1024,
                                               '疑似占位图！' if suspect else ''))
    except Exception as e:
        print('  ❌ %-34s 下载/解析失败: %s' % (name, str(e)[:70]))
        REPORT.append({'name': name, 'url': url, 'path': None, 'error': str(e)[:120]})

json.dump(REPORT, open(os.path.join(BASE, 'scripts', '_image_report.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print()
print('已下载 %d 张到 assets/img/ ；报告：scripts/_image_report.json' % len([r for r in REPORT if r.get('path')]))
print('疑似占位图：%d 张' % len([r for r in REPORT if r.get('suspect')]))
