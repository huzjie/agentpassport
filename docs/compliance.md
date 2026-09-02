# 合规对照

## 欧盟 AI Act（GPAI 执法权已激活）

- 高风险动作（execute/run/delegate）要求 `human_oversight` 元数据
- 全链路日志留存满足透明度义务

## 中国智能体治理（数字护照 + 循环审计 + Harness 法定嵌入）

- 数字护照指纹强制（缺指纹即拒绝）
- 委派动作需 `registered` 备案标记
- 哈希链 + 证明链满足「留痕」义务

## 如何扩展

在 `policy/compliance.py` 的 `check()` 中增加新框架分支即可。
