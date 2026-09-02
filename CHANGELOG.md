# 变更日志

## [1.0.0] - 2026-08-31

### 新增
- 数字护照：签发 / 校验 / 续期 / 吊销 + 吊销列表（CRL）
- 全链路溯源：证明链（parent_hash）、重放防护（nonce 时间窗）、防伪造检测
- 循环审计：审计引擎 + 后台循环审计 + 能力漂移检测
- 信道监控：拓扑策略（hub/chain/broadcast/tree/star）+ 未授权信道阻断 + 异常高频检测
- 策略引擎：拒绝式默认 + 内置规则 + 合规框架（EU AI Act / 中国智能体治理）
- 哈希链账本（防篡改追加）+ SQLite 存储层
- LLM Provider：OpenAI 兼容 8 家 + Anthropic + Mock（零依赖离线）
- HTTP 控制面（标准库）+ CLI + Python/TypeScript SDK + Web 控制台
- 部署：Docker / docker-compose / K8s / Helm / CI / CodeQL
