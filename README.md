# Backend Developer Technical Assessment - Data Pipeline

This project is a technical assessment for the Backend Developer position at Acumen Strategy. It demonstrates a data pipeline architecture consisting of a Mock Server (Flask), a Pipeline Service (FastAPI), and a PostgreSQL database, all orchestrated using Docker.

## System Architecture

The system consists of three main components:
1. **Mock Server (Flask):** Serves customer data from a JSON file with pagination support.
2. **Pipeline Service (FastAPI):** Ingests data from the Mock Server using `dlt` (Data Load Tool) and stores it in PostgreSQL.
3. **Database (PostgreSQL):** Persistent storage for the ingested customer records.

## Key Features

- **Automated Ingestion:** Handles auto-pagination to ensure all records are fetched from the source.
- **Idempotent Loads (Upsert):** Uses `dlt` with `merge` write disposition to prevent duplicate records based on `customer_id`.
- **Database Schema Integrity:** Implemented using SQLAlchemy models for structured data storage.
- **Full Dockerization:** Easily deployable using a single Docker Compose command.

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Getting Started

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <project-folder-name>
```
### 2. Run the Services
Execute the following command to build and start all containers:

```bash
docker-compose up -d --build
Wait for about 10-15 seconds to ensure PostgreSQL is healthy and ready.
```

3. Verify Services
Check if all containers are running:

```bash
docker ps
You should see 3 running containers: mock-server, pipeline-service, and postgres.
```

## Testing the API
Phase 1: Mock Server Check
Fetch the raw data from the Flask Mock Server:

```bash
curl "http://localhost:5000/api/customers?page=1&limit=5"
```
Phase 2: Trigger Data Ingestion
Run the pipeline to move data from Flask to PostgreSQL:

```bash
curl -X POST http://localhost:8000/api/ingest
Response: {"status": "success", "records_processed": 20}
```

Phase 3: Verify Data in PostgreSQL
Retrieve the ingested data via the Pipeline Service (FastAPI):

```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
```
## Project Structure

```Plaintext
.
├── mock-server/
│   ├── app.py              # Flask Application
│   ├── Dockerfile          # Mock Server Docker Config
│   ├── requirements.txt    # Flask Dependencies
│   └── data/
│       └── customers.json  # Source Data
├── pipeline-service/
│   ├── main.py             # FastAPI Entry Point
│   ├── database.py         # SQLAlchemy Connection
│   ├── Dockerfile          # Pipeline Docker Config
│   ├── requirements.txt    # FastAPI & DLT Dependencies
│   ├── models/
│   │   └── customer.py     # SQLAlchemy Schema
│   └── services/
│       └── ingestion.py    # DLT Logic & Auto-pagination
└── docker-compose.yml      # Orchestration File
```
## Tech Stack
Languages: Python 3.10

Frameworks: FastAPI, Flask

Libraries: SQLAlchemy, DLT (Data Load Tool), Requests

Database: PostgreSQL 15

DevOps: Docker, Docker Compose