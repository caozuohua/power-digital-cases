# ⚡ 全球电力行业数字化项目案例集

> Power Industry Digital Transformation Case Studies — 全球电力行业数字化转型案例开放数据集

[![GitHub Pages](https://img.shields.io/badge/deploy-Pages-2ea44f)](https://caozuohua.github.io/power-digital-cases)
[![GitHub last commit](https://img.shields.io/github/last-commit/caozuohua/power-digital-cases)](https://github.com/caozuohua/power-digital-cases/commits/main)
[![Data](https://img.shields.io/badge/data-483%20cases-3b82f6)](data/cases.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🌐 在线浏览：https://caozuohua.github.io/power-digital-cases

## 概述

搜集整理全球电力行业数字化转型项目案例，涵盖火电、水电、核电、风电、光伏、储能、电网、配电等全领域。

### 数据规模

| 指标 | 数据 |
|------|------|
| 总案例数 | **483** |
| 覆盖国家 | **43** |
| 涉及企业 | **191** |
| 年份跨度 | 2020–2026 |

### 技术标签 TOP 10

`AI`(395) · `IoT`(249) · `大数据`(249) · `智能电网`(237) · `数字孪生`(157) · `储能`(80) · `云计算`(77) · `虚拟电厂`(49) · `边缘计算`(41) · `光伏`(40)

## 功能

- 🔍 **全文搜索** — 按名称、企业、技术、国家、摘要即时检索
- 🌍 **交互式地图** — Leaflet 地图按国家分布展示，点击定位到案例
- 📊 **数据可视化** — 趋势图、置信度分布等图表（Canvas 纯前端渲染）
- 🏷️ **标签云** — 技术标签快速过滤
- 📱 **响应式设计** — 桌面/移动端适配

## 项目结构

```
power-digital-cases/
├── index.html              # 首页（搜索+筛选+地图+图表+卡片列表）
├── css/style.css           # 样式
├── js/app.js               # 前端逻辑（搜索/筛选/地图/图表/弹窗）
├── data/
│   └── cases.json          # 📌 唯一数据源（483 条）
├── scripts/
│   ├── validate.py         # 数据质量校验
│   ├── dedup.py            # 重复检测引擎
│   ├── cases_automation.py # 自动化脚本（校验+报告+导出）
│   ├── clean_scale.py      # 规模字段标准化
│   └── tag_converge.py     # 技术标签归并
├── docs/
│   └── PROJECT_SUMMARY.md  # 项目总结与收集指南
└── .github/workflows/
    ├── deploy.yml          # push → GitHub Pages 自动部署
    └── weekly-update.yml   # 每周一 UTC 01:00 自动校验+创建 PR
```

## 数据模型

```json
{
  "id": "cn-sgcc-001",          // 唯一标识：国家代码-公司缩写-序号
  "title": "项目名称",
  "country": "中国",
  "company": "企业",
  "year": 2025,
  "tech": ["AI", "数字孪生"],
  "scale": "大型",
  "investment": "5000万+",
  "roi": "成效描述",
  "summary": "200字摘要",
  "detail": "详细描述（可选）",
  "source": "https://...",
  "tags": ["标签1", "标签2"],
  "confidence": "高"        // 高=官方 / 中=新闻报道 / 低=行业报告
}
```

## 本地运行

```bash
python3 -m http.server 8000
# 或
npx serve .
```

## 自动化

| 工作流 | 触发 | 说明 |
|--------|------|------|
| `deploy.yml` | push 到 main | 自动构建并部署到 GitHub Pages |
| `weekly-update.yml` | 每周一 UTC 01:00 | 自动校验数据质量 + 创建 PR 供审核 |

```bash
# 数据校验
python3 scripts/validate.py data/cases.json
python3 scripts/dedup.py
python3 scripts/dedup.py --check new_cases.json
python3 scripts/cases_automation.py --full
python3 scripts/cases_automation.py --export-csv
```

## 贡献

欢迎提交新案例！

1. 按数据模型格式化后添加到 `data/cases.json`
2. 运行校验：`python3 scripts/validate.py data/cases.json`
3. 运行去重：`python3 scripts/dedup.py`
4. 提交 PR

### 命名规范

ID 格式：`{国家代码}-{公司缩写}-{序号}`（如 `cn-sgcc-001`）

### 置信度标准

- **高** — 官方新闻稿/官网案例/权威媒体报道
- **中** — 行业报告提及/政府规划文件
- **低** — 学术论文/间接提及

详细收集指南见 [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)。

## License

MIT
