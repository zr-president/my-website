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
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = PERSONAL_CONFIG;
}
