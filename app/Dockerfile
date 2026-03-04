FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade jaraco.context wheel

COPY main.py index.html index.dev.html index.prod.html ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]