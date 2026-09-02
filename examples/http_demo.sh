#!/usr/bin/env bash
# HTTP API 端到端演示（先启动 serve）
set -e
BASE=http://127.0.0.1:8420

echo "== 健康检查 =="
curl -s $BASE/healthz

echo "\n== 签发护照 =="
P=$(curl -s -X POST $BASE/passports -H "Content-Type: application/json" \
  -d '{"name":"scanner","owner":"team"}')
echo "$P"
AID=$(echo "$P" | python -c "import sys,json;print(json.load(sys.stdin)['agent_id'])")

echo "\n== 审计动作 =="
curl -s -X POST $BASE/audit -H "Content-Type: application/json" \
  -d "{\"agent_id\":\"$AID\",\"action\":\"read\"}"

echo "\n== 校验哈希链 =="
curl -s $BASE/audit/verify
echo
