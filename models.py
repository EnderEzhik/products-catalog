from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    in_stock = Column(Boolean, default=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product")
    status = Column(String, default="New", nullable=False)
    delivery_address = Column(String, nullable=False)
