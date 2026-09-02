# HTTP API 参考

基址：`http://127.0.0.1:8420`

## 健康与元信息

- `GET /healthz` → `{"status": "ok"}`
- `GET /version` → `{"version": "1.0.0"}`
- `GET /doctor` → `{"status", "passports", "audit_records", "chain_intact"}`

## 护照

- `GET /passports` — 列出所有护照
- `POST /passports` — 签发护照，body：`{"name", "owner", "capabilities", "provider", "model"}`
- `GET /passports/{agent_id}` — 查询单个护照
- `POST /passports/{agent_id}/revoke` — 吊销

## 审计

- `POST /audit` — 审计动作，body：`{"agent_id", "action", "context"}`
- `GET /audit` — 最近审计记录
- `GET /audit/verify` — 哈希链完整性 `{"intact": bool, "broken_index": int}`

## 溯源

- `POST /provenance` — 记录证明，body：`{"agent_id", "action", "inputs", "outputs", "tool", "duration_ms"}`
- `GET /provenance/{agent_id}` — 某智能体的溯源链

## 信道

- `POST /channels` — 记录通信边 `{"src", "dst", "channel", "authorized"}`
- `GET /channels/topology` — 当前拓扑

## 策略

- `POST /policy/evaluate` — 评估 `{"agent_id", "action", "context"}` → `{"allowed", "reason"}`
