# -*- coding: utf-8 -*-
"""把新模型补录同步到 ai-track 与 news"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

ADD = ("<br><br><b>四、9-10 月模型层的大换血（评分表已补录到 20 个模型）</b><br>"
  "<b>① Claude 两条线同时更新</b>：Opus 5.5（9/22）拿下 AA 智能指数 <b>58 分</b>（榜上最高）——"
  "HLE 61.4%、SciCode 66.9%、十项评测六项领先，同时<b>降价 20%</b>（$5/$25 → $4/$20）、缓存读取降 60%；"
  "Sonnet 5.5（9/30）则出现罕见的「中杯反超大杯」：Terminal-Bench 4.0 达 <b>70.6%</b>，"
  "高于 Opus 5.5 的 66.4%，而价格只有一半（$2/$10）。<br>"
  "<b>② 谷歌重回前沿</b>：Gemini 4 Argon（10/13）刻意不谈参数量，只讲「软件工程 / 企业知识工作 / 网络防御」三个场景，"
  "API 限时五折——竞争焦点从跑分转向落地。<br>"
  "<b>③ OpenAI 补速度位</b>：GPT-6.1 Sol Ultrafast（10/9），在保留 Sol 推理能力的前提下拉高吞吐。<br>"
  "<b>④ 开源仍在追</b>：Reflection Beam（10/16）501B 开放权重、AA 智能指数 30，已是美国开放权重第 2，"
  "但距闭源前沿（58）仍有代差。<br>"
  "<b>⑤ 评价标准变了</b>：从「谁的跑分高」转向「完成一个任务要花多少钱」。"
  "Sonnet 5.5 只开 Medium effort 就超过 Sonnet 5 的最好成绩且成本不到 1/10；"
  "Opus 5.5 输出 token 是 GPT-6 Astra 的 4 倍多，但单任务成本持平。<br>"
  "<b>对你的影响：日常主力仍用 DeepSeek V4.1-Flash-1017（综合 91 分最高、闲时再减半），"
  "但「性价比 Coding」这一格已被 Claude Sonnet 5.5 抢走（88 分、Terminal-Bench 最高）。</b>")

# ---- ai-track.summary 追加 ----
i_ins = d.find('var INSIGHTS = {')
i_end = i_ins + re.search(r'\n\};', d[i_ins:]).end()
seg = d[i_ins:i_end]
pat = re.compile(r'((?:"ai-track"|ai-track)\s*:\s*\{)([\s\S]*?)(\n  \})')
m = pat.search(seg)
if m:
    body = m.group(2)
    sm = re.search(r'("?summary"?\s*:\s*)(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', body)
    if sm:
        cur = json.loads(sm.group(0).split(':', 1)[1].strip()) if sm.group(0).split(':',1)[1].strip().startswith('"') \
              else None
        if cur is None:
            print('⚠️  summary 不是双引号，改用标记追加')
            # 兜底：直接在原始字符串末尾（引号前）插入
            raw = sm.group(0)
            qwrap = raw[raw.index(':', 1)+1:].strip()
            inner = qwrap[1:-1]
            # 反转义判断
            newq = json.dumps(inner.replace('\\"', '"').replace("\\'", "'") + ADD, ensure_ascii=False)
            nb = body[:sm.start()] + sm.group(1) + newq + body[sm.end():]
        else:
            nb = body[:sm.start()] + sm.group(1) + json.dumps(cur + ADD, ensure_ascii=False) + body[sm.end():]
        seg = seg[:m.start()] + m.group(1) + nb + m.group(3) + seg[m.end():]
        d = d[:i_ins] + seg + d[i_end:]
        print('✅ ai-track.summary 已追加「模型层大换血」')
else:
    print('❌ 未找到 ai-track')

# ---- news.summary 追加 ----
i_ins = d.find('var INSIGHTS = {')
i_end = i_ins + re.search(r'\n\};', d[i_ins:]).end()
seg = d[i_ins:i_end]
pat = re.compile(r'((?:"news"|news)\s*:\s*\{)([\s\S]*?)(\n  \})')
m = pat.search(seg)
if m:
    body = m.group(2)
    sm = re.search(r'("?summary"?\s*:\s*)(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', body)
    if sm:
        raw = sm.group(0)
        q = raw[raw.index(':', 1)+1:].strip()
        inner = q[1:-1].replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
        addnews = ("<br>⑧ <b>模型层大换血（评分表已补录到 20 个模型）</b>："
          "Claude Opus 5.5（9/22·AA 智能指数 58 登顶·降价 20%）、"
          "Claude Sonnet 5.5（9/30·Terminal-Bench 70.6% 反超旗舰·价格一半）、"
          "Gemini 4 Argon（10/13·限时五折·转向「干活」）、"
          "GPT-6.1 Sol Ultrafast（10/9·速度优先）、Reflection Beam（10/16·501B 开放权重）。")
        nb = body[:sm.start()] + sm.group(1) + json.dumps(inner + addnews, ensure_ascii=False) + body[sm.end():]
        seg = seg[:m.start()] + m.group(1) + nb + m.group(3) + seg[m.end():]
        d = d[:i_ins] + seg + d[i_end:]
        print('✅ news.summary 已追加模型更新')

# ---- 版本 ----
d = d.replace('var SITE_VERSION = "1.8.25";', 'var SITE_VERSION = "1.8.26";')
d = re.sub(r'版本1\.8\.2[0-9]', '版本1.8.26', d)
print('✅ 版本 → 1.8.26')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:300])

IH = BASE + r'\index.html'
h = open(IH, 'r', encoding='utf-8').read()
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.26', h)
open(IH, 'w', encoding='utf-8').write(h)
print('✅ index.html 引用 → 1.8.26')
