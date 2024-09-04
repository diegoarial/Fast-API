from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

# Simulando um banco de dados simples
fake_products_db = []

router = APIRouter()

@router.get("/", response_model=List[Product])
def read_products():
    return fake_products_db

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int):
    product = next((product for product in fake_products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    product_dict = product.dict()
    product_dict['id'] = len(fake_products_db) + 1
    fake_products_db.append(product_dict)
    return product_dict

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    index = next((index for index, p in enumerate(fake_products_db) if p["id"] == product_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Product not found")
    fake_products_db[index] = product.dict()
    return product.dict()

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    global fake_products_db
    product_index = next((index for index, product in enumerate(fake_products_db) if product["id"] == product_id), None)
    if product_index is None:
        raise HTTPException(status_code=404, detail="Product not found")
    del fake_products_db[product_index]
    return None
