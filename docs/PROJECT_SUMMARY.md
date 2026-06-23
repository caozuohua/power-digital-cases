# 电力行业数字化项目案例集 — 项目总结

> 最后更新：2026-06-23
> 数据文件：`data/cases.json`（281条，41国）
> 在线地址：https://caozuohua.github.io/power-digital-cases
> 仓库：https://github.com/caozuohua/power-digital-cases

---

## 一、项目结构

```
power-digital-cases/
├── data/
│   └── cases.json              # 唯一数据源（281条）
├── src/                        # 前端（纯静态HTML+CSS+JS）
│   ├── index.html              # 首页：搜索+筛选+标签云+卡片列表
│   ├── css/style.css
│   └── js/app.js               # 搜索/筛选/渲染/弹窗
├── scripts/
│   ├── validate.py             # 数据质量校验（字段/ID/重复/格式）
│   ├── dedup.py                # 重复检测引擎（ID/标题/URL/企业+年份）
│   └── cases_automation.py     # 自动化脚本（校验+报告+导出CSV/JSONL）
├── .github/workflows/
│   ├── deploy.yml              # 自动部署到GitHub Pages
│   └── weekly-update.yml        # 每周一自动校验+创建PR
├── docs/
│   └── automation.md           # 自动化方案说明
└── README.md
```

## 二、数据模型

```json
{
  "id": "cn-sgcc-001",          // 唯一标识：国家代码-公司缩写-序号
  "title": "项目名称",
  "country": "中国",
  "company": "企业",
  "year": 2025,
  "tech": ["AI", "数字孪生"],    // 技术标签数组
  "scale": "大型",                // 大型/中型/小型
  "investment": "5000万+",
  "roi": "成效描述",
  "summary": "200字摘要",
  "detail": "详细描述（可选）",
  "source": "https://...",      // 来源URL（必须可访问）
  "tags": ["标签1", "标签2"],   // 自由标签数组
  "confidence": "高"             // 高=官方来源 / 中=新闻报道 / 低=行业报告
}
```

## 三、当前数据覆盖

### 大洲分布
| 大洲 | 案例数 | 主要国家 |
|---|---|---|
| 亚洲 | 155 | 中国107、印度7、泰国6、越南6、日本5、韩国4 |
| 欧洲 | 52 | 德国6、挪威6、意大利5、西班牙5、法国4、英国4 |
| 北美 | 32 | 美国29、墨西哥3 |
| 非洲 | 19 | 尼日利亚5、肯尼亚5、南非4、埃及2、摩洛哥2、莫桑比克1 |
| 南美 | 13 | 哥伦比亚7、巴西6 |
| 大洋洲 | 3 | 澳大利亚3 |
| 全球 | 4 | 厂商跨国案例 |

### 年份分布
| 年份 | 案例数 |
|---|---|
| 2020 | 5 |
| 2021 | 14 |
| 2022 | 42 |
| 2023 | 67 |
| 2024 | 15 |
| **2025** | **108** |
| **2026** | **30** |

### 技术TOP5
AI(185) / IoT(109) / 数字孪生(93) / 大数据(75) / AI大模型(55)

### 厂商案例（18条）
华为4 / 国电南瑞3 / ABB 3 / 中兴2 / Hitachi Energy 2 / Nokia 1 / Siemens Energy 1

## 四、自动化流程

### 定时任务
- **cronjob** `weekly-power-cases-update`：每周一 UTC 01:00 触发
- 子代理搜索全球电力行业新闻 → 提取候选案例 → 写入 `data/candidates.json`
- 自动去重检查 → 输出摘要

### GitHub Actions
- `deploy.yml`：push到main自动部署到Pages
- `weekly-update.yml`：每周一自动校验+创建PR

### 数据校验
```bash
python3 scripts/validate.py data/cases.json        # 质量校验
python3 scripts/dedup.py                           # 重复检测
python3 scripts/dedup.py --check new_cases.json    # 新数据去重
python3 scripts/cases_automation.py --full          # 完整流程
python3 scripts/cases_automation.py --export-csv   # 导出CSV
```

## 五、后续收集指南

### 收集优先级（按2025+2026案例潜力）

**第1优先级：欧洲缺失**
- 瑞典（现有3条，2025+仅2）
- 西班牙（现有5条，2025+仅3）
- 意大利（现有5条，2025+仅3）
- 挪威（现有6条，2025+仅4）

**第2优先级：东南亚**
- 菲律宾（现有4条，全是2025+）
- 泰国（现有6条，2025+仅4）
- 越南（现有6条，2025+仅4）

**第3优先级：中东扩展**
- 约旦（现有3条，全是2025）
- 阿曼（现有3条，全是2025）
- 沙特（现有3条，2025+仅1）

**第4优先级：非洲扩展**
- 南非（现有4条，2025+仅3）
- 尼日利亚（现有5条，2025+仅4）
- 肯尼亚（现有5条，2025+仅4）

**第5优先级：厂商官网**
- 华为：https://e.huawei.com/cn/industries/grid
- 国电南瑞：https://www.sasac.gov.cn
- 中兴通讯：https://www.zte.com.cn/china/enterpriseindustry/energy_industry_solution.html
- ABB：https://new.abb.com/cn/about/businesses/electrification
- Hitachi Energy：https://www.hitachienergy.com
- Nokia：https://www.nokia.com/industries/power-utilities
- Siemens Energy：https://www.siemens-energy.com

### 收集流程
1. 搜索目标国家/厂商的2025-2026年电力数字化新闻
2. 提取候选案例，按数据模型格式化
3. 写入临时文件 `data/candidates_batchN.json`
4. 运行 `python3 scripts/dedup.py --check data/candidates_batchN.json`
5. 去重通过后合并到 `data/cases.json`
6. 运行 `python3 scripts/validate.py data/cases.json`
7. 提交并推送

### 搜索关键词模板
- `"power industry digital transformation 2025 2026"`
- `"smart grid AI IoT project commissioned"`
- `"virtual power plant VPP 2025 2026"`
- `"energy storage digital platform AI"`
- `"power utility digital twin 2025 2026"`
- 加上目标国家/厂商名称

### 置信度标注标准
- **高**：有官方新闻稿/官网案例/权威媒体报道
- **中**：有行业报告提及/政府规划文件
- **低**：仅有学术论文/间接提及

## 六、Git断点记录

| Commit | 内容 |
|---|---|
| `0d04256` | P1: 项目骨架+10个种子案例 |
| `53315c4` | P2: 数据填充到55条+置信度筛选 |
| `72c6b5a` | P3: 数据填充到81条 |
| `40e8fc5` | P4: 数据填充到144条 |
| `da8f99c` | P5: 数据更新自动化+校验脚本 |
| `9d7d5bf` | P7: 2025年案例补充到185条 |
| `27fabf3` | P9: 美国案例补充到220条 |
| `3543709` | P10: 巴西/哥伦比亚/越南/伊拉克补充到235条 |
| `f1dac2d` | P11: 欧洲/东南亚/中东补充到255条 |
| `3f4d4e5` | P13: 厂商官网案例补充到281条 |
