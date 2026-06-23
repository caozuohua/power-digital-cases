# 数据更新自动化方案

## 架构

```
定时触发 (cronjob)
  → 子代理搜索全球电力行业新闻
  → 提取候选案例（结构化）
  → 自动校验（去重/格式/完整性）
  → 生成 PR（GitHub Actions）
  → 人工审核合入
```

## 流程

### 1. 定时触发
- cronjob 每周执行一次（周一 09:00 UTC）
- 触发数据更新子代理

### 2. 子代理任务
子代理执行以下搜索任务：
- 搜索过去一周电力行业数字化转型新闻
- 关键词：smart grid, digital transformation, AI energy, IoT power, VPP, energy storage, hydrogen, renewable
- 来源：Reuters, Bloomberg, PV Magazine, Utility Dive, 中国电力网等
- 提取候选案例并保存到 `data/candidates.json`

### 3. 自动校验
- 运行 `scripts/cases_automation.py --validate`
- 检查：必填字段、ID唯一性、重复检测、格式规范
- 输出：有效/无效/重复分类

### 4. PR 生成
- GitHub Actions 自动创建 PR
- PR 内容：新增候选案例 + 校验报告
- 人工审核后合入 main

### 5. 报告
- 每次更新生成报告到 `reports/` 目录
- 包含：新增数量、国家分布、技术分布、数据质量
