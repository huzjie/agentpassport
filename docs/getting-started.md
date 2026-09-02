# 快速上手

## 环境要求

- Python 3.9+（核心零第三方依赖，无需 pip install）

## 三步跑通

```bash
# 1. 复制配置
cp config.example.json config.json

# 2. 自检
python -m agentpassport doctor
# → {"status": "ok", "version": "1.0.0", "passports": 0, ...}

# 3. 启动控制面
python -m agentpassport serve
```

浏览器打开 `web/index.html` 或访问 `http://127.0.0.1:8420/healthz`。

## 签发并审计

```bash
python -m agentpassport issue --name scanner --owner security-team
# → {"agent_id": "agt-...", ...}

python -m agentpassport audit <agent_id> read
# → {"verdict": "pass", ...}

python -m agentpassport audit <agent_id> delegate
# → {"verdict": "fail", "reason": "..."}
```

## Docker

```bash
docker build -t agentpassport .
docker run -p 8420:8420 -v $PWD/data:/app/data agentpassport
```
