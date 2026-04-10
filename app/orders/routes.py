from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.orders.schemas import (
    AddItemRequest,
    OrderCreate,
    OrderItemResponse,
    OrderResponse,
    RemoveItemRequest,
)
from app.orders.service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


# Создание заказа
@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate, session: AsyncSession = Depends(get_session)
):
    service = OrderService(session)
    return await service.create_order(order_data)


# Получение списка заказов
@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
):
    service = OrderService(session)
    return await service.list_orders(skip, limit)


# Получение конкретного заказа
@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, session: AsyncSession = Depends(get_session)):
    service = OrderService(session)
    return await service.get_order(order_id)


# Добавление товара в заказ
@router.post("/add-item", response_model=OrderItemResponse)
async def add_item_to_order(
    request: AddItemRequest, session: AsyncSession = Depends(get_session)
):
    service = OrderService(session)
    return await service.add_item_to_order(request)


# Удаление товара из заказа
@router.post("/remove-item")
async def remove_item_from_order(
    request: RemoveItemRequest, session: AsyncSession = Depends(get_session)
):
    service = OrderService(session)
    return await service.remove_item_from_order(request)
