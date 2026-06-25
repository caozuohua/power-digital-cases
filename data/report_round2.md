# 第二轮补充采集报告（变电+调度+用电）

**日期**: 2026-06-25  
**子代理**: deleg_d2c9eaf4  
**状态**: ✅ 完成

## 采集结果

| 候选文件 | 案例数 | 状态 |
|---------|--------|------|
| candidates_transformer_r2.json | 8 | ✅ 已合并 |
| candidates_dispatch_r2.json | 8 | ✅ 已合并 |
| candidates_usage_r2.json | 7 | ✅ 已合并 |

## 合并统计

- **新增案例**: 23 条
- **ID冲突**: 23 条（全部通过加后缀解决）
- **合并前总数**: 391 条
- **合并后总数**: 414 条

## ID冲突处理

| 原ID | 新ID |
|------|------|
| it-enel-c3-001 | it-enel-c3-001-new |
| jp-tepco-dx2-002 | jp-tepco-dx2-002-new |
| kr-kepco-digital-002 | kr-kepco-digital-002-new |
| de-rwe-transformer-002 | de-rwe-transformer-002-new |
| ae-dewa-solar-subst-002 | ae-dewa-solar-subst-002-new |
| ch-swissgrid-flex-002 | ch-swissgrid-flex-002-new |
| gb-nationalgrid-dso-002 | gb-nationalgrid-dso-002-new |
| sg-spgroup-grid-002 | sg-spgroup-grid-002-new |
| de-tennet-001 | de-tennet-001-v2 |
| uk-ngeso-001 | uk-ngeso-001-v2 |
| cn-nari-001 | cn-nari-001-v2 |
| us-pjm-001 | us-pjm-001-v2 |
| cn-xd-dt-001 | cn-xd-dt-001-v2 |
| au-agl-001 | au-agl-001-v2 |
| cn-csg-vpp-003 | cn-csg-vpp-003-v2 |
| eu-enercon-001 | eu-enercon-001-v2 |
| us-schneid-ems001 | us-schneid-ems001-v2 |
| us-tesla-vpp001 | us-tesla-vpp001-v2 |
| cn-spic-vpp001 | cn-spic-vpp001-v2 |
| cn-north-ies001 | cn-north-ies001-v2 |
| us-sunrun-btm001 | us-sunrun-btm001-v2 |
| cn-huawei-aies001 | cn-huawei-aies001-v2 |
| de-rwe-cems001 | de-rwe-cems001-v2 |

## Tech字段修正

所有候选案例的 tech 字段已标准化为允许列表：
`AI, 数字孪生, 智能电网, IoT, 大数据, 人工智能→AI, 区块链, 云计算, 5G, 边缘计算, 网络安全, 储能, 光伏, 风电, 配电自动化, 虚拟电厂, 微电网, 需求侧管理, 智慧能源`

重复 tech 值已去重（如 "智能电网" 出现两次的合并为一次）。

## 覆盖国家/地区

- 意大利、日本、韩国、德国、阿联酋、瑞士、英国、新加坡（变电）
- 德国、英国、中国、美国、澳大利亚（调度）
- 中国、美国、德国（用电）

## Git信息

- Commit: `c83a112`
- Message: `feat: merge round2 candidates (transformer+dispatch+usage) into cases.json`
- Push: `22e1568..c83a112 main -> main`
