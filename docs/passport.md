# 数字护照（Passport）

## 概念

数字护照是智能体的**可验证身份凭证**，包含：

- `agent_id`：全局唯一 ID
- `name` / `owner`：名称与所属团队
- `provider` / `model`：底层模型
- `capabilities`：能力声明（动作 + 范围 + 风险等级）
- `issued_at` / `expires_at`：签发与过期时间
- `fingerprint`：内容 SHA-256 指纹（防篡改）
- `signature`：基于 `secret` 的 HMAC 签名

## 生命周期

```
issue（签发） → active（生效） → renew（续期） → revoke（吊销）
                   │
                   └── suspended（挂起）
```

## 校验流程

`PassportVerifier.validate()` 依次检查：

1. 指纹与签名是否一致（防篡改）
2. 状态是否为 revoked
3. 是否在吊销列表（CRL）中
4. 是否已过期

任一步失败抛出对应异常（`PassportInvalidError` / `PassportRevokedError` / `PassportExpiredError`）。

## 能力声明

内置标准能力模板见 `passport/capability.py`：`read-data`、`write-data`、`run-code`、`call-tool`、`send-message`、`network-egress`、`delegate`。
