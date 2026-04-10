from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.models import OrderItemModel, OrderModel


class OrderDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_with_items(self, order_id: int) -> OrderModel | None:
        stmt = select(OrderModel).where(OrderModel.id == order_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, customer_id: int) -> OrderModel:
        order = OrderModel(customer_id=customer_id)
        self.session.add(order)
        await self.session.flush()
        return order

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[OrderModel]:
        stmt = select(OrderModel).offset(skip).limit(limit).order_by(OrderModel.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


class OrderItemDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_order_and_product(
        self, order_id: int, product_id: int
    ) -> OrderItemModel | None:
        stmt = select(OrderItemModel).where(
            OrderItemModel.order_id == order_id, OrderItemModel.product_id == product_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self, order_id: int, product_id: int, quantity: int, price: float
    ) -> OrderItemModel:
        item = OrderItemModel(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_moment=price,
        )
        self.session.add(item)
        await self.session.flush()
        return item

    async def update_quantity(self, item_id: int, additional_quantity: int) -> None:
        stmt = (
            update(OrderItemModel)
            .where(OrderItemModel.id == item_id)
            .values(quantity=OrderItemModel.quantity + additional_quantity)
        )
        await self.session.execute(stmt)

    async def decrease_quantity(self, item_id: int, subtract_quantity: int) -> None:
        stmt = (
            update(OrderItemModel)
            .where(OrderItemModel.id == item_id)
            .values(quantity=OrderItemModel.quantity - subtract_quantity)
        )
        await self.session.execute(stmt)

    async def delete(self, item_id: int) -> None:
        stmt = delete(OrderItemModel).where(OrderItemModel.id == item_id)
        await self.session.execute(stmt)
