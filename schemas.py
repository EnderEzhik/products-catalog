from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Имя товара длиной от 1 до 50 символов")
    description: str | None = None
    price: float = Field(gt=0)
    in_stock: bool = True


class Product(ProductCreate):
    id: int


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50, description="Имя товара длиной от 1 до 50 символов")
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    in_stock: bool | None = None
