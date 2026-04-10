# app/products/routes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.products.schemas import ProductCreate, ProductResponse
from app.products.service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate, session: AsyncSession = Depends(get_session)
):
    service = ProductService(session)
    return await service.create_product(product_data)
