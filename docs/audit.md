# 循环审计（Continuous Audit）

## 审计引擎

`Auditor.audit(passport, action, context)`：

1. 护照校验（签名 / 过期 / 吊销）
2. 策略判定（默认拒绝 + 合规）
3. 产出 `AuditRecord` 并追加到哈希链账本

## 循环审计

`ContinuousAuditor` 后台线程周期性重审所有在册护照，检测：

- 过期 / 吊销 / 签名失效
- 能力漂移（实际行为超出声明范围）

`start()` 启动后台循环，`run_once()` 手动触发一轮，`last_report` 保存最近一轮违规清单。

## 漂移检测

`DriftDetector` 对比「护照声明能力」与「近期实际动作」，越权比例超过阈值即报警。
