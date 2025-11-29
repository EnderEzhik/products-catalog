from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Product
from schemas import ProductCreate, ProductUpdate


async def create_product(session: AsyncSession, product_data: ProductCreate) -> Product:
    new_product = Product(**product_data.model_dump())
    session.add(new_product)
    await session.commit()
    return new_product


async def get_product_list(session: AsyncSession,
                     q: str = None,
                     in_stock: bool = None,
                     min_price: float = None,
                     max_price: float = None) -> list[Product]:
    query = select(Product)

    if in_stock is not None:
        query = query.filter(Product.in_stock == in_stock)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    result = await session.execute(query)
    products = result.scalars().all()

    if q is not None:
        q_lower = q.lower()
        result = [p for p in result if q_lower in p.name.lower()]

    return products


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    result = await session.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()


async def put_product(session: AsyncSession, product: Product, product_data: ProductCreate) -> Product:
    for field, value in product_data.model_dump():
        setattr(product, field, value)
    await session.commit()
    return product


async def patch_product(session: AsyncSession, product: Product, product_data: ProductUpdate) -> Product:
    update = product_data.model_dump(exclude_unset=True)
    for field, value in update.items():
        setattr(product, field, value)
    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    await session.delete(product)
    await session.commit()
    return
