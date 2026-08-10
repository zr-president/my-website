import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

filepath = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

vocab_start = content.find('var DAILY_VOCAB = {')
vocab_end = content.find('var AI_MODEL_COMPARISON', vocab_start)
vocab_section = content[vocab_start:vocab_end]

# Fix field names
vocab_section = vocab_section.replace('def:', 'definition:')
vocab_section = vocab_section.replace('importance:', 'why_matters:')

# Add emoji and category
words_data = [
    ('资安关键能力', '🔐', 'AI'),
    ('打新(IPO申购)', '💰', '金融'),
    ('AI资本支出(Capex)', '💻', 'AI'),
    ('Starmind(轨道AI数据中心)', '🛰️', '科技'),
    ('空调外机效应(气象)', '🌡️', '科技'),
    ('开源权重(Open-weight)', '🔓', 'AI'),
    ('空降定档(电影行业)', '🎬', '产品'),
    ('MoE(混合专家模型)', '🧩', 'AI'),
    ('信仰之力(投资行为)', '🙏', '金融'),
    ('AI安全对齐(Alignment)', '🛡️', 'AI'),
]

for word, emoji, cat in words_data:
    old = '{word:"' + word + '", definition:'
    new = '{emoji:"' + emoji + '", category:"' + cat + '", word:"' + word + '", definition:'
    if old in vocab_section:
        vocab_section = vocab_section.replace(old, new)
        print(f'  OK {word}: +{emoji} +{cat}')
    else:
        print(f'  MISS {word}')

content = content[:vocab_start] + vocab_section + content[vocab_end:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
