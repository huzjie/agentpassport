# 策略引擎（Policy）

## 默认拒绝

`PolicyEngine` 采用拒绝式默认策略：未明确允许即拒绝（`default: deny`）。

## 评估顺序

1. 高危动作黑名单（`delete-production`、`exfiltrate` 等）
2. 能力校验（`match_rule` + 护照能力声明）
3. 合规框架检查
4. 默认拒绝

## 内置规则

`DEFAULT_RULES` 覆盖 read/query/search/write/call/send 等基础动作（允许）与 execute/run/delegate 等高风险动作（拒绝）。
