var DAILY_DATA = {
  "update_time": "2026-07-26T08:57:00+08:00",
  "update_date": "2026年7月26日",

  "market_summary": "上证~3,867点 | 本周涨+1.33% | 大盘价值领涨（银行+4.5%）| 科技板块调整中 | 高盛/花旗超配A股",

  "news_headlines": [
    {"title": "Kimi K3发布：月之暗面发布全球最大开源模型2.8万亿参数", "url": "https://www.36kr.com/", "source": "36氪", "category": "AI"},
    {"title": "中美AI差距缩至3-5个月，美国研究者最新判断", "url": "https://www.jiqizhixin.com/", "source": "机器之心", "category": "AI"},
    {"title": "开源vs闭源大战：25家美国科技巨头联名支持开源", "url": "https://wallstreetcn.com/", "source": "华尔街见闻", "category": "科技"},
    {"title": "DeepSeek筹备IPO，V4模型预计月底发布", "url": "https://www.cls.cn/", "source": "财联社", "category": "AI"},
    {"title": "A股V型反弹：央企增持600亿+央行净投放8000亿", "url": "https://www.cls.cn/", "source": "财联社", "category": "财经"}
  ],

  "daily_recommendation": {
    "music": {"title": "今日推荐专辑：FKJ — Ylang Ylang", "desc": "Neo-Soul/电子 · 适合工作背景音", "link": "https://music.163.com/#/search/m/?s=FKJ+Ylang+Ylang"},
    "anime": {"title": "今日追番：咒术回战 死灭回游篇", "desc": "规则系智斗巅峰 · 2026夏季必看", "link": "https://www.bilibili.com/search?keyword=咒术回战"},
    "novel": {"title": "今日阅读：十日终焉", "desc": "无限流智斗天花板 · 已完结386万字", "link": "https://www.qidian.com/soushu/十日终焉.html"},
    "cocktail": {"title": "今日特调：威士忌酸 Whiskey Sour", "desc": "波本60ml+柠檬汁30ml+糖浆20ml · 经典不败", "link": "https://s.taobao.com/search?q=波本威士忌"}
  },

  "weather_summary": "广州 34°C/26°C · 多云转雷阵雨 · 湿度75% · 微风",

  "weekly_focus": "📊 周二：深度推荐日 · 股市学习+动漫小说推荐",

  "tip_of_day": "💡 新手的投资第一课：不亏钱比赚钱更重要。开始定投沪深300ETF前，先读《彼得·林奇的成功投资》。"
};

var PICKS = {
  anime: [
    {icon:"🥇", title:"咒术回战 死灭回游篇", desc:"规则系智斗巅峰 · 2026夏季最期待", link:"https://www.bilibili.com/search?keyword=咒术回战"},
    {icon:"🥈", title:"地狱乐 第二季", desc:"MAPPA黑暗战斗 · 神仙vs人类", link:"https://www.bilibili.com/search?keyword=地狱乐"},
    {icon:"🥉", title:"怪兽8号 第二季", desc:"JUMP新台柱 · 热血怪兽战斗", link:"https://www.bilibili.com/search?keyword=怪兽8号"}
  ],
  music: [
    {icon:"🎹", title:"FKJ — Ylang Ylang", desc:"Neo-Soul/电子 · 工作背景音首选", link:"https://music.163.com/#/search/m/?s=FKJ+Ylang+Ylang"},
    {icon:"🎸", title:"告五人 — 迷雾之子", desc:"独立流行 · 从主流到独立的桥梁", link:"https://music.163.com/#/search/m/?s=告五人+迷雾之子"},
    {icon:"🗾", title:"YOASOBI — 夜に駆ける", desc:"J-Rock · 旋律走向接近华语审美", link:"https://music.163.com/#/search/m/?s=YOASOBI+夜に駆ける"}
  ],
  novel: [
    {icon:"🥇", title:"十日终焉", desc:"无限流智斗天花板 · 已完结386万字", link:"https://www.qidian.com/soushu/十日终焉.html"},
    {icon:"🥈", title:"道诡异仙", desc:"克系修仙 · 网文史上独一档的癫", link:"https://www.qidian.com/soushu/道诡异仙.html"},
    {icon:"🥉", title:"深海余烬", desc:"末世克系 · 氛围塑造网文天花板", link:"https://www.qidian.com/soushu/深海余烬.html"}
  ],
  beer: [
    {icon:"🍺", title:"保拉纳酵母小麦", desc:"德式小麦入门首选 · 香蕉丁香", link:"https://s.taobao.com/search?q=保拉纳小麦啤酒"},
    {icon:"🍻", title:"酿酒狗朋克IPA", desc:"IPA探险第一站 · 热带水果轰炸", link:"https://s.taobao.com/search?q=酿酒狗朋克IPA"},
    {icon:"🍸", title:"威士忌酸 Whiskey Sour", desc:"今日特调 · 波本+柠檬+糖浆", link:"https://s.taobao.com/search?q=波本威士忌"}
  ],
  gaming: [
    {icon:"⚔️", title:"只狼：影逝二度", desc:"拼刀战斗巅峰 · 史低¥134", link:"https://store.steampowered.com/app/814380/"},
    {icon:"🐉", title:"怪物猎人：荒野", desc:"联机狩猎 · 史低¥146", link:"https://store.steampowered.com/app/2246340/"}
  ],
  learning: [
    {icon:"✍️", title:"Prompt Engineering速成", desc:"5个技巧让你立刻提升AI效率", link:"#"},
    {icon:"🗺️", title:"2026 AI学习路线图", desc:"零代码到Agent开发者的6步路径", link:"#"},
    {icon:"🧰", title:"AI工具全景清单", desc:"20+工具按用途分类速查", link:"#"}
  ],
  fashion: [
    {icon:"👕", title:"日系简约日常", desc:"重磅白T+黑色九分裤+帆布鞋", link:"https://s.taobao.com/search?q=重磅棉落肩T恤男250g"},
    {icon:"👔", title:"韩系都市通勤", desc:"牛津纺衬衫+卡其裤+德训鞋", link:"https://s.taobao.com/search?q=优衣库牛津纺衬衫男浅蓝"}
  ],
  fitness: [
    {icon:"💪", title:"周一：胸+三头", desc:"俯卧撑→钻石俯卧撑→拉力绳推胸", link:"#"},
    {icon:"📈", title:"12周渐进训练计划", desc:"每周5练 · 适应→增肌→强化", link:"#"}
  ],
  diet: [
    {icon:"🥗", title:"午餐：鸡胸肉+糙米饭", desc:"650kcal · 42g蛋白质", link:"#"},
    {icon:"🐟", title:"晚餐：清蒸鱼+红薯", desc:"500kcal · 35g蛋白质", link:"#"}
  ],
  career: [
    {icon:"💼", title:"BOSS直聘", desc:"AI/互联网岗位最集中", link:"https://www.zhipin.com"},
    {icon:"🎯", title:"猎聘", desc:"中高端岗位更多 · 内推渠道", link:"https://www.liepin.com"}
  ],
  car: [
    {icon:"⚡", title:"极氪007焕新版", desc:"¥19.39万 · 715km续航 · 900V", link:"https://www.dongchedi.com"},
    {icon:"🚗", title:"小鹏MONA M03", desc:"¥14.99万 · 15万内智驾最强", link:"https://www.dongchedi.com"}
  ],
  house: [
    {icon:"🏠", title:"广州", desc:"新房~3.2万/㎡ · 二手~2.8万/㎡", link:"https://www.ke.com"},
    {icon:"🏙️", title:"深圳", desc:"新房~5.5万/㎡ · 二手~5.0万/㎡", link:"https://www.ke.com"}
  ]
};

// Trigger picks rendering (function defined in index.html)
if(typeof renderAllPicks === 'function') renderAllPicks();
