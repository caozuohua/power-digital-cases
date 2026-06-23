# ⚡ 全球电力行业数字化项目案例集

Power Industry Digital Transformation Case Studies

## 简介

搜集整理全球电力行业数字化转型项目案例，涵盖火电、水电、核电、风电、光伏、储能、电网、配电等领域。

## 功能

- 全文搜索（名称/企业/技术/国家/摘要）
- 多维度筛选（国家、规模、年份）
- 标签云快速过滤
- 案例详情弹窗
- 响应式设计，移动端友好

## 数据

所有案例数据存放在 `data/cases.json`，唯一数据源。

### 字段说明

| 字段 | 说明 |
|------|------|
| id | 唯一标识 |
| title | 项目名称 |
| country | 国家/地区 |
| company | 企业 |
| year | 年份 |
| tech | 技术标签（数组） |
| scale | 规模（大型/中型/小型） |
| investment | 投资额 |
| roi | 成效/ROI |
| summary | 摘要 |
| detail | 详情 |
| source | 来源链接 |
| tags | 自由标签（数组） |

## 本地预览

```bash
# 任意静态服务器即可
python3 -m http.server 8000
# 或
npx serve .
```

## 部署

推送至 GitHub 后自动通过 GitHub Actions 部署到 Pages。

## 贡献

欢迎提交新案例。在 `data/cases.json` 中按现有格式添加即可。
