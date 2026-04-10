from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.customers.models import CustomerModel


class CustomerDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, customer_id: int) -> CustomerModel | None:
        stmt = select(CustomerModel).where(CustomerModel.id == customer_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
