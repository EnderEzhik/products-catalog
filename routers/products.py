from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import ProductOut, ProductCreate, ProductUpdate
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from repositories import products_repository


router = APIRouter(prefix="/products", tags=["products"])


# вспомогательнеая функция для получения товара по ID (если тогвара нет - возвращает статус 404)
async def get_product_or_404(session: AsyncSession, product_id: int) -> ProductOut:
    product = await products_repository.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


# ендпоинт для обработки POST-запроса на создание нового товара
@router.post("/", response_model=ProductOut)
async def create_product(product_data: ProductCreate, session: AsyncSession = Depends(get_session)):
    return await products_repository.create_product(session, product_data)


# ендпоинт для обработки GET-запроса на получение списка всех товаров
@router.get("/", response_model=List[ProductOut])
async def get_product_list(q: str | None = Query(default=None, description="Поиск по подстроке в названии продукта"),
                     in_stock: bool | None = Query(default=None, description="Поиск по наличию товара"),
                     min_price: float | None = Query(default=None, ge=0, description="Минимальная цена товара"),
                     max_price: float | None = Query(default=None, ge=0, description="Максимальная цена товара"),
                     session: AsyncSession = Depends(get_session)):
    return await products_repository.get_product_list(session, q, in_stock, min_price, max_price)


# ендпоинт для обработки GET-запроса на получение товара по ID
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    return await get_product_or_404(session, product_id)


# ендпоинт для обработки PUT-запроса на полную замену данных о товаре по ID
@router.put("/{product_id}", response_model=ProductOut)
async def put_product(product_id: int, product_data: ProductUpdate, session: AsyncSession = Depends(get_session)):
    product = await get_product_or_404(product_id)
    return await products_repository.put_product(session, product, product_data)


# ендпоинт для обработки PATCH-запроса на частичное обновление данных о товаре по ID
@router.patch("/{product_id}", response_model=ProductOut)
async def patch_product(product_id: int, product_data: ProductUpdate, session: AsyncSession = Depends(get_session)):
    product = await get_product_or_404(product_id)
    return await products_repository.patch_product(session, product, product_data)


# ендпоинт для обработки DELETE-запроса на удаление данных о товаре по ID
@router.delete("/{product_id}", response_model=ProductOut)
async def delete_product(product_id, session: AsyncSession = Depends(get_session)):
    product = await get_product_or_404(product_id)
    await products_repository.delete_product(session, product)
    return { "message": "Товар удален" }
