# -*- coding: utf-8 -*-
"""视觉体检：多视口 × 多板块
   ① 程序化检测：横向溢出 / 超宽元素 / 图片加载失败 / 图片高度异常 / 文本截断
   ② 输出需人工看图的清单（多模态复核）
"""
import io, sys, os, re, json, time, subprocess, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# 板块：detail key（None=首页）
SECTIONS = [
    (None, '首页'),
    ('fashion', '穿搭'), ('anime', '动漫'), ('movie', '影视'),
    ('fitness', '健身'), ('diet', '饮食'), ('car', '购车'),
    ('stock', '股市'), ('career', '求职'), ('learning', '学习'),
]
VIEWPORTS = [(1440, 900, '桌面'), (768, 1000, '平板'), (390, 844, '手机')]

AUDIT_JS = r'''
<script>
window.addEventListener("load", function(){
  setTimeout(function(){
    var W = window.innerWidth;
    var out = {vw: W, vh: window.innerHeight,
               scrollW: document.documentElement.scrollWidth, issues: []};
    function push(s){ if(out.issues.length < 25) out.issues.push(s); }
    // 横向溢出
    if (document.documentElement.scrollWidth > W + 2) {
      push("页面横向溢出：scrollWidth=" + document.documentElement.scrollWidth + " > " + W);
      var seen = 0;
      document.querySelectorAll("body *").forEach(function(el){
        if (seen >= 6) return;
        var r = el.getBoundingClientRect();
        if (r.width > W + 2 && r.height > 4 && el.offsetParent !== null) {
          seen++;
          var cn = (typeof el.className === "string" ? el.className : "").slice(0, 34);
          push("  超宽元素 <" + el.tagName.toLowerCase() + " class=\"" + cn + "\"> w=" + Math.round(r.width));
        }
      });
    }
    // 图片
    document.querySelectorAll("img").forEach(function(im){
      var src = im.getAttribute("src") || "";
      if (!im.complete) return;
      if (im.naturalWidth === 0) push("图片加载失败：" + src.slice(0, 70));
      else {
        var r = im.getBoundingClientRect();
        if (r.height < 8 && r.width > 0) push("图片高度异常(" + Math.round(r.height) + "px)：" + src.slice(0, 60));
        var ar = im.naturalWidth / im.naturalHeight;
        var box = r.width / Math.max(r.height, 1);
        if (box > 0 && ar > 0 && Math.abs(Math.log(box / ar)) > 0.75) {
          push("图片裁切比例失真(原 " + ar.toFixed(2) + " vs 容器 " + box.toFixed(2) + ")：" + src.slice(0, 55));
        }
      }
    });
    // 卡片文字溢出
    var ov = 0;
    document.querySelectorAll(".img-card .img-title, .img-card .img-desc, .pick-title").forEach(function(el){
      if (ov >= 4) return;
      if (el.scrollHeight > el.clientHeight + 3 && el.clientHeight > 0) {
        ov++; push("文字被截断：" + (el.textContent || "").slice(0, 34));
      }
    });
    var pre = document.createElement("pre");
    pre.id = "AUDIT_OUT";
    pre.textContent = "AUDITJSON:" + JSON.stringify(out);
    document.body.appendChild(pre);
    document.title = "AUDIT_DONE";
  }, 2600);
});
</script>
'''

h = open(os.path.join(BASE, 'index.html'), encoding='utf-8').read()
i = h.rfind('</body>')

tmpdir = tempfile.mkdtemp()
results = []
print('=== 视觉体检：%d 板块 × %d 视口 ===' % (len(SECTIONS), len(VIEWPORTS)))

for key, label in SECTIONS:
    open_call = ('<script>window.addEventListener("load",function(){setTimeout(function(){try{openDetail("%s")}catch(e){}},1600);});</script>' % key) if key else ''
    html = h[:i] + open_call + AUDIT_JS + h[i:]
    fp = os.path.join(tmpdir, ('t_%s.html' % (key or 'home')))
    open(fp, 'w', encoding='utf-8').write(html)
    url = 'file:///' + fp.replace('\\', '/')
    for (w, hh, vlabel) in VIEWPORTS:
        out = os.path.join(tmpdir, 'o_%s_%d.html' % (key or 'home', w))
        err = out + '.err'
        p = subprocess.Popen([EDGE, '--headless=new', '--disable-gpu', '--dump-dom',
                              '--window-size=%d,%d' % (w, hh), '--virtual-time-budget=12000', url],
                             stdout=open(out, 'w', encoding='utf-8', errors='replace'),
                             stderr=open(err, 'w', encoding='utf-8', errors='replace'))
        p.wait(timeout=90)
        try:
            dom = open(out, encoding='utf-8', errors='replace').read()
        except Exception:
            dom = ''
        m = re.search(r'AUDITJSON:(\{.*?\})</pre>', dom, re.S)
        if m:
            try:
                d = json.loads(m.group(1))
            except Exception:
                d = {'issues': ['解析失败']}
        else:
            d = {'issues': ['未取到审计结果（页面可能未渲染）']}
        d['section'] = label; d['viewport'] = vlabel; d['w'] = w
        results.append(d)
        tag = '✅' if not d.get('issues') else ('❌ %d 项' % len(d['issues']))
        print('  %-6s %-4s %s' % (label, vlabel, tag))
        for s in d.get('issues', []):
            print('        · ' + s)

json.dump(results, open(os.path.join(BASE, 'scripts', '_visual_audit.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
bad = [r for r in results if r.get('issues')]
print()
print('=== 汇总：%d/%d 个组合有问题 ===' % (len(bad), len(results)))
