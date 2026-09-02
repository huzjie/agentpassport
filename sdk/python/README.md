# agentpassport Python SDK

标准库 `urllib` 实现的轻量客户端，零第三方依赖。

```python
from agentpassport_sdk import Client

c = Client("http://127.0.0.1:8420")
print(c.health())
p = c.issue("scanner", "security-team", capabilities=[
    {"name": "read-data", "actions": ["read", "search"]}
])
print(p["agent_id"])
```
