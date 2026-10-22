from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="ShopFlow Product Service", version="1.0.0")


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    description: str = Field(default="", max_length=500)


class Product(ProductCreate):
    id: int


products: dict[int, Product] = {
    1: Product(
        id=1,
        name="Mechanical Keyboard",
        price=2499.0,
        description="Wired mechanical keyboard",
    ),
    2: Product(
        id=2,
        name="Wireless Mouse",
        price=999.0,
        description="Wireless mouse",
    ),
}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "product-service"}


@app.get("/products", response_model=list[Product])
def list_products():
    return list(products.values())


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = products.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=Product, status_code=201)
def create_product(payload: ProductCreate):
    new_id = max(products.keys(), default=0) + 1
    product = Product(id=new_id, **payload.model_dump())
    products[new_id] = product
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, payload: ProductCreate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = Product(id=product_id, **payload.model_dump())
    products[product_id] = product
    return product


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return None
