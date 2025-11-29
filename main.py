from fastapi import FastAPI
from routers import products


app = FastAPI()


# ендпоинт для обработки GET-запроса к корневому элементу (базовая проверка работы приложения)
@app.get("/")
def root():
    return { "message": "Приложение работает" }


app.include_router(products.router)
