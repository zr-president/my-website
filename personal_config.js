// personal_config.js — 个人偏好配置
// 此文件提交到仓库，只含偏好不含密钥
// 敏感信息（PushPlus Token、API Key）通过 GitHub Secrets 注入

var PERSONAL_CONFIG = {
  // --- 基本信息 ---
  profile: {
    name: "钟锐",
    city: "广州",
    timezone: "Asia/Shanghai",
    job_status: "求职中",
    target_roles: ["AI产品运营", "AI增长运营"],
    target_companies: ["字节跳动", "腾讯", "美团", "小红书", "微众银行", "SHEIN", "滴滴"],
    height_cm: 170,
    weight_kg: 59,
    dietary: ["肾结石预防", "甲状腺结节"],
    fitness_goal: "增肌",
    fitness_week: 3
  },

  // --- 自选股 ---
  watchlist: {
    stocks: ["上证指数", "创业板指", "科创50", "恒生科技"],
    ipo_track: true,
    ipo_sectors: ["AI", "机器人", "半导体"]
  },

  // --- 求职追踪 ---
  job: {
    weekly_target: 15,
    platforms: ["Boss直聘", "猎聘", "脉脉"],
    total_sent: 0,
    interviews: 0,
    offers: 0
  },

  // --- 内容偏好 ---
  preferences: {
    anime_genres: ["智斗", "悬疑", "克苏鲁", "战斗"],
    music_genres: ["华语流行", "Neo-Soul", "J-Pop", "K-Pop"],
    novel_genres: ["玄幻", "克苏鲁", "悬疑", "修真"],
    game_genres: ["动作", "ARPG", "克苏鲁", "武侠"],
    movie_genres: ["悬疑", "科幻", "动画", "喜剧"],
    beer_styles: ["德式小麦", "IPA", "金酒基鸡尾酒"],
    learning_topics: ["AI安全", "AI产品", "开源生态", "机器人", "增长策略"]
  },

  // --- 推送时间表 ---
  schedule: {
    morning: "08:00",
    midday: "12:00",
    evening: "18:00",
    night: "22:00"
  },

  // --- 板块价值权重（0-5星，决定首页排序与折叠）---
  // 基于钟锐对信息价值的看重：与工作/钱/学习/健康强相关的板块权重高
  section_weights: {
    "toolchain-radar": 5,   // AI工具链：正在用的工具，最高优先
    "stock": 5,             // 股市基金：钱相关
    "career": 5,            // 求职中心：工作相关
    "learning": 4,          // 学习区：自我提升
    "ai-track": 4,          // AI动态：行业+求职
    "daily-vocab": 4,       // 每日一词：知识积累
    "daily-quiz": 4,        // 每日一练：能力训练
    "fitness": 3,           // 健身：健康相关
    "diet": 3,              // 饮食：健康相关（肾结石/甲状腺）
    "news": 3,              // 新闻：精选后有价值
    "car": 2,               // 购车：中长期决策
    "house": 2,             // 购房：中长期决策
    "beer": 2,              // 精酿：兴趣
    "novel": 2,             // 小说：兴趣
    "anime": 2,             // 动漫：兴趣
    "gaming": 2,            // 游戏：兴趣
    "movie": 2,             // 影视：娱乐
    "music": 1,             // 音乐：娱乐放松
    "fashion": 1,           // 穿搭：低频需求
    "travel": 1,            // 旅游：低频需求
    "life-tips": 1          // 生活助手：按需查询
  },

  // --- 新闻噪音过滤（推送/首页RSS过滤用）---
  news_filters: {
    watch: ["AI", "大模型", "机器人", "求职", "招聘", "广州", "深圳", "半导体", "芯片", "算力", "DeepSeek", "Claude", "GPT", "开源", "新能源", "自动驾驶"],
    block: ["明星", "八卦", "出轨", "综艺", "选秀", "网红带货"]
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = PERSONAL_CONFIG;
}
