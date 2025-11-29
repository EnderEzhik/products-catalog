from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate, ProductUpdate


def create_product(db: Session, product_data: ProductCreate) -> Product:
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    return new_product


def get_product_list(db: Session,
                     q: str = None,
                     in_stock: bool = None,
                     min_price: float = None,
                     max_price: float = None) -> list[Product]:
    result = db.query(Product)

    if in_stock is not None:
        result = result.filter(Product.in_stock == in_stock)

    if min_price is not None:
        result = result.filter(Product.price >= min_price)

    if max_price is not None:
        result = result.filter(Product.price <= max_price)

    result = result.all()

    if q is not None:
        q_lower = q.lower()
        result = [p for p in result if q_lower in p.name.lower()]

    return result


def put_product(db: Session, product: Product, product_data: ProductCreate) -> Product:
    for field, value in product_data.model_dump():
        setattr(product, field, value)
    db.commit()
    return product


def patch_product(db: Session, product: Product, product_data: ProductUpdate) -> Product:
    update = product_data.model_dump(exclude_unset=True)
    for field, value in update.items():
        setattr(product, field, value)
    db.commit()
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()
    return
