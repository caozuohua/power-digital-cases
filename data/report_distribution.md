# 配电维度案例搜索报告

## 搜索概况

**搜索时间**: 2026-06-25  
**搜索方向**: 5个方向（distribution automation/FLISR, smart feeder, V2G integration, microgrid controller, 配电自动化智能台区）  
**有效案例**: 5条  
**输出文件**: candidates_distribution.json

## 搜索策略与结果

| # | 搜索方向 | 关键词 | 结果 |
|---|---------|--------|------|
| 1 | FLISR配电自动化 | "distribution automation" FLISR utility 2025 | 找到Huntsville Utilities/SEL 46kV输配电FLISR案例，含详尽数据 |
| 2 | 智能馈线 | "smart feeder" pilot utility 2025 | 搜索结果偏向智能鸟食器(产品歧义)，无直接相关案例，改为FLISR深入搜索 |
| 3 | V2G配电融合 | "V2G" "distribution" grid integration 2025 | 找到Eurelectric/EY研究和美国DOE VGI评估报告，数据丰富 |
| 4 | 微电网控制器 | "microgrid controller" utility DER 2025 | 找到Eaton/Xendee合作案例，AI驱动的微电网控制器 |
| 5 | 中文配电自动化 | 配电自动化 智能台区 2025 | 找到国家发改委配电网高质量发展政策及华为配电网数字化指标体系 |

## 案例概览

| ID | 标题 | 国家 | 年份 | 置信度 |
|----|------|------|------|--------|
| us-hunts-001 | Huntsville Utilities与Redstone Arsenal部署46kV FLISR自愈系统 | 美国 | 2025 | 高 |
| eu-eurel-001 | Eurelectric与EY联合V2G配电融合研究：年节省40亿欧元 | 英国 | 2025 | 高 |
| us-doe-vgi001 | 美国DOE车网融合评估：2030年100TWh充电需求挑战配电系统 | 美国 | 2025 | 高 |
| cn-ndrc-001 | 国家发改委配电网高质量发展指导意见，推动配电智能化转型 | 中国 | 2024 | 高 |
| us-eaton-001 | Eaton与Xendee合作AI微电网控制器，加速DER管理部署 | 美国 | 2025 | 中 |

## 去重检查

- 已读cases.json中315条案例ID，所有5条新案例ID均不重复
- 新ID命名：us-hunts-001, eu-eurel-001, us-doe-vgi001, cn-ndrc-001, us-eaton-001

## 备注

- "smart feeder"搜索存在严重歧义(与智能鸟食器产品混淆)，后续可考虑用"smart feeder reconfiguration"或"intelligent feeder automation"替代
- web_search与web_extract在搜索后期遇到订阅配额限制(SUBSCRIPTION_REQUIRED)，部分URL无法二次提取详情
- us-eaton-001置信度为"中"，因详细部署数据有限，主要是平台合作公告
- eu-eurel-001的国家标注为"英国"(Eurelectric总部在布鲁塞尔，但该研究由EY英国主导发布)
