# 中国案例校对报告 (Batch A)

## 校对概览

| 项目 | 数值 |
|------|------|
| 数据文件 | cases.json |
| 中国案例总数 | 96 条 |
| 本次校对数量 | 50 条（前50条） |
| 校对日期 | 2026-06-25 |
| 校对标准 | title准确性、year范围(2020-2026)、tech标签合规性、summary长度(≥100字)、confidence合理性 |

---

## 校对结果统计

### 各类问题统计

| 问题类型 | 涉及案例数 | 占比 |
|----------|-----------|------|
| tech标签不合规 | 38 | 76% |
| summary长度不足(<100字) | 32 | 64% |
| title过于泛泛 | 2 | 4% |
| year超出范围 | 0 | 0% |
| confidence不合理 | 0 | 0% |

### 结论
- ✅ **year字段**：全部50条案例year均在2020-2026范围内，无问题
- ✅ **confidence字段**：全部为"高"，合理
- ⚠️ **tech标签合规性**：38条（76%）存在不合规的tech标签，为最突出问题
- ⚠️ **summary长度**：32条（64%）summary不足100字
- ⚠️ **title准确性**：2条title过于泛泛

---

## 高频不合规tech标签排行

| 不合规标签 | 出现频次 | 建议替换为 |
|-----------|---------|-----------|
| AI大模型 | ~25 | AI |
| 无人机 | ~7 | 删除（不在允许列表） |
| 数字化 | ~5 | 数字孪生 / 大数据 |
| 强化学习 | ~3 | 删除 |
| 绿氢 | ~3 | 智慧能源 / 储能 |
| BIM | ~3 | 数字孪生 |
| 智能建造 | ~3 | 数字孪生 |
| 机器人 | ~3 | AI / 智能电网 |
| 机器视觉 | ~3 | AI |
| 能源交易 | ~3 | 删除 |
| 深度学习 | ~2 | 删除 |
| 知识图谱 | ~2 | 删除 |
| 其他（产品名/非技术标签） | 若干 | 删除 |

> **核心问题**："AI大模型"是最大问题。数据中存在大量"AI大模型"但允许列表中只有"AI"，应统一替换。

---

## 典型案例问题详情

### 严重案例（多项问题）

**cn-cnnc-001** - 中核漳州核电2号机组商运
- tech全部不合规：核电、华龙一号、数字化、智能运维均不在允许列表
- summary仅65字，不达标

**vendor-zte-003** - 中兴通讯 2026能源网络通信创新应用
- tech全部不合规：数字化、AI算力、通信网络、绿色低碳
- summary仅26字，严重不足

**cn-sgcc-metering-001** - 国家电网智能电表全覆盖项目
- tech不合规：AMI、智能电表不在允许列表
- summary仅58字，不达标

### 需关注title问题

**cn-sgcc-digital-001** - "国家电网数字化转型综合示范区"
- 问题：title泛泛使用"数字化转型"，不够具体
- 建议：改为"国家电网AI+数字孪生综合示范区"

**cn-csg-new-001** - "南方电网新型电力系统数字化示范区"
- 问题：title泛泛使用"数字化"
- 建议：改为"南方电网AI+区块链源网荷储示范区"

---

## 允许tech列表

```
AI, 数字孪生, 智能电网, IoT, 大数据, 人工智能, 区块链, 云计算, 
5G, 边缘计算, 网络安全, 储能, 光伏, 风电, 配电自动化, 
虚拟电厂, 微电网, 需求侧管理, 智慧能源
```

---

## 修正优先级建议

1. **P0 - 立即修复**：将所有"AI大模型"替换为"AI"（影响约25条案例）
2. **P1 - 重要**：清理产品名/非技术标签（瑞元、如意、SSC600、华龙一号等）
3. **P2 - 重要**：统一替换明显错误标签（数字化→数字孪生，大数据分析→大数据，微网→微电网）
4. **P3 - 建议**：扩展不足100字的summary（影响32条案例）
5. **P4 - 优化**：改进2条泛泛的title

---

## 未校对案例

本次校对前50条中国案例，剩余46条（id: cn-spic-hydrogen-001 及之后）未纳入本次校对范围。如需校对剩余案例，可继续执行下一批次。

---

## 附录：50条校对案例ID列表

cn-envision-008, cn-cnnc-001, cn-cgn-001, cn-spic-vpp-001, cn-envision-009, cn-envision-010, cn-spic-ai-001, cn-sgcc-ai-010, cn-catl-007, cn-sgcc-iot-005, cn-csg-ai-013, cn-huanneng-009, cn-datang-006, cn-rosed-006, cn-xd-006, cn-dongfang-006, cn-three-gorges-007, vendor-nari-002, vendor-nari-003, vendor-zte-003, vendor-abb-001, cn-envision-002, cn-sgcc-vpp-002, cn-spic-hydrogen-002, cn-envision-003, cn-catl-002, cn-vision-002, cn-sinopec-002, vendor-huawei-001, vendor-huawei-004, vendor-nari-001, vendor-zte-001, vendor-zte-002, vendor-abb-002, vendor-abb-003, cn-sgcc-ai-dispatch-001, cn-csg-ai-001, cn-sgcc-digital-001, cn-csg-new-001, cn-catl-smart-001, cn-spic-nuclear-002, cn-envision-storage-001, cn-csg-ai-002, cn-csg-vpp-002, cn-spic-wind-002, cn-sgcc-ai-001, cn-csg-ai-003, cn-csg-001, cn-huadian-001, cn-spic-nuclear-001, cn-csg-digital-001, cn-sgcc-vpp-001, cn-spic-offshore-001
