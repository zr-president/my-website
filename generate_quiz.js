const fs = require('fs');

const quiz = JSON.parse(fs.readFileSync('C:/Users/ZR/Desktop/钟锐的个人网站/extracted_quiz.json', 'utf-8'));

function esc(str) {
  return str.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\n/g, '\\n').replace(/\r/g, '');
}

let js = "var DAILY_QUIZ = {\n";
js += "  title: '每日一练',\n";
js += "  subtitle: '按星期轮换5种题型 · 每天一道 · 附答案和答题技巧',\n";
js += "  schedule: {\n";
js += "    '周一': 'SQL实战',\n";
js += "    '周二': '产品分析',\n";
js += "    '周三': 'Prompt设计',\n";
js += "    '周四': '数据分析',\n";
js += "    '周五': '行为面试'\n";
js += "  },\n";
js += "  questions: [\n";

quiz.forEach((q, i) => {
  // Shorten very long answers
  let shortAnswer = q.answer;
  if (shortAnswer.length > 500) {
    shortAnswer = shortAnswer.substring(0, 500) + '...(完整答案含SQL代码和详细步骤,详见学习中心)';
  }
  js += "    {\n";
  js += "      type: '" + esc(q.type) + "',\n";
  js += "      day: '" + esc(q.day) + "',\n";
  js += "      question: '" + esc(q.question) + "',\n";
  js += "      answer: '" + esc(shortAnswer) + "',\n";
  js += "      tip: '" + esc(q.tip) + "'\n";
  js += "    }";
  if (i < quiz.length - 1) js += ",";
  js += "\n";
});

js += "  ]\n";
js += "};\n";

fs.writeFileSync('C:/Users/ZR/Desktop/钟锐的个人网站/generated_quiz.js', js, 'utf-8');
console.log('Generated quiz JS with ' + quiz.length + ' questions');
