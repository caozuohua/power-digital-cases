#!/usr/bin/env python3
"""
dedup.py — 电力案例集重复检测引擎 v2

改进：
- 提高标题相似度阈值到 0.85（避免"XX集团风电平台" vs "XX集团光伏平台"误判）
- URL相似度不再单独作为判断依据（同一企业多个项目共享域名是正常的）
- "企业+国家+年份"组合需要标题也有一定相似度才判定重复
- 增加 --fix 模式：自动标记真正重复（标题相似>90% 且 企业+年份相同）

使用方式：
  python3 scripts/dedup.py                        # 检测现有数据
  python3 scripts/dedup.py --check <new_file.json> # 检测新数据
  python3 scripts/dedup.py --fix                   # 自动去重（保守模式）
"""

import json, sys, re, os
from pathlib import Path
from collections import Counter
from difflib import SequenceMatcher

PROJECT_DIR = Path(__file__).parent.parent
DATA_FILE = PROJECT_DIR / "data" / "cases.json"

def load_cases(path=None):
    if path is None:
        path = DATA_FILE
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'^(the|a|an)\s+', '', text)
    text = re.sub(r'\s+(project|program|system|platform|pilot|demo|trial)$', '', text)
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff]', '', text)
    return text

def title_similarity(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()

def find_true_duplicates(cases):
    """
    只标记真正的重复：
    1. ID 完全相同
    2. 标题相似度 >= 90% 且 企业+国家+年份相同
    3. 标题相似度 >= 95%（几乎相同标题）
    """
    duplicates = []
    n = len(cases)
    
    for i in range(n):
        for j in range(i + 1, n):
            a, b = cases[i], cases[j]
            reasons = []
            is_dup = False
            
            # ID 完全匹配
            if a.get('id') and b.get('id') and a['id'] == b['id']:
                reasons.append(f"ID相同: {a['id']}")
                is_dup = True
            
            # 标题相似度
            sim = title_similarity(a.get('title', ''), b.get('title', ''))
            
            # 几乎相同标题（>=95%）
            if sim >= 0.95:
                reasons.append(f"标题几乎相同({sim:.0%})")
                is_dup = True
            
            # 高度相似标题 + 企业+年份相同
            if sim >= 0.90:
                if (a.get('company') == b.get('company') and
                    a.get('year') == b.get('year') and
                    a.get('company')):
                    reasons.append(f"标题高度相似({sim:.0%}) + 企业+年份相同")
                    is_dup = True
            
            if is_dup:
                duplicates.append({
                    'case_a': {'id': a.get('id'), 'title': a.get('title'), 'company': a.get('company'), 'year': a.get('year')},
                    'case_b': {'id': b.get('id'), 'title': b.get('title'), 'company': b.get('company'), 'year': b.get('year')},
                    'reasons': reasons,
                })
    
    return duplicates

def check_new_against_existing(new_cases, existing_cases):
    """检查新案例与现有数据的重复"""
    results = {'clean': [], 'duplicates': []}
    
    for nc in new_cases:
        dup_reasons = []
        
        for ec in existing_cases:
            reasons = []
            
            if nc.get('id') == ec.get('id'):
                reasons.append(f"ID已存在: {nc['id']}")
            
            sim = title_similarity(nc.get('title', ''), ec.get('title', ''))
            
            if sim >= 0.95:
                reasons.append(f"标题与 [{ec['id']}] 几乎相同({sim:.0%})")
            elif sim >= 0.90:
                if (nc.get('company') == ec.get('company') and
                    nc.get('year') == ec.get('year')):
                    reasons.append(f"可能与 [{ec['id']}] 重复(标题相似{sim:.0%}+企业/年份相同)")
            
            if reasons:
                dup_reasons.extend(reasons)
        
        if dup_reasons:
            results['duplicates'].append({
                'case': {'id': nc.get('id'), 'title': nc.get('title')},
                'reasons': list(set(dup_reasons)),
            })
        else:
            results['clean'].append(nc)
    
    return results


def cmd_check():
    cases = load_cases()
    dups = find_true_duplicates(cases)
    
    if not dups:
        print("✅ 无真正重复")
        return
    
    print(f"⚠️ 发现 {len(dups)} 组真正重复：\n")
    for i, d in enumerate(dups, 1):
        print(f"{'='*60}")
        print(f"#{i}")
        print(f"  A: [{d['case_a']['id']}] {d['case_a']['title']}")
        print(f"      {d['case_a']['company']} / {d['case_a']['year']}")
        print(f"  B: [{d['case_b']['id']}] {d['case_b']['title']}")
        print(f"      {d['case_b']['company']} / {d['case_b']['year']}")
        for r in d['reasons']:
            print(f"  → {r}")


def cmd_check_new(new_file):
    new_cases = load_cases(new_file)
    existing = load_cases()
    results = check_new_against_existing(new_cases, existing)
    
    total = len(new_cases)
    clean = len(results['clean'])
    dups = len(results['duplicates'])
    
    print(f"检查结果：{total} 条新数据 → ✅ 无重复: {clean}  ⚠️ 重复: {dups}")
    
    if results['duplicates']:
        print(f"\n重复详情：")
        for d in results['duplicates']:
            print(f"\n  [{d['case']['id']}] {d['case']['title']}")
            for r in d['reasons']:
                print(f"    → {r}")
    
    if results['clean']:
        clean_file = str(new_file).replace('.json', '_clean.json')
        with open(clean_file, 'w', encoding='utf-8') as f:
            json.dump(results['clean'], f, ensure_ascii=False, indent=2)
        print(f"\n{clean} 条无重复数据已保存到: {clean_file}")
    
    return results


def cmd_fix():
    """保守自动去重：只删除明确重复的（标题>=95%相似）"""
    cases = load_cases()
    dups = find_true_duplicates(cases)
    
    if not dups:
        print("✅ 无需去重")
        return
    
    # 收集要删除的 ID（每组只删 B，保留 A）
    to_remove = set()
    for d in dups:
        # 只删除标题几乎相同（>=95%）的
        for r in d['reasons']:
            if '几乎相同' in r:
                to_remove.add(d['case_b']['id'])
                break
    
    if not to_remove:
        print("✅ 无需自动修复（无标题几乎相同的重复）")
        return
    
    clean = [c for c in cases if c['id'] not in to_remove]
    print(f"将删除 {len(to_remove)} 条重复：")
    for rid in to_remove:
        title = next((c['title'] for c in cases if c['id'] == rid), '?')
        print(f"  🗑️ [{rid}] {title}")
    
    choice = input(f"\n确认删除？[y/N]: ").strip().lower()
    if choice == 'y':
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(clean, f, ensure_ascii=False, indent=2)
        print(f"✅ 已删除 {len(to_remove)} 条，保留 {len(clean)} 条")
    else:
        print("已取消")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='案例重复检测 v2')
    parser.add_argument('--check', type=str, help='检查新数据文件')
    parser.add_argument('--fix', action='store_true', help='自动去重')
    args = parser.parse_args()
    
    if args.check:
        cmd_check_new(args.check)
    elif args.fix:
        cmd_fix()
    else:
        cmd_check()
