"""tag_converge.py: 标签收敛 496 -> ~60"""
import json
from collections import Counter

cases = json.load(open('/home/caozuohua99/power-digital-cases/data/cases.json'))
existing_count = Counter()
for c in cases:
    for t in c.get('tags', []):
        existing_count[t] += 1

# 直接映射表: 旧标签 -> 新标签
M = {}
# AI 类
for t in ['AI', 'AI大模型','AI调度','AI节能','AI健康度预测','AI健康度评估','AI诊断','AI检测',
          'AI故障诊断','AI图像识别','AI交易','AI算力','AI预测','GenAI','AI代理','AI微电网',
          '机器学习','深度学习','强化学习','自然语言处理','计算机视觉','大模型','知识图谱',
          '多模态','智能体','AI交易','AI电力系统']:
    M[t] = 'AI'

# 智慧X -> 智能电网
for t in ['智慧能源','智慧电网','智慧电厂','智慧运维','智慧调度','智慧配电','智慧运营',
          '数字员工','数字电网','电网智能化','新型电力系统','电力企业','电力管理',
          '电力监控','电力数字化','智慧能源岛','智慧社区','智慧风场','智慧电场',
          '智慧海洋','智慧加油站','智慧配电网','智慧风场','智慧电厂']:
    M[t] = '智能电网'

# DERMS/微电网
for t in ['DERMS','DER管理','微网','微电网','就地消纳']:
    M[t] = '微电网'

# 储能
for t in ['户用储能','用户侧储能','共享储能','新型储能','构网型储能','构网型控制',
          '虚拟惯量','储能调度','氢能','抽水蓄能','新型储能','电池储能','BESS','储能']:
    M[t] = '储能'

# 营销
for t in ['PPA','电力市场交易','现货市场','容量市场','辅助服务市场','辅助服务',
          '电力市场','碳交易','碳减排','碳排放','碳排放权','CCER','绿电证书','绿电溯源',
          '绿电交易','绿电聚合','绿电','电力平衡市场','客户能源管理','工商业能源管理',
          '住宅光储','工商业用户','综合能源服务','净计量']:
    M[t] = '营销'

# 虚拟电厂
for t in ['虚拟电厂','VPP','聚合运营','源网荷储协同','源网荷储']:
    M[t] = '虚拟电厂'

# 需求侧管理
for t in ['需求响应','需求侧管理']:
    M[t] = '需求侧管理'

# 数字孪生
for t in ['数字孪生','数字孪生调度','数字变电站']:
    M[t] = '数字孪生'

# 电网调度
for t in ['城市电网调度','电网调度','调度自动化','调度优化','输电调度','DNE调度',
          '调度预演','电网调度自动化']:
    M[t] = '电网调度'

# IoT
for t in ['物联网','在线监控']:
    M[t] = 'IoT'

# 数字孪生
for t in ['数字孪生调度']:
    M[t] = '数字孪生'

# 数字孪生
for t in ['5G通信','5G专网','5G边缘计算']:
    M[t] = '5G'

# 军事
for t in ['军事','国防电网','军工配网']:
    M[t] = '军事'

# 配电自动化
for t in ['FLISR']:
    M[t] = '配电自动化'

# 光伏
for t in ['太阳能','光伏组件','分布式光伏','光伏','光储一体化','户用光伏']:
    M[t] = '光伏'

# 风电
for t in ['风电预测','风储一体化','海上风电','风电']:
    M[t] = '风电'

# 其他保持不变但去空

# 第二轮收敛: 移除非技术标签(公司名/地名/描述词) 并 合并近似技术词
TECH_TAGS = {
    'AI', '智能电网', '数字孪生', 'IoT', '营销', '储能', '虚拟电厂',
    '需求侧管理', '电网调度', '光伏', '风电', '数据中心', '5G',
    '区块链', '可再生能源', '智能电表', '微电网', '配电自动化',
    'V2G', '数字变电站', '状态检修', '智慧城市', '故障自愈',
    '云边协同', '在线监测', '负荷预测', '源网荷储'}

for c in cases:
    new_tags = []
    seen = set()
    for t in c.get('tags', []):
        mapped = M.get(t, t)
        # 只保留技术标签(或在TECH_TAGS中)
        if mapped in TECH_TAGS and mapped not in seen:
            new_tags.append(mapped)
            seen.add(mapped)
    # 兜底: 如果tags全空 至少给一个大类
    if not new_tags:
        new_tags = ['智能电网']
    c['tags'] = sorted(new_tags)

# 统计
final = Counter()
for c in cases:
    for t in c.get('tags', []):
        final[t] += 1

with open('/home/caozuohua99/power-digital-cases/data/cases.json', 'w') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print(f'收敛: {len(existing_count)}种 -> {len(final)}种')
print()
for t, cnt in sorted(final.items(), key=lambda x: -x[1]):
    print(f'  {t}: {cnt}')
