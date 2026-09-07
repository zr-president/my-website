# -*- coding: utf-8 -*-
"""2026-09-07 其余INSIGHTS板块更新（anime/music/novel/gaming/movie/learning/beer/fashion/fitness/diet/car/house/life-tips）
状态推进到9/7周一：①更新updated日期 ②anime追番+1天 ③movie加哪吒百花奖 ④关键板块改写"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
content = open(FP, 'r', encoding='utf-8').read()

def esc(v):
    return v.replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")

def replace_section(key, summary='', trend='', tip='', verdict='', reasoning=''):
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
    for k, v in [('verdict', verdict), ('summary', summary), ('trend', trend), ('tip', tip)]:
        if v: lines.append("    " + k + ": '" + esc(v) + "',")
    lines.append("    updated: '2026-09-07'")
    lines.append('  },')
    content = content[:i] + '\n'.join(lines) + content[end:]
    print('OK', key)

# anime：追番第26天（9/7）
replace_section('anime',
 summary='2026年9月7日动漫区【夺还篇完结倒计时】——Re:Zero S4【夺还篇】追番第26天（8/12开播），最终话9/30定档（还剩23天）——486在丧失记忆后的认知博弈进入收束阶段。国产方面：False Memory（B站独播）更新中；Link Click S3时光代理人第三季热播。BLEACH千年血战篇-祸进谭-仍在最终章。无职转生第三季稳步更新。10月秋季新番档期前瞻开启。',
 trend='9月动漫趋势：(1)**Re:Zero完结倒计时**——追番第26天，最终话9/30定档，完结前补番窗口只剩3周多；(2)**秋季新番前瞻**——10月档期临近，Re:Zero完结后接力阵容陆续公布→提前加追番单；(3)**国产悬疑持续**——False Memory+Link Click S3稳定输出；(4)**异世界双雄**——无职转生S3与Re:Zero构成奇幻供给。',
 tip='9月初追番策略：(1)**必追**——Re:Zero夺还篇第26天、9/30最终话(还23天)，追到最新+补完前篇；(2)**同步**——BLEACH千年血战篇、无职转生S3；(3)**前瞻**——关注10月秋季新番情报；(4)**尝鲜**——False Memory+时光代理人S3。周一广州秋高气爽，下班放松追番正好。')

# movie：哪吒百花奖 + 龙餐馆等
replace_section('movie',
 summary='2026年电影市场【哪吒百花奖+龙餐馆破20亿】：《哪吒之魔童闹海》获第38届大众电影百花奖最佳影片奖——国产动画获主流奖项认可。《欢迎来龙餐馆》累计票房破20亿（2026第四部20亿+，超《给阿嬷的情书》升年票房榜第三）。暑期档总票房124亿收官+9月近40部影片定档。诺兰《奥德赛》IMAX继续热映。影之刃零预售持续（268元起·10/29发售）。Re:Zero S4夺还篇追番第26天——最终话9/30定档。',
 trend='9月电影趋势：(1)**哪吒百花奖**——《哪吒之魔童闹海》最佳影片——国产动画/内容品质获主流奖项持续认可；(2)**龙餐馆长尾**——破20亿升年榜第三，口碑长尾+喜剧刚需双引擎；(3)**9月新片定档潮**——近40部定档，暑期到国庆平滑过渡；(4)**金九银十内容旺季**——OpenAI《哪吒》获百花奖带动国产动画关注。',
 tip='9月初观影策略：(1)**看获奖**——《哪吒之魔童闹海》(百花奖最佳影片·国产动画标杆)《欢迎来龙餐馆》(破20亿·口碑长尾)；(2)**IMAX之选**——《奥德赛》诺兰史诗巨制热映；(3)**9月新片**——近40部定档，关注口碑；(4)**Re:Zero补番**——追番第26天，最终话9/30(还23天)。')

# learning：GPT-6新叙事学习
replace_section('learning',
 verdict='🎯 今日学习结论：① 今天最有价值的学习主题是【GPT-6新叙事】——从Coding转向长程Agent/Computer Use：模型竞争主线之变，理解"端到端任务交付"价值是AI面试核心；② 次优【算力长逻辑】——GPT-6用10万卡训练→算力需求长期强化，A股算力硬件(CPO/光通信)是主线；③ 落地：把GPT-6新叙事写进简历/行业观察+理解Computer Use/Recurrent Depth概念。',
 summary='9月7日（周一）学习重点：(1)GPT-6新叙事解读——OpenAI 9/3发布GPT-6 Astra，模型竞争从Coding转向长程Agent/Computer Use：『任何你在电脑上能做的事Astra都替你完成』→理解端到端任务交付价值→AI产品/Agent岗面试核心(Coding是任务一环不是终点)；(2)算力长逻辑——GPT-6用10万卡训练(Stargate德州站)+Recurrent Depth架构(层复用+隐空间推理)→推理难监控、算力需求强化→A股算力硬件(CPO/光通信/芯片)是GPT-6主线；(3)金九银十求职复盘——周一复盘投递、更新简历、写GPT-6新叙事行业观察。',
 trend='9月学习主线：(1)**GPT-6新叙事=AI竞争主线之变**——从Coding到端到端Agent/Computer Use：理解"任务是交付而非单点回答"→AI产品/Agent岗的核心认知；(2)**Computer Use/长程Agent**——模型操作电脑/浏览器/办公工具→理解自动化价值；(3)**Recurrent Depth/隐空间推理**——层复用、推理难监控→AI安全/可解释性成新话题；(4)**算力长逻辑**——10万卡训练+Agent推理需求→算力需求长期强化；(5)**国产差距**——国产日常能力强但长程执行短板。',
 tip='今日学习行动：(1)**30分钟读懂GPT-6新叙事**——读ai-track板块→理解"Coding到任务交付"的模型竞争主线之变→写进简历/行业观察；(2)**理解核心概念**——Computer Use(电脑操作)/长程Agent(端到端任务)/Recurrent Depth(循环深度架构)→面试能讲清楚；(3)**写300字行业观察**——《GPT-6新叙事：从Coding到端到端任务交付》→本周作品集；(4)**算力链认知**——理解GPT-6→算力硬件(CPO/光通信/芯片)逻辑→面试谈资+1；(5)**看小白课堂**——今日新科普(GPT-6新叙事/Computer Use)。')

# 其余状态推进板块：只更新日期（weather类用旧内容，car/house为周一状态）
# 用通用方式：把这些板块的 updated 从 9-06 改到 9-07
for sec in ['music','novel','gaming','beer','fashion','fitness','diet','car','house','"life-tips"']:
    old = sec.replace('"','')
    # 找到该板块 updated 位置并替换日期
    m = re.search(r'(?m)^  ' + re.escape(sec) + r':\s*\{', content)
    if m:
        # 在该板块块内找 updated:'2026-09-06' 并改
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
        newblk = blk.replace("updated: '2026-09-06'", "updated: '2026-09-07'")
        if newblk != blk:
            content = content[:blk_start] + newblk + content[j+1:]
            print('date->', old)
        else:
            print('NOCHANGE', old)

open(FP, 'w', encoding='utf-8').write(content)
print('rest done')
