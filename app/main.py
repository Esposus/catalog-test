from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import create_test_entities
from app.core.database import health_live
from app.orders.routes import router as orders_router
from app.products.routes import router as products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_test_entities()
    yield


app = FastAPI(
    title="Сервис управления заказами",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(orders_router)
app.include_router(products_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/health/live")
async def live():
    return await health_live()
