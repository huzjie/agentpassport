# 常见问题

**Q: 需要安装第三方依赖吗？**
A: 不需要。核心只用 Python 标准库，复制 `config.example.json` 即可运行。

**Q: 支持哪些部署方式？**
A: 本地进程、Docker、Kubernetes、Helm，均提供现成配置。

**Q: 如何接入现有智能体框架？**
A: 通过 HTTP API 或 Python/TypeScript SDK，在智能体执行动作前调用 `/audit` 或 `/policy/evaluate`。

**Q: 审计账本可以修改吗？**
A: 账本为追加式哈希链，任何历史改动都会破坏链完整性，`chain-verify` 可随时校验。
