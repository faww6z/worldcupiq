FROM python:3.12-slim

WORKDIR /app/backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY data/ /app/data/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
