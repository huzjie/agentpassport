# LLM Provider 适配器

用于护照能力评估、行为分析等需模型辅助的场景（核心治理逻辑不依赖模型）。

## 支持的 Provider

| Provider | 类型 | 默认 base_url |
| --- | --- | --- |
| mock | 离线确定性 | — |
| openai | OpenAI 兼容 | `https://api.openai.com/v1` |
| deepseek | OpenAI 兼容 | `https://api.deepseek.com/v1` |
| qwen | OpenAI 兼容 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| kimi | OpenAI 兼容 | `https://api.moonshot.cn/v1` |
| glm | OpenAI 兼容 | `https://open.bigmodel.cn/api/paas/v4` |
| ollama | OpenAI 兼容 | `http://localhost:11434/v1` |
| vllm | OpenAI 兼容 | `http://localhost:8000/v1` |
| anthropic | Messages API | `https://api.anthropic.com` |

## 使用

```python
from agentpassport.providers import get_provider

p = get_provider("deepseek", api_key="sk-...")
r = p.complete("你好")
print(r.text)
```
