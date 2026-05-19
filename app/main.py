from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Product Manager API",
    description="Mini API para gestionar productos",
    version="1.0.0"
)

class ProductCreate(BaseModel):
    name: str
    description: str | None = None

class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    available: bool = False

products: list[Product] = []
next_id = 1

@app.get("/")
def home():
    return {
        "message": "Bienvenido a Product Manager API",
        "docs": "/docs"
    }

@app.get("/products")
def list_products():
    return products

@app.post("/products")
def create_product(product_data: ProductCreate):
    global next_id

    new_product = Product(
        id=next_id,
        name=product_data.name,
        description=product_data.description,
        available=False
    )

    products.append(new_product)
    next_id += 1

    return {
        "message": "Producto creado correctamente",
        "product": new_product
    }

@app.put("/products/{product_id}/available")
def available_product(product_id: int):
    for product in products:
        if product.id == product_id:
            product.available = True

            return {
                "message": "Producto disponible",
                "product": product
            }

    raise HTTPException(status_code=404, detail="Producto no encontrado")