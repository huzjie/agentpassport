# 贡献指南

感谢你对 agentpassport 的关注。

## 开发流程

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feat/xxx`
3. 提交修改并附清晰说明
4. 推送并提交 Pull Request

## 代码规范

- 内核保持零第三方依赖（仅 Python 标准库）
- 新 Provider 实现 `Provider.complete()`
- 新合规框架在 `policy/compliance.py` 增加分支
- 为新增功能补单元测试（`tests/`）

## 提交信息

使用约定式提交：`feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`。
