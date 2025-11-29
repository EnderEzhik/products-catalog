from fastapi import FastAPI, HTTPException
from schemas import ProductCreate, Product, ProductUpdate
from data_store import store
from typing import List


app = FastAPI()


# вспомогательнеая функция для получения товара по ID (если тогвара нет - возвращает статус 404)
def get_product_or_404(product_id: int) -> Product:
    product = store.products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


# ендпоинт для обработки GET-запроса к корневому элементу (базовая проверка работы приложения)
@app.get("/")
def root():
    return { "message": "Приложение работает" }


# енжпоинт для обработки POST-запроса на создание нового товара
@app.post("/product", response_model=Product)
def create_product(product_data: ProductCreate):
    product = Product(id = store.next_id(), **product_data.model_dump())
    store.products[product.id] = product
    return product


@app.get("/product", response_model=List[Product])
def get_product_list():
    return list(store.products.value())


# ендпоинт для обработки GET-запроса на получение товара по ID
@app.get("/product/{product_id}", response_model=Product)
def get_product(product_id: int):
    return get_product_or_404(product_id)


# ендпоинт для обработки PUT-запроса на полную замену данных о товаре по ID
@app.put("/product/{product_id}", response_model=Product)
def put_product(product_id: int, product_data: ProductUpdate):
    _ = get_product_or_404(product_id)
    updated = Product(id=product_id, **product_data.model_dump())
    store.products[product_id] = updated
    return updated


# ендпоинт для обработки PATCH-запроса на частичное обновление данных о товаре по ID
@app.patch("/product/{product_id}", response_model=Product)
def patch_product(product_id: int, product_data: ProductUpdate):
    current = get_product_or_404(product_id)
    updates = product_data.model_dump(exclude_unset=True)
    product_data_updated = current.model_copy(update=updates)
    store.products[product_id] = product_data_updated
    return product_data_updated


# ендпоинт для обработки DELETE-запроса на удаление данных о товаре по ID
@app.delete("/product/{product_id}", response_model=Product)
def delete_product(product_id):
    _ = get_product_or_404(product_id)
    del store.products[product_id]
    return { "message": "Товар удален" }
