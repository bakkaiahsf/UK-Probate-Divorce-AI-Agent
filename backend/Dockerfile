# backend/Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Set environment
ENV PYTHONUNBUFFERED=1

# Run FastAPI app
CMD ["uvicorn", "app.api.v1.api:app", "--host", "0.0.0.0", "--port", "8000"]
