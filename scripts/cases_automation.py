#!/usr/bin/env python3
"""
cases_automation.py — 电力案例集数据更新自动化

功能：
1. fetch_news() — 从 RSS/Atom 源抓取电力行业新闻
2. extract_candidates() — 从新闻中提取候选案例
3. validate_batch() — 校验候选案例质量
4. generate_report() — 生成更新报告

使用方式：
  python3 scripts/cases_automation.py --fetch        # 抓取新闻并生成候选
  python3 scripts/cases_automation.py --validate      # 校验现有数据
  python3 scripts/cases_automation.py --report        # 生成数据报告
  python3 scripts/cases_automation.py --full          # 完整流程
"""

import json, os, sys, re, argparse, subprocess
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_FILE = PROJECT_DIR / "data" / "cases.json"
CANDIDATES_FILE = PROJECT_DIR / "data" / "candidates.json"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

# ── RSS/Atom 源 ──
NEWS_FEEDS = {
    # 国际电力行业
    "reuters-energy": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
    "bloomberg-energy": "https://feeds.bloomberg.com/markets/news.rss",
    # 中国电力
    "china-power": "https://news.b3.org.cn/rss/energy.xml",
    "sgcc-news": "https://www.sgcc.com.cn/html/20240101/1349001.shtml",
    # 新能源
    "pv-magazine": "https://www.pv-magazine.com/feed/",
    "windpower-engineering": "https://www.windpowerengineering.com/feed/",
    "energy-storage": "https://www.energy-storage.news/feed/",
    # 数字化
    "smart-grid": "https://www.smartgridtoday.com/feed/",
    "utility-dive": "https://www.utilitydive.com/feed/",
    "greentech-media": "https://www.greentechmedia.com/feed/",
}

# 关键词匹配（用于从新闻中提取候选）
POWER_KEYWORDS = [
    "digital transformation", "smart grid", "AI", "artificial intelligence",
    "IoT", "digital twin", "virtual power plant", "VPP", "energy storage",
    "predictive maintenance", "无人机巡检", "数字孪生", "智慧电厂",
    "智能电网", "虚拟电厂", "储能", "绿氢", "hydrogen",
    "renewable energy", "solar", "wind power", "光伏", "风电",
    "carbon neutral", "net zero", "ESG", "carbon emissions",
    "advanced metering", "AMI", "smart meter", "智能电表",
    "microgrid", "微电网", "demand response", "需求响应",
    "blockchain energy", "电力区块链", "电力市场",
    "power utility", "electricity", "grid modernization",
]

COMPANY_KEYWORDS = [
    "State Grid", "SGCC", "南方电网", "China Southern Power Grid",
    "华能", "大唐", "华电", "国电", "国家电投", "SPIC",
    "远景能源", "Envision", "宁德时代", "CATL", "隆基", "LONGi",
    "阳光电源", "Sungrow", "比亚迪", "BYD",
    "Tesla", "NextEra", "Duke Energy", "Exelon", "Southern California Edison",
    "PG&E", "Florida Power", "FPL",
    "E.ON", "RWE", "EnBW", "EDF", "Engie", "Enel", "Iberdrola",
    "National Grid", "Ørsted", "Vattenfall", "Statkraft",
    "TEPCO", "关西电力", "KEPCO", "Korea Electric",
    "Tata Power", "NTPC", "Adani", "Suzlon",
    "ACWA Power", "DEWA", "EWEC",
    "Iberdrola", "Endesa", "TenneT", "Statnett",
    "CPFL", "Eletrobras", "Enel", "A2A",
]


def load_existing():
    """加载现有案例数据"""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_candidates(candidates):
    """保存候选案例"""
    with open(CANDIDATES_FILE, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    print(f"保存 {len(candidates)} 条候选案例到 {CANDIDATES_FILE}")


def load_candidates():
    """加载候选案例"""
    if not CANDIDATES_FILE.exists():
        return []
    with open(CANDIDATES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_duplicates(candidate, existing_cases):
    """检查候选案例是否与现有数据重复"""
    issues = []
    for c in existing_cases:
        # ID 重复
        if candidate.get('id') == c.get('id'):
            issues.append(f"ID '{c['id']}' 已存在")
        # 标题相似（简单包含检测）
        if candidate.get('title', '') and c.get('title', ''):
            if candidate['title'][:20] in c['title'] or c['title'][:20] in candidate['title']:
                issues.append(f"标题可能与 '{c['title']}' 重复")
    return issues


# ── 数据校验 ──
def validate_candidates(candidates, existing_cases=None):
    """校验候选案例"""
    if existing_cases is None:
        existing_cases = load_existing()
    
    results = {"valid": [], "invalid": [], "duplicates": []}
    seen_ids = set()
    
    for c in candidates:
        errors = []
        
        # 必填字段
        for field in ['id', 'title', 'country', 'company', 'year', 'tech', 'scale', 'investment', 'roi', 'summary', 'source', 'tags']:
            if field not in c or not c[field]:
                errors.append(f"缺少必填字段 '{field}'")
        
        # ID 唯一（批次内）
        if c.get('id') in seen_ids:
            errors.append(f"ID '{c['id']}' 在批次内重复")
        seen_ids.add(c.get('id'))
        
        # 与现有数据重复
        dup_issues = check_duplicates(c, existing_cases)
        if dup_issues:
            results["duplicates"].append({"case": c, "issues": dup_issues})
            continue
        
        if errors:
            results["invalid"].append({"case": c, "errors": errors})
        else:
            results["valid"].append(c)
    
    return results


# ── 报告生成 ──
def generate_report(candidates_results=None):
    """生成数据更新报告"""
    existing = load_existing()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"""# 电力案例集数据更新报告
> 生成时间：{now}

## 当前数据概况
- 总案例数：{len(existing)}
- 国家数：{len(set(c['country'] for c in existing))}
- 年份范围：{min(c['year'] for c in existing)} - {max(c['year'] for c in existing)}

## 国家分布
"""
    from collections import Counter
    countries = Counter(c['country'] for c in existing)
    for country, count in countries.most_common():
        report += f"- {country}: {count}\n"
    
    report += f"\n## 技术分布\n"
    techs = Counter()
    for c in existing:
        for t in c.get('tech', []):
            techs[t] += 1
    for tech, count in techs.most_common(15):
        report += f"- {tech}: {count}\n"
    
    if candidates_results:
        report += f"\n## 本次抓取结果\n"
        report += f"- 有效候选：{len(candidates_results.get('valid', []))}\n"
        report += f"- 无效数据：{len(candidates_results.get('invalid', []))}\n"
        report += f"- 重复数据：{len(candidates_results.get('duplicates', []))}\n"
        
        if candidates_results.get('invalid'):
            report += f"\n### 无效数据详情\n"
            for item in candidates_results['invalid']:
                report += f"- [{item['case'].get('id', '?')}] {item['case'].get('title', '?')}\n"
                for err in item['errors']:
                    report += f"  - ❌ {err}\n"
        
        if candidates_results.get('duplicates'):
            report += f"\n### 重复数据详情\n"
            for item in candidates_results['duplicates']:
                report += f"- [{item['case'].get('id', '?')}] {item['case'].get('title', '?')}\n"
                for issue in item['issues']:
                    report += f"  - ⚠️ {issue}\n"
    
    report_path = REPORT_DIR / f"update-report-{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已生成：{report_path}")
    return report_path


# ── 导出功能 ──
def export_csv(output_path=None):
    """导出为 CSV"""
    import csv
    existing = load_existing()
    if not output_path:
        output_path = PROJECT_DIR / "data" / "cases.csv"
    
    fieldnames = ['id', 'title', 'country', 'company', 'year', 'tech', 'scale',
                  'investment', 'roi', 'summary', 'source', 'tags', 'confidence']
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for c in existing:
            row = dict(c)
            row['tech'] = '|'.join(c.get('tech', []))
            row['tags'] = '|'.join(c.get('tags', []))
            writer.writerow(row)
    print(f"导出 {len(existing)} 条案例到 {output_path}")


def export_jsonl(output_path=None):
    """导出为 JSONL"""
    existing = load_existing()
    if not output_path:
        output_path = PROJECT_DIR / "data" / "cases.jsonl"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for c in existing:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
    print(f"导出 {len(existing)} 条案例到 {output_path}")


# ── 主流程 ──
def cmd_validate():
    """校验现有数据"""
    existing = load_existing()
    errors = []
    warnings = []
    seen_ids = set()
    
    for i, c in enumerate(existing):
        prefix = f"[{i+1}] {c.get('id','?')}"
        for field in ['id', 'title', 'country', 'company', 'year', 'tech', 'scale', 'investment', 'roi', 'summary', 'source', 'tags']:
            if field not in c or not c[field]:
                errors.append(f"{prefix}: 缺少必填字段 '{field}'")
        if c.get('id') in seen_ids:
            errors.append(f"{prefix}: ID '{c['id']}' 重复")
        seen_ids.add(c.get('id'))
    
    print(f"校验完成：{len(errors)} 错误，{len(warnings)} 警告")
    for e in errors:
        print(f"  ❌ {e}")
    for w in warnings:
        print(f"  ⚠️ {w}")
    return len(errors) == 0


def cmd_fetch():
    """抓取新闻并生成候选（占位——实际由 cron 子代理执行）"""
    print("新闻抓取应由 cronjob 触发的子代理执行")
    print("子代理使用 web_search 搜索最新电力行业新闻，提取候选案例")
    print("候选案例保存到 data/candidates.json")
    print("")
    print("手动测试：运行 python3 scripts/cases_automation.py --full")


def cmd_report():
    """生成报告"""
    candidates_results = None
    if CANDIDATES_FILE.exists():
        candidates = load_candidates()
        candidates_results = validate_candidates(candidates)
    generate_report(candidates_results)


def cmd_full():
    """完整流程"""
    print("=== 1. 校验现有数据 ===")
    cmd_validate()
    
    print("\n=== 2. 检查候选数据 ===")
    if CANDIDATES_FILE.exists():
        candidates = load_candidates()
        existing = load_existing()
        results = validate_candidates(candidates, existing)
        print(f"有效: {len(results['valid'])}, 无效: {len(results['invalid'])}, 重复: {len(results['duplicates'])}")
    else:
        print("无候选数据，跳过")
    
    print("\n=== 3. 生成报告 ===")
    cmd_report()
    
    print("\n=== 4. 导出数据 ===")
    export_csv()
    export_jsonl()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='电力案例集数据自动化管理')
    parser.add_argument('--validate', action='store_true', help='校验现有数据')
    parser.add_argument('--fetch', action='store_true', help='抓取新闻（提示）')
    parser.add_argument('--report', action='store_true', help='生成报告')
    parser.add_argument('--export-csv', action='store_true', help='导出CSV')
    parser.add_argument('--export-jsonl', action='store_true', help='导出JSONL')
    parser.add_argument('--full', action='store_true', help='完整流程')
    args = parser.parse_args()
    
    if args.validate:
        cmd_validate()
    elif args.fetch:
        cmd_fetch()
    elif args.report:
        cmd_report()
    elif args.export_csv:
        export_csv()
    elif args.export_jsonl:
        export_jsonl()
    elif args.full:
        cmd_full()
    else:
        cmd_full()
