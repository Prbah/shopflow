from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import models

from pydantic import ConfigDict

app = FastAPI(title="ShopFlow Product Service", version="1.0.0")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    description: str = Field(default="", max_length=500)

class Product(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "product-service"}


@app.get("/products", response_model=list[Product])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@app.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = models.Product(**payload.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    payload: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in payload.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product



@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return None
