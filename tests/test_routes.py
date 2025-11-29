import asyncio
from http.client import responses

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import delete
from src.models import Product

from fastapi.testclient import TestClient
from src.main import app
from src.database import Base, get_session
from src.schemas import ProductOut


client = TestClient(app)

engine = create_async_engine("sqlite+aiosqlite:///:memory:", poolclass=StaticPool)

SessionMaker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_schema():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_schema())


async def override_get_session():
    async with SessionMaker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


def reset_and_seed():
    async def op():
        async with SessionMaker() as session:
            await session.execute(delete(Product))
            session.add_all([
                Product(name="Phone", description="good camera", price=50000, in_stock=True),
                Product(name="Headphone", description="good", price=12000, in_stock=True),
                Product(name="Notebook", description="game", price=90000, in_stock=True)
            ])
            await session.commit()
    asyncio.run(op())


def test_app_starts():
    response = client.get("/")
    assert response.status_code == 200


def test_product_shape():
    reset_and_seed()
    response = client.get("/products")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    expected_keys = ProductOut.model_fields.keys()
    assert data and expected_keys <= set(data[0].keys())
