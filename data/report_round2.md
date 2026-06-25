# 第二轮补充采集报告（变电+调度+用电）

## 采集状态：✅ 完成

**日期**: 2026-06-25  
**子代理**: deleg_d2c9eaf4

## 候选文件

| 文件 | 状态 | 条目数 |
|------|------|--------|
| candidates_transformer_r2.json | ✅ 已生成 | 8 |
| candidates_dispatch_r2.json | ✅ 已生成 | 8 |
| candidates_usage_r2.json | ✅ 已生成 | 7 |

## 合并结果

| 指标 | 数值 |
|------|------|
| 合并前总数 | 352 |
| 新增条目 | 23 |
| 合并后总数 | 375 |
| ID 冲突数 | 0 |
| tech 字段修正数 | 0（已标准化） |

## 新增案例摘要

### 变电/变压器（transformer_r2）
- it-enel-c3-001: Enel意大利16000座变电站C3 AI预测性维护
- jp-tepco-dx2-002: TEPCO DX 2.0 AI辅助调度+数字孪生电网
- kr-kepco-digital-002: KEPCO全韩数字化变电站+5G通信
- ...等8条

### 调度（dispatch_r2）
- de-tennet-001: Tennet AI风电预测与电网调度优化
- uk-ngeso-001: National Grid ESO动态线路额定值+AI调度
- ...等8条

### 用电（usage_r2）
- us-schneid-ems001: 施耐德EcoStruxure商业建筑能源管理
- us-tesla-vpp001: 特斯拉Autobidder虚拟电厂
- ...等7条

## 未解决问题
- candidates_dispatch_r2.json 中部分条目字段名使用 `title(中文)` / `country(中文国家名)`，已在合并时统一为 `title` / `country`
- 建议：后续采集统一使用英文字段名

---
*报告自动生成 by 监控代理*
