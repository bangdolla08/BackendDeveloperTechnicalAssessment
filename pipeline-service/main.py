from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import database, models.customer
from services.ingestion import run_ingestion

# Inisialisasi FastAPI
app = FastAPI(title="Data Ingestion Pipeline")

# Membuat tabel di database saat aplikasi dijalankan
models.customer.Base.metadata.create_all(bind=database.engine)


# Dependency untuk mendapatkan session database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/ingest")
def ingest_data():
    """
    Endpoint untuk menarik data dari Flask dan menyimpannya ke PostgreSQL.
    """
    try:
        count = run_ingestion()
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers")
def read_customers(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    """
    Mengambil data pelanggan dari PostgreSQL dengan pagination.
    """
    skip = (page - 1) * limit
    customers = db.query(models.customer.Customer).offset(skip).limit(limit).all()
    total = db.query(models.customer.Customer).count()

    return {
        "data": customers,
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/api/customers/{id}")
def read_customer(id: str, db: Session = Depends(get_db)):
    """
    Mengambil satu pelanggan berdasarkan ID dari database.
    """
    customer = db.query(models.customer.Customer).filter(models.customer.Customer.customer_id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)