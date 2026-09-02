# 全链路溯源（Provenance）

## 证明链

每次动作生成一条 `Attestation`，通过 `parent_hash` 串联成链：

```
att1 ← parent_hash ← att2 ← parent_hash ← att3
```

`parent_hash = sha256(prev_hash + record_id + inputs_hash + outputs_hash)`，
任何一条记录的插入、删除、重排都会破坏链完整性。

## 防伪造（Tamper Detection）

`TamperDetector` 双重校验：

1. **单条校验**：重算记录内容哈希，与存储哈希比对
2. **整链校验**：遍历账本，校验 `prev_hash` 连续性

直击「约 7% 执行记录被伪造」的场景——`scan()` 返回所有被篡改记录的下标。

## 重放防护

`ReplayGuard` 维护 nonce 集合（带时间窗自动清理），同一证明被重复提交即判定为重放。
