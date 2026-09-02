FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    AGENTPASSPORT_SERVER__HOST=0.0.0.0 \
    AGENTPASSPORT_SERVER__PORT=8420

WORKDIR /app

COPY pyproject.toml ./
COPY agentpassport/ ./agentpassport/

RUN mkdir -p /app/data

EXPOSE 8420

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8420/healthz')" || exit 1

ENTRYPOINT ["python", "-m", "agentpassport", "serve"]
