from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import ProductOut, ProductCreate, ProductUpdate
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import Product
from repositories import products_repository

router = APIRouter(prefix="/products", tags=["products"])


# вспомогательнеая функция для получения товара по ID (если тогвара нет - возвращает статус 404)
def get_product_or_404(db: Session, product_id: int) -> ProductOut:
    product = products_repository.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


# ендпоинт для обработки POST-запроса на создание нового товара
@router.post("/", response_model=ProductOut)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return products_repository.create_product(db, product_data)


# ендпоинт для обработки GET-запроса на получение списка всех товаров
@router.get("/", response_model=List[ProductOut])
def get_product_list(q: str | None = Query(default=None, description="Поиск по подстроке в названии продукта"),
                     in_stock: bool | None = Query(default=None, description="Поиск по наличию товара"),
                     min_price: float | None = Query(default=None, ge=0, description="Минимальная цена товара"),
                     max_price: float | None = Query(default=None, ge=0, description="Максимальная цена товара"),
                     db: Session = Depends(get_db)):
    return products_repository.get_product_list(db, q, in_stock, min_price, max_price)


# ендпоинт для обработки GET-запроса на получение товара по ID
@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_or_404(db, product_id)


# ендпоинт для обработки PUT-запроса на полную замену данных о товаре по ID
@router.put("/{product_id}", response_model=ProductOut)
def put_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = get_product_or_404(product_id)
    return products_repository.put_product(db, product, product_data)


# ендпоинт для обработки PATCH-запроса на частичное обновление данных о товаре по ID
@router.patch("/{product_id}", response_model=ProductOut)
def patch_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = get_product_or_404(product_id)
    return products_repository.patch_product(db, product, product_data)


# ендпоинт для обработки DELETE-запроса на удаление данных о товаре по ID
@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(product_id, db: Session = Depends(get_db)):
    product = get_product_or_404(product_id)
    products_repository.delete_product(db, product)
    return { "message": "Товар удален" }
