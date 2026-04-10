from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.products.models import ProductModel


class ProductDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_for_update(self, product_id: int) -> ProductModel | None:
        stmt = (
            select(ProductModel).where(ProductModel.id == product_id).with_for_update()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def decrease_stock(self, product_id: int, quantity: int) -> None:
        stmt = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(stock_quantity=ProductModel.stock_quantity - quantity)
        )
        await self.session.execute(stmt)

    async def increase_stock(self, product_id: int, quantity: int) -> None:
        stmt = (
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(stock_quantity=ProductModel.stock_quantity + quantity)
        )
        await self.session.execute(stmt)

    async def create(self, data: dict) -> ProductModel:
        product = ProductModel(**data)
        self.session.add(product)
        await self.session.flush()
        return product
