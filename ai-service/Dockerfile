FROM python:3.10-slim

WORKDIR /app

# Install dependencies first — Docker caches this layer
# so rebuilds are fast when only your code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]