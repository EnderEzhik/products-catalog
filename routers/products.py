from fastapi import APIRouter, HTTPException, Query
from schemas import Product, ProductCreate, ProductUpdate
from data_store import store
from typing import List

router = APIRouter(prefix="/products", tags=["products"])


# вспомогательнеая функция для получения товара по ID (если тогвара нет - возвращает статус 404)
def get_product_or_404(product_id: int) -> Product:
    product = store.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


# ендпоинт для обработки POST-запроса на создание нового товара
@router.post("/", response_model=Product)
def create_product(product_data: ProductCreate):
    return store.create_product(product_data)


# ендпоинт для обработки GET-запроса на получение списка всех товаров
@router.get("/", response_model=List[Product])
def get_product_list(q: str | None = Query(default=None, description="Поиск по подстроке в названии продукта"),
                     in_stock: bool | None = Query(default=None, description="Поиск по наличию товара"),
                     min_price: float | None = Query(default=None, ge=0, description="Минимальная цена товара"),
                     max_price: float | None = Query(default=None, ge=0, description="Максимальная цена товара")):
    return store.get_product_list(q, in_stock, min_price, max_price)


# ендпоинт для обработки GET-запроса на получение товара по ID
@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    return get_product_or_404(product_id)


# ендпоинт для обработки PUT-запроса на полную замену данных о товаре по ID
@router.put("/{product_id}", response_model=Product)
def put_product(product_id: int, product_data: ProductUpdate):
    _ = get_product_or_404(product_id)
    return store.put_product(product_id, product_data)


# ендпоинт для обработки PATCH-запроса на частичное обновление данных о товаре по ID
@router.patch("/{product_id}", response_model=Product)
def patch_product(product_id: int, product_data: ProductUpdate):
    _ = get_product_or_404(product_id)
    return store.patch_product(product_id, product_data)


# ендпоинт для обработки DELETE-запроса на удаление данных о товаре по ID
@router.delete("/{product_id}", response_model=Product)
def delete_product(product_id):
    _ = get_product_or_404(product_id)
    store.delete_product(product_id)
    return { "message": "Товар удален" }
