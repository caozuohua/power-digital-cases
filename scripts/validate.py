#!/usr/bin/env python3
"""
validate.py — 电力案例集数据质量校验（集成去重检查）

使用方式：
  python3 scripts/validate.py              # 校验现有数据
  python3 scripts/validate.py --check FILE  # 校验新数据文件
"""
import json, sys, re, os
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent))
from dedup import find_true_duplicates, check_new_against_existing, load_cases

PROJECT_DIR = Path(__file__).parent.parent
DATA_FILE = PROJECT_DIR / "data" / "cases.json"

def validate(path):
    cases = load_cases(path)
    errors = []
    warnings = []
    seen_ids = set()
    seen_titles = set()
    
    for i, c in enumerate(cases):
        prefix = f"[{i+1}] {c.get('id','?')}"
        
        for field in ['id', 'title', 'country', 'company', 'year', 'tech', 'scale', 'investment', 'roi', 'summary', 'source', 'tags']:
            if field not in c or not c[field]:
                errors.append(f"{prefix}: 缺少必填字段 '{field}'")
        
        if c.get('id') in seen_ids:
            errors.append(f"{prefix}: ID '{c['id']}' 重复")
        seen_ids.add(c.get('id'))
        
        title_key = c.get('title', '').strip()
        if title_key in seen_titles:
            warnings.append(f"{prefix}: 标题可能重复 '{title_key}'")
        seen_titles.add(title_key)
        
        if 'year' in c and isinstance(c['year'], int):
            if c['year'] < 2000 or c['year'] > 2026:
                warnings.append(f"{prefix}: 年份 {c['year']} 超出范围(2000-2026)")
        
        if c.get('scale') not in ('大型', '中型', '小型', None):
            warnings.append(f"{prefix}: 规模 '{c['scale']}' 非标准值")
        
        for field in ['tech', 'tags']:
            if field in c and not isinstance(c[field], list):
                errors.append(f"{prefix}: '{field}' 应为数组")
            elif field in c and len(c[field]) == 0:
                warnings.append(f"{prefix}: '{field}' 为空数组")
        
        if 'source' in c and c['source']:
            if not re.match(r'^https?://', c['source']):
                warnings.append(f"{prefix}: 来源URL可能无效 '{c['source']}'")
        
        if 'summary' in c and len(c.get('summary','')) < 30:
            warnings.append(f"{prefix}: 摘要过短({len(c['summary'])}字)")
        
        if 'confidence' in c:
            if c['confidence'] not in ('高', '中', '低'):
                warnings.append(f"{prefix}: 置信度 '{c['confidence']}' 非标准值")
    
    # 去重检查
    dups = find_true_duplicates(cases)
    
    print(f"=== 数据质量报告 ===")
    print(f"总案例数: {len(cases)}")
    print(f"错误: {len(errors)}")
    print(f"警告: {len(warnings)}")
    print(f"重复: {len(dups)}")
    
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
    
    conf = Counter(c.get('confidence','未标注') for c in cases)
    print(f"置信度分布: {dict(conf)}")
    
    if errors:
        print(f"\n=== 错误 ({len(errors)}) ===")
        for e in errors:
            print(f"  ❌ {e}")
    
    if warnings:
        print(f"\n=== 警告 ({len(warnings)}) ===")
        for w in warnings[:20]:
            print(f"  ⚠️ {w}")
        if len(warnings) > 20:
            print(f"  ... 还有 {len(warnings)-20} 条警告")
    
    if dups:
        print(f"\n=== 重复 ({len(dups)}) ===")
        for d in dups:
            print(f"  [{d['case_a']['id']}] {d['case_a']['title'][:30]}")
            print(f"    [{d['case_b']['id']}] {d['case_b']['title'][:30]}")
            for r in d['reasons']:
                print(f"    → {r}")
    
    return len(errors) == 0 and len(dups) == 0

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else str(DATA_FILE)
    ok = validate(path)
    sys.exit(0 if ok else 1)
