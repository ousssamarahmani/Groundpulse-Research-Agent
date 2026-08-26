FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/agent \
    PORT=8080

WORKDIR /app

COPY agent/requirements.txt /app/agent/requirements.txt

RUN pip install --no-cache-dir --disable-pip-version-check \
    -r /app/agent/requirements.txt

COPY agent/groundpulse_agent /app/agent/groundpulse_agent
COPY evals /app/evals

WORKDIR /app/agent

CMD ["uvicorn", "groundpulse_agent.api:app", "--host", "0.0.0.0", "--port", "8080"]
