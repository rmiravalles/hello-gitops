FROM python:3.12-slim

WORKDIR /app

# Upgrade pip to >=25.3 to remediate CVE-2025-8869
RUN pip install --no-cache-dir --upgrade "pip>=25.3"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade jaraco.context wheel

COPY main.py index.html index.dev.html index.prod.html ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]