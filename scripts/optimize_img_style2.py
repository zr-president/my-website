# -*- coding: utf-8 -*-
"""图片样式优化（第二批）
   ① WebP 转换 + 压缩（体积对比）
   ② 统一色调：所有实拍图叠一层极淡的主题色渐变，消除"素材拼凑感"
   ③ 加载淡入：避免灰块闪烁
"""
import io, sys, os, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
from PIL import Image

# ---------- ① WebP 转换 ----------
print('=== ① WebP 转换 ===')
IMG_DIR = os.path.join(BASE, 'assets', 'img')
total_before = total_after = 0
converted = {}
for name in sorted(os.listdir(IMG_DIR)):
    if not name.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    src = os.path.join(IMG_DIR, name)
    before = os.path.getsize(src)
    stem = os.path.splitext(name)[0]
    dst = os.path.join(IMG_DIR, stem + '.webp')
    try:
        im = Image.open(src).convert('RGB')
        # 限制最大边 900px（卡片显示宽度远小于此，够清晰且更小）
        im.thumbnail((900, 900), Image.LANCZOS)
        im.save(dst, 'WEBP', quality=82, method=6)
        after = os.path.getsize(dst)
        total_before += before
        total_after += after
        converted['assets/img/' + name] = 'assets/img/' + stem + '.webp'
        print('  %-46s %6.1fKB → %6.1fKB  (-%d%%)' % (
            name[:46], before / 1024, after / 1024, round((1 - after / before) * 100)))
    except Exception as e:
        print('  ❌ %s: %s' % (name, str(e)[:60]))

print('  合计：%.0fKB → %.0fKB，节省 %.0fKB（-%.0f%%）' % (
    total_before / 1024, total_after / 1024, (total_before - total_after) / 1024,
    (1 - total_after / total_before) * 100 if total_before else 0))

# 替换引用
n = 0
for f in ['index.html', 'daily_data.js', 'detail_content.js', 'img_style.js']:
    p = os.path.join(BASE, f)
    t = open(p, encoding='utf-8').read()
    c = 0
    for old, new in converted.items():
        if old in t:
            c += t.count(old); t = t.replace(old, new)
    if c:
        open(p, 'w', encoding='utf-8').write(t)
    n += c
    print('  %-20s 替换 %d 处' % (f, c))

# img_style.js 的键也要换名
p = os.path.join(BASE, 'img_style.js')
t = open(p, encoding='utf-8').read()
for old, new in converted.items():
    t = t.replace('"' + old + '"', '"' + new + '"')
open(p, 'w', encoding='utf-8').write(t)
print('  img_style.js 键名已同步')

# 保留原图作为无损备份？删除以减小仓库
for name in list(os.listdir(IMG_DIR)):
    if name.lower().endswith(('.jpg', '.jpeg', '.png')):
        os.remove(os.path.join(IMG_DIR, name))
print('  原始 JPG/PNG 已删除（保留 WebP）')

# ---------- ②③ CSS：统一色调 + 加载淡入 ----------
FP = os.path.join(BASE, 'index.html')
h = open(FP, encoding='utf-8').read()

CSS2 = '''/* ===== 图片统一色调 + 加载淡入（消除多源素材的拼凑感）===== */
.img-card .img-thumb{
  filter:saturate(.96) contrast(1.03);
  opacity:0;transition:opacity .45s ease,transform .38s ease,filter .3s}
.img-card .img-thumb.loaded{opacity:1}
[data-theme="dark"] .img-card .img-thumb{filter:saturate(.94) contrast(1.02) var(--if,none);}
/* 底部叠一层极淡的卡片主色，让图片与文字区同色系 */
.img-card::after{content:'';position:absolute;left:0;right:0;top:0;aspect-ratio:4/3;
  pointer-events:none;border-radius:12px 12px 0 0;
  background:linear-gradient(180deg,transparent 62%,var(--icf,rgba(0,0,0,0)) 100%)}
'''
if '统一色调' not in h:
    anchor = '/* ===== 图片卡片：窄屏适配'
    h = h.replace(anchor, CSS2 + anchor, 1)
    print('② 已加统一色调与淡入样式')
else:
    print('② 样式已存在')

# 淡入脚本：图片加载完成后加 .loaded
FADE_JS = '''<script>
// 图片加载完成后淡入（避免灰块闪烁）
(function(){
  function mark(im){ if(im.complete && im.naturalWidth>0){ im.classList.add('loaded'); } }
  function scan(){
    document.querySelectorAll('.img-thumb:not(.loaded)').forEach(function(im){
      if(im.complete){ mark(im); } else { im.addEventListener('load',function(){im.classList.add('loaded')},{once:true}); }
    });
  }
  if(document.readyState!=='loading') setTimeout(scan,300);
  document.addEventListener('DOMContentLoaded',function(){setTimeout(scan,600)});
  window.addEventListener('load',function(){setTimeout(scan,300)});
  setInterval(scan,2500);
  window.zh_markImgs = scan;
})();
</script>
'''
if 'zh_markImgs' not in h:
    idx = h.rfind('</body>')
    h = h[:idx] + FADE_JS + h[idx:]
    print('③ 已加图片淡入脚本')
else:
    print('③ 淡入脚本已存在')

open(FP, 'w', encoding='utf-8').write(h)

for f in ['daily_data.js', 'detail_content.js', 'img_style.js']:
    r = subprocess.run(['node', '--check', os.path.join(BASE, f)], capture_output=True, text=True)
    print('  %-18s %s' % (f, 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:120]))
r = subprocess.run(['node', '-e', "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=[...h.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(x=>x[1]);let bad=0;for(const s of m){try{new Function(s)}catch(e){bad++}};console.log('index inline FAIL='+bad)"],
                   capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(' ', r.stdout.strip())
