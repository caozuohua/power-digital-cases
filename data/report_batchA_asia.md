# 亚洲电力案例校对报告 (Batch A)

**校对日期**: 2026-06-25  
**校对范围**: id 以 jp-、kr-、in-、th-、vn-、ph-、id-、my- 开头的案例  
**校对案例总数**: 37 条  
**发现问题总数**: 42 项  

---

## 一、总体统计

| 问题类型 | 数量 | 占比 |
|---------|------|------|
| summary 字数不足80字 | 16 | 38.1% |
| tech 标签不在允许列表中 | 19 | 45.2% |
| title 过于泛化 | 7 | 16.7% |
| id 与公司名不匹配 | 1 | 2.4% |
| 标题重复 | 1 | 2.4% |

**无问题案例**: 11 条 (jp-tepco-001, jp-kyushu-001, jp-kepco-001, in-tatapower-001, in-ntpc-001, kr-kepco-001, kr-kepco-ai-001, kr-kepco-smart-001, vn-evn-001, vn-evn-002, vn-evn-renewable-001, th-egat-001)

---

## 二、各国案例问题分布

### 🇯🇵 日本 (jp-) - 5条
| ID | 问题描述 |
|----|---------|
| jp-tepco-002 | title泛化（'DX 数字转型2.0'），summary过短 |
| jp-tepco-dx-001 | title泛化（'DX 数字转型白皮书项目'） |
| jp-tepco-001 | ✅ 无问题 |
| jp-kyushu-001 | ✅ 无问题 |
| jp-kepco-001 | ✅ 无问题 |

### 🇰🇷 韩国 (kr-) - 5条
| ID | 问题描述 |
|----|---------|
| kr-kepco-002 | summary过短（28字） |
| kr-kepco-ai-001 | ✅ 无问题 |
| kr-kepco-001 | ✅ 无问题 |
| kr-kepco-smart-001 | ✅ 无问题 |

### 🇮🇳 印度 (in-) - 7条
| ID | 问题描述 |
|----|---------|
| in-tatapower-002 | summary过短（30字） |
| in-ntpc-002 | summary过短（35字） |
| in-suzlon-002 | tech含SCADA（不允许），summary过短 |
| in-tatapower-001 | ✅ 无问题 |
| in-ntpc-001 | ✅ 无问题 |
| in-adani-001 | tech含无人机（不允许） |
| in-greenko-001 | id前缀与公司不匹配，tech含SCADA，summary过短 |

### 🇮🇩 印度尼西亚 (id-) - 3条
| ID | 问题描述 |
|----|---------|
| id-pln-002 | title泛化 |
| id-pln-001 | title泛化 |
| id-pln-ami-001 | tech含AMI/智能电表（不允许），summary过短 |

### 🇹🇭 泰国 (th-) - 7条
| ID | 问题描述 |
|----|---------|
| th-egat-002 | summary过短（33字） |
| th-gorilla-001 | tech含'数字化'（不允许） |
| th-egat-003 | tech含'可再生能源'（不允许），summary过短（25字） |
| th-pea-002 | tech含'数字化'（不允许），summary过短（22字） |
| th-pea-001 | tech含AMI（不允许） |
| th-egat-001 | ✅ 无问题 |

### 🇻🇳 越南 (vn-) - 7条
| ID | 问题描述 |
|----|---------|
| vn-evn-003 | title泛化，tech含'数字化'，summary过短 |
| vn-evn-002 | ✅ 无问题 |
| vn-evn-004 | title泛化，tech含'数字化'，summary过短 |
| vn-evn-005 | 标题与vn-evn-002重复 |
| vn-evn-001 | ✅ 无问题 |
| vn-evn-renewable-001 | ✅ 无问题 |

### 🇵🇭 菲律宾 (ph-) - 3条
| ID | 问题描述 |
|----|---------|
| ph-meralco-001 | tech含AMI/数字化，summary过短（25字） |
| ph-meralco-002 | title泛化，tech含数字化/数据平台，summary过短 |
| ph-meralco-003 | tech含'数字化'，summary过短 |

### 🇲🇾 马来西亚 (my-) - 3条
| ID | 问题描述 |
|----|---------|
| my-tnb-002 | tech含AMI/智能电表（不允许） |
| my-tnb-solar-001 | tech含无人机（不允许） |
| my-tnb-001 | tech含AMI/智能电表（不允许） |

---

## 三、高频问题分析

### 3.1 不允许的 tech 标签统计
| 标签 | 出现次数 | 建议替换 |
|------|---------|---------|
| 数字化 | 7 | 大数据 / IoT / 云计算 |
| AMI | 4 | 智能电网 / IoT |
| 智能电表 | 3 | IoT / 智能电网 |
| SCADA | 2 | 大数据 / IoT |
| 无人机 | 2 | IoT / 大数据 |
| 数据平台 | 1 | 大数据 |
| 可再生能源 | 1 | 光伏 / 风电 |

### 3.2 Title 泛化问题
以下title过于泛化，未准确反映项目实质：
- `东京电力 DX 数字转型2.0` → 应突出AI大模型+数字孪生
- `PLN 印尼智能电网数字化转型2.0` → 应突出AI大模型+数字孪生
- `EVN 2026年数字化转型关键任务` → 应突出AI+智能电网
- `Meralco 2025 AI峰会数字化战略` → 应突出Giga Summit与七大支柱

---

## 四、校对结论

1. **最严重问题**: summary字数不足是最高发问题（16/42），许多案例的summary仅20-35字，远未达80字要求。
2. **tech标签规范化**: '数字化'一词出现7次，属于泛化描述，应替换为具体技术标签。AMI、智能电表、SCADA、无人机等均需替换为允许列表中的标签。
3. **整体质量**: 11条案例（约30%）通过全部校对标准，质量较好；其余需修改后重新审核。
4. **year 合规性**: 所有37条案例的year均在2020-2026范围内，全部合规。
5. **confidence合理性**: 所有案例confidence为"高"或"中"，与数据详实程度基本匹配，无需调整。

---

*报告完成。修正详情见 corrections_batchA_asia.json*
