# -*- coding: utf-8 -*-
"""2026-09-12 剩余更新：movie(国庆档)/anime(追番第31天) + 其余板块日期推进 + DAILY_DECISIONS + AI_OBSERVATIONS"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
content = open(FP, 'r', encoding='utf-8').read()

def esc(v):
    return v.replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")

def replace_section(key, verdict='', summary='', trend='', tip='', reasoning=''):
    global content
    m = re.search(r'(?m)^  ' + re.escape(key) + r':\s*\{', content)
    if not m:
        print('MISS:', key); return
    i = m.start(); j = i; depth = 0; L = len(content); inq = False; q = ''
    while j < L:
        ch = content[j]
        if inq:
            if ch == q: inq = False
            elif ch == '\\': j += 1
        elif ch in ("'", '"'):
            inq = True; q = ch
        elif ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: break
        j += 1
    end = j + 1
    while end < L and content[end] == ',': end += 1
    lines = ['  ' + key + ': {']
    for k, v in [('verdict', verdict), ('summary', summary), ('trend', trend), ('tip', tip), ('reasoning', reasoning)]:
        if v: lines.append("    " + k + ": '" + esc(v) + "',")
    lines.append("    updated: '2026-09-12'")
    lines.append('  },')
    content = content[:i] + '\n'.join(lines) + content[end:]
    print('OK', key)

# ---------- movie（国庆档定档 + 哪吒百花奖） ----------
replace_section('movie',
 summary='2026年电影市场【国庆档定档+哪吒百花奖】：（1）4部影片定档2026国庆档——《小猪佩奇·完美假期》《野兽之心》《熊猫守护者》《活色生香》，陈思诚新片（张译/马丽主演）也将杀进国庆档、票房预期剑指10亿；（2）《哪吒之魔童闹海》获第38届大众电影百花奖最佳影片奖——国产动画获主流奖项认可；（3）《欢迎来龙餐馆》累计破20亿（2026第四部20亿+·年票房榜第三）。暑期档124亿收官+9月近40部影片定档。Re:Zero S4夺还篇最终话9/30定档（倒计时18天）。',
 trend='9月电影四大趋势：(1)**国庆档预热启动**——4部定档+陈思诚新片杀进，国庆档（10/1-10/7）是全年第二大档期→头部影片密集定档；(2)**哪吒百花奖**——国产动画获主流奖项，内容品质持续获认可；(3)**龙餐馆长尾**——破20亿升年榜第三，口碑长尾+喜剧刚需双引擎；(4)**金九银十内容旺季**——9月近40部新片+国庆档前瞻，内容消费热度延续。',
 tip='9月观影策略：(1)**国庆档前瞻**——4部已定档（小猪佩奇/野兽之心/熊猫守护者/活色生香）+陈思诚新片(张译马丽)，国庆档头部影片陆续公布→提前加片单；(2)**补看**——《哪吒之魔童闹海》(百花奖最佳影片/国产动画标杆)《欢迎来龙餐馆》(破20亿?口碑长尾)；(3)**IMAX之选**——《奥德赛》诺兰史诗；(4)**Re:Zero补番**——最终话9/30(倒计时18天)，补番窗口收窄。')

# ---------- anime（追番第31天·完结倒计时18天） ----------
replace_section('anime',
 summary='2026年9月12日动漫区【夺还篇完结倒计时】——Re:Zero S4【夺还篇】追番第31天（8/12开播），最终话9/30定档（还剩18天）——486在丧失记忆后的认知博弈进入收束阶段。国产方面：False Memory（B站独播）更新中；Link Click S3时光代理人第三季热播。BLEACH千年血战篇-祸进谭-仍在最终章。无职转生第三季稳步更新。10月秋季新番档期前瞻开启。',
 trend='9月动漫趋势：(1)**Re:Zero完结倒计时**——追番第31天，最终话9/30定档仅剩18天→完结前补番窗口收窄；(2)**秋季新番前瞻**——10月档期临近，接档阵容陆续公布→提前加追番单；(3)**国产悬疑持续**——False Memory+Link Click S3稳定输出；(4)**异世界双雄**——无职转生S3与Re:Zero构成奇幻供给。',
 tip='9月中追番策略：(1)**必追**——Re:Zero夺还篇第31天、9/30最终话(仅剩18天)，追到最新+补完前篇；(2)**同步**——BLEACH千年血战篇、无职转生S3；(3)**前瞻**——关注10月秋季新番情报与接档阵容；(4)**尝鲜**——False Memory+时光代理人S3。周末广州舒适，宅家补番正合适。')

# ---------- 其余板块：日期推进 9/12 ----------
for sec in ['music','novel','gaming','beer','fashion','diet','car','house','"life-tips"']:
    old = sec.replace('"','')
    m = re.search(r'(?m)^  ' + re.escape(sec) + r':\s*\{', content)
    if not m: 
        print('MISS', old); continue
    blk_start = m.start()
    depth = 0; j = m.start(); L = len(content); inq=False; q=''
    while j < L:
        ch = content[j]
        if inq:
            if ch == q: inq = False
            elif ch == '\\': j += 1
        elif ch in ("'", '"'): inq=True; q=ch
        elif ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: break
        j += 1
    blk = content[blk_start:j+1]
    newblk = blk.replace("updated: '2026-09-07'", "updated: '2026-09-12'")
    if newblk != blk:
        content = content[:blk_start] + newblk + content[j+1:]
        print('date->', old)

# ---------- DAILY_DECISIONS（9/12周六版） ----------
old_dec = re.search(r'var DAILY_DECISIONS = \{.*?\n\};', content, re.S)
new_dec = '''var DAILY_DECISIONS = {
  updated: "2026-09-12",
  items: [
    {icon:"🐳", action:"升级工具链：Harness + DeepSeek V4.1 Flash 实测（替代V4-Flash）", why:"V4.1 Flash(9/10发布)多个benchmark超Opus5/GPT-5.6 Sol·原生视觉·MIT开源·API降价(峰值$0.3/$1.2)", how:"①官网/HuggingFace下载或API调用 ②实测高频任务(写码/中文分析/看图) ③记录性能+成本对比→做成「模型选型实测」作品", priority:"P0"},
    {icon:"📝", action:"写300字行业观察《DeepSeek V4.1 Flash：开源模型追平闭源旗舰意味着什么》", why:"本周最强AI信号·面试必考·最能体现行业理解深度", how:"写300字→归档作品集→面试讲『开源vs闭源格局之变+成本/能力/隐私三角权衡』", priority:"P0"},
    {icon:"💪", action:"启动8周腹肌计划：周六有氧40min（跳绳/快走）", why:"新目标练出腹肌·体脂率是核心(现约15-18%·需≤12-15%)·跳绳是减脂主力", how:"跳绳40min(或30秒快跳+30秒休息×15组)·结束后量腰围记录基线·戒含糖饮料/夜宵(最快见效)", priority:"P1"},
    {icon:"📈", action:"A股9/11复盘：失守3900·AI硬件(覆铜板/元件)逆势是结构主线", why:"沪指-1.18%收3888.11·超4870只下跌·赚钱效应11%·但AI硬件/军工/电力逆势", how:"下周一(9/14)看：①能否收回3900 ②AI硬件(覆铜板涨价链)持续性 ③财报/美联储议息·普跌别抄底等企稳", priority:"P1"},
    {icon:"🎬", action:"国庆档前瞻+Re:Zero补番（倒计时18天）", why:"4部影片定档国庆档+陈思诚新片杀进·Re:Zero最终话9/30", how:"国庆档片单加收藏(小猪佩奇/野兽之心/熊猫守护者/活色生香)·Re:Zero夺还篇追到最新", priority:"P2"}
  ]
};'''
if old_dec:
    content = content.replace(old_dec.group(0), new_dec, 1)
    print('OK DAILY_DECISIONS')

# ---------- AI_OBSERVATIONS（加9/12） ----------
obs_anchor = "var AI_OBSERVATIONS = [\n"
obs_new = """var AI_OBSERVATIONS = [
  {date:'2026-09-12', topic:'DeepSeek V4.1 Flash发布，开源追平闭源旗舰', summary:'9/10发布：5520亿MoE、原生视觉理解、多个benchmark超Claude Opus 5/GPT-5.6 Sol、AutomationBench-AA超GPT-6 Astra拿第一、MIT开源、API峰值$0.3/$1.2——开源模型与闭源旗舰的能力差距正在消失，本地部署/私有化方案竞争力质变'},
  {date:'2026-09-12', topic:'AI治理立法化+Agent标准化', summary:'美国加州签署AI安全法案(Anthropic/OpenAI支持)+OpenAI推出Agents API公开测试版+无问芯穹发布Agent-Native模型NeoHorse——AI安全从企业自律走向立法，Agent开发走向标准化，AI安全/治理与Agent产品岗位需求上升'},
  {date:'2026-09-12', topic:'工信部人工智能+软件专项行动', summary:'到2028年累计100项软件企业智能化技改项目、部署智能编程与算力协同——政策驱动软件智能化改造，AI硬件(覆铜板/元件)与软件智能化方向获边际催化'},
"""
if 'V4.1 Flash发布，开源追平闭源旗舰' not in content:
    content = content.replace(obs_anchor, obs_new, 1)
    print('OK AI_OBSERVATIONS')

open(FP, 'w', encoding='utf-8').write(content)
print('rest 9/12 done')
