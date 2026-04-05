# Gunakan Python 3.10 sesuai prasyarat [cite: 2]
FROM python:3.10-slim

# Set direktori kerja
WORKDIR /app

# Install dependencies sistem yang diperlukan untuk psycopg2 (driver postgres)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Salin dan install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode pipeline-service
COPY . .

# Port FastAPI sesuai instruksi
EXPOSE 8000

# Jalankan FastAPI menggunakan uvicorn
CMD ["python", "main.py"]