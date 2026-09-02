# SDK 使用

## Python SDK

```python
from agentpassport_sdk import Client

c = Client("http://127.0.0.1:8420")
c.issue("scanner", "team")
c.audit("<agent_id>", "read")
```

安装：`pip install -e sdk/python` 或直接把 `sdk/python` 加入 `PYTHONPATH`。

## TypeScript SDK

```bash
cd sdk/typescript && npm install && npm run build
```

```typescript
import { Client } from "@agentpassport/sdk";
const c = new Client();
await c.health();
await c.listPassports();
```
