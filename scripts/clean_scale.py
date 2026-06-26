"""优化 scale 字段: 只保留简洁规模描述"""
import json, re

cases = json.load(open('/home/caozuohua99/power-digital-cases/data/cases.json'))

def clean_scale(id_text, text):
    """从可能很长的文字中提取简洁规模"""
    if not text:
        return ''
    
    # 如果文字本身很短(<=15字)，直接用
    if len(text) <= 15:
        return text
    
    # 提取关键量词模式
    patterns = [
        # 规模+数字
        r'(\d+\.?\d*\s*(?:GW|MW|kW|台|座|户|万只|亿只|千万|百万|GW|GWh|MWh|亿|万|户|套|个|条|km|公里|立方米|吨|人|家|MWp|吉瓦|兆瓦|千瓦))',
        # 覆盖 + 地区/国家 
        r'(全球|全国|全省|全市|覆盖[^，,。]+)',
    ]
    
    found = []
    for pat in patterns:
        matches = re.findall(pat, text)
        if matches:
            # 取最长匹配的(更完整的信息)
            best = max(matches, key=len)
            if len(best) > 2:
                found.append(best)
    
    if found:
        unique_found = list(dict.fromkeys(found))
        result = '/'.join(unique_found[:2])
        return result[:20]  # 硬限20字
    
    # fallback
    if 'MW' in text or 'GW' in text:
        m = re.search(r'\d+\.?\d*\s*(?:MW|GW)', text)
        if m:
            return m.group()
    if '户' in text:
        m = re.search(r'\d+\s*户', text)
        if m:
            return m.group()
    if '全国' in text or '全球' in text:
        return text[:10]
    
    # 最终fallback
    return text[:15]

changed = 0
for c in cases:
    original = c.get('scale', '')
    cleaned = clean_scale(c['id'], original)
    c['scale'] = cleaned
    if cleaned != original:
        changed += 1

with open('/home/caozuohua99/power-digital-cases/data/cases.json', 'w') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print(f'修改: {changed}条')
print(f'\n效果抽样(修改前后对比):')
print('-' * 60)
# 再看最长的是多少字
new_lens = [(c['id'], c.get('scale','')) for c in cases if len(c.get('scale','')) > 10]
new_lens.sort(key=lambda x: -len(x[1]))
for cid, s in new_lens[:7]:
    print(f'  {cid[:25]:<26} | {len(s):>2}字 | {s}')
