#!/usr/bin/env python3
"""cases_validate.py — 校验 cases.json 数据质量"""
import json, sys, re
from collections import Counter

def validate(path):
    with open(path, 'r', encoding='utf-8') as f:
        cases = json.load(f)
    
    errors = []
    warnings = []
    seen_ids = set()
    seen_titles = set()
    
    for i, c in enumerate(cases):
        prefix = f"[{i+1}] {c.get('id','?')}"
        
        # 必填字段
        for field in ['id', 'title', 'country', 'company', 'year', 'tech', 'scale', 'investment', 'roi', 'summary', 'source', 'tags']:
            if field not in c or not c[field]:
                errors.append(f"{prefix}: 缺少必填字段 '{field}'")
        
        # ID 唯一
        if c.get('id') in seen_ids:
            errors.append(f"{prefix}: ID '{c['id']}' 重复")
        seen_ids.add(c.get('id'))
        
        # 标题重复检测
        title_key = c.get('title', '').strip()
        if title_key in seen_titles:
            warnings.append(f"{prefix}: 标题可能重复 '{title_key}'")
        seen_titles.add(title_key)
        
        # 年份合理性
        if 'year' in c and isinstance(c['year'], int):
            if c['year'] < 2000 or c['year'] > 2026:
                warnings.append(f"{prefix}: 年份 {c['year']} 超出合理范围(2000-2026)")
        
        # 规模枚举
        if c.get('scale') not in ('大型', '中型', '小型', None):
            warnings.append(f"{prefix}: 规模 '{c['scale']}' 非标准值(大型/中型/小型)")
        
        # 数组字段
        for field in ['tech', 'tags']:
            if field in c and not isinstance(c[field], list):
                errors.append(f"{prefix}: '{field}' 应为数组")
            elif field in c and len(c[field]) == 0:
                warnings.append(f"{prefix}: '{field}' 为空数组")
        
        # 来源URL格式
        if 'source' in c and c['source']:
            if not re.match(r'^https?://', c['source']):
                warnings.append(f"{prefix}: 来源URL可能无效 '{c['source']}'")
        
        # 摘要长度
        if 'summary' in c and len(c.get('summary','')) < 30:
            warnings.append(f"{prefix}: 摘要过短({len(c['summary'])}字)，建议30字以上")
        
        # 置信度标记检查
        if 'confidence' in c:
            if c['confidence'] not in ('高', '中', '低'):
                warnings.append(f"{prefix}: 置信度 '{c['confidence']}' 非标准值(高/中/低)")
    
    # 统计
    print(f"=== 数据质量报告 ===")
    print(f"总案例数: {len(cases)}")
    print(f"错误: {len(errors)}")
    print(f"警告: {len(warnings)}")
    
    countries = Counter(c.get('country','') for c in cases)
    print(f"\n国家分布: {dict(countries.most_common())}")
    
    scales = Counter(c.get('scale','') for c in cases)
    print(f"规模分布: {dict(scales)}")
    
    years = Counter(c.get('year',0) for c in cases)
    print(f"年份分布: {dict(sorted(years.items()))}")
    
    all_tags = []
    for c in cases:
        all_tags.extend(c.get('tags',[]))
    print(f"标签TOP10: {Counter(all_tags).most_common(10)}")
    
    # 置信度分布
    conf = Counter(c.get('confidence','未标注') for c in cases)
    print(f"置信度分布: {dict(conf)}")
    
    if errors:
        print(f"\n=== 错误 ({len(errors)}) ===")
        for e in errors:
            print(f"  ❌ {e}")
    
    if warnings:
        print(f"\n=== 警告 ({len(warnings)}) ===")
        for w in warnings:
            print(f"  ⚠️ {w}")
    
    return len(errors) == 0

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/cases.json'
    ok = validate(path)
    sys.exit(0 if ok else 1)
