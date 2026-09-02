# 部署

## Docker Compose

```bash
docker compose up -d
```

## Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml -f k8s/secret.yaml
```

## Helm

```bash
helm install agentpassport ./helm/agentpassport
```

## 生产建议

1. 通过环境变量注入 `AGENTPASSPORT_PASSPORT__SECRET`（不要硬编码）
2. 数据目录 `data/` 挂载持久卷
3. 在网关层启用 TLS
4. 配置 Prometheus 抓取 `/metrics`
