# 信道监控（Channel Monitor）

## 拓扑策略

`TopologyPolicy` 约束智能体间通信拓扑：

- 允许：`hub`（中心）、`chain`（链式）、`broadcast`（广播）、`tree`、`star`
- 禁止：点对点全网 `mesh`

## 未授权信道

`ChannelMonitor.record()` 记录通信边，`authorized=False` 时抛 `UnauthorizedChannelError`。

## 异常检测

`AnomalyDetector` 按时间窗统计频率，识别异常高频通信（对标「7 万条私建频道消息」）。
