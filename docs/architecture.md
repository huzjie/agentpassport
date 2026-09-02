# 架构设计

## 设计原则

1. **零依赖内核**：核心只用 Python 标准库，开箱即用，可离线部署在隔离 / air-gapped 环境。
2. **拒绝式默认**：安全策略默认拒绝，未明确允许即拦截，符合零信任。
3. **哈希链不可篡改**：所有审计记录以哈希链串联，任何改动都会破坏链完整性。
4. **闭环治理**：护照（身份）→ 审计（合规）→ 溯源（留痕）→ 信道（通信）四子系统互相咬合。

## 模块职责

| 模块 | 职责 | 关键类 |
| --- | --- | --- |
| `passport/` | 身份签发与校验 | `PassportAuthority`、`PassportVerifier`、`RevocationList` |
| `provenance/` | 全链路留痕 | `AttestationChain`、`ReplayGuard`、`TamperDetector` |
| `audit/` | 循环审计 | `Auditor`、`ContinuousAuditor`、`DriftDetector` |
| `channel/` | 信道监控 | `ChannelMonitor`、`TopologyPolicy`、`AnomalyDetector` |
| `policy/` | 策略与合规 | `PolicyEngine`、`DEFAULT_RULES`、`compliance` |
| `providers/` | LLM 适配 | `Provider` 抽象 + OpenAI 兼容 + mock |
| `storage/` | 持久化 | `SqliteBackend` + 四个业务 store |
| `observability/` | 可观测 | `Metrics`（Prometheus）、`TraceContext`（W3C） |
| `api/` | HTTP 控制面 | 标准库 `http.server` |
| `cli/` | 命令行 | 10 个子命令 |

## 数据流

一次「审计动作」的完整链路：

```
audit_action(agent_id, action)
  → passport_store.get(agent_id)         # 加载护照
  → auditor.audit(passport, action)      # 策略判定 + 护照校验
      → policy.evaluate(...)             #   默认拒绝 + 合规
      → verifier.validate(...)           #   签名/过期/吊销
      → audit_ledger.append(rec)         #   写入哈希链账本
  → drift.observe(agent_id, action)      # 记录行为，供漂移检测
  → metrics.inc("audits_total")          # 指标
```

## 扩展点

- **新增 Provider**：在 `providers/` 实现 `Provider.complete()` 并在 `registry.py` 注册。
- **新增合规框架**：在 `policy/compliance.py` 的 `check()` 增加分支。
- **新增存储后端**：实现 `storage/store.py` 中 store 的接口，替换 SQLite。
