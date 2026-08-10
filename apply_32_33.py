import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

filepath = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# === #32: Add 安全 scores to each model ===
# Pattern: "intelligence:NN, speed:NN,性价比:NN, 综合:NN,"
# Replace with: "intelligence:NN, speed:NN,性价比:NN, 安全:SS, 综合:NN,"

# Each model's security score:
# Format: (model_name_marker, security_score)
model_security = [
    # DeepSeek V4 Flash
    ('"DeepSeek V4 Flash"', 85),
    # DeepSeek V4 Pro
    ('"DeepSeek V4 Pro"', 82),
    # GPT-5.6 Luna
    ('"GPT-5.6 Luna"', 78),
    # GPT-5.6 Sol
    ('"GPT-5.6 Sol"', 74),
    # Claude Sonnet 4.6
    ('"Claude Sonnet 4.6"', 88),
    # Claude Opus 5
    ('"Claude Opus 5"', 92),
    # Claude Fable 5
    ('"Claude Fable 5"', 85),
    # Kimi K3
    ('"Kimi K3"', 76),
    # Grok 4.6
    ('"Grok 4.6"', 62),
    # Qwen3.8-Max
    ('"Qwen3.8-Max"', 84),
    # Gemini 3 Pro
    ('"Gemini 3 Pro"', 75),
]

count = 0
for model_name, sec_score in model_security:
    # Find the model block
    idx = content.find(model_name)
    if idx < 0:
        print(f'❌ Model not found: {model_name}')
        continue
    # Find the intelligence/speed/性价比/综合 line within this model's block
    block_end = content.find('},', idx)
    if block_end < 0:
        block_end = content.find('}', idx)
    block = content[idx:block_end]

    # Pattern: intelligence:NN, speed:NN,性价比:NN, 综合:NN,
    pattern = r'(intelligence:\d+,\s*speed:\d+,\s*性价比:\d+),\s*(综合:\d+)'
    match = re.search(pattern, block)
    if match:
        old_str = content[idx + match.start():idx + match.end()]
        new_str = match.group(1) + f', 安全:{sec_score}, ' + match.group(2)
        content = content.replace(old_str, new_str, 1)
        count += 1
        print(f'✅ {model_name}: 安全={sec_score}')
    else:
        print(f'❌ Pattern not found in {model_name} block')

print(f'\n{count}/11 models updated with 安全 scores')

# === Update scoring_guide ===
old_guide = "综合: '智能50% + 性价比35% + 速度15% = 满分100·综合≥90绿·75-89琥珀·<75灰'"
new_guide = "综合: '智能50% + 性价比35% + 速度15% = 满分100·综合≥90绿·75-89琥珀·<75灰',\n    安全: '开源透明度+安全围栏+红队测试+对齐投入·≥85绿(安全标杆)·70-84琥珀·<70灰(安全风险)'"
if old_guide in content:
    content = content.replace(old_guide, new_guide)
    print('✅ scoring_guide updated with 安全 dimension')
else:
    print('❌ scoring_guide pattern not found')

# === Update MODEL_SCORE_COLORS ===
old_colors = "综合: {high:'#059669', mid:'#d97706', low:'#94a3b8'}"
new_colors = "综合: {high:'#059669', mid:'#d97706', low:'#94a3b8'},\n    安全: {high:'#059669', mid:'#d97706', low:'#e11d48'}"
if old_colors in content:
    content = content.replace(old_colors, new_colors)
    print('✅ MODEL_SCORE_COLORS updated with 安全')
else:
    print('❌ MODEL_SCORE_COLORS pattern not found')

# === #33: Add INSIGHTS_TODAY_UPDATED ===
today_updated_var = '\n// Today\'s updated INSIGHTS sections (for optimization #33)\nvar INSIGHTS_TODAY_UPDATED = [\'stock\',\'ai-track\',\'movie\',\'learning\',\'career\',\'news\'];\n'
# Insert after INSIGHTS closing (after the }; of INSIGHTS)
insights_end = content.find("};\n\nvar OPTIMIZATION_LOG")
if insights_end > 0:
    content = content[:insights_end] + today_updated_var + content[insights_end:]
    print('✅ INSIGHTS_TODAY_UPDATED added')
else:
    print('❌ INSIGHTS end marker not found')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n✅ daily_data.js updated for #32 + #33')
