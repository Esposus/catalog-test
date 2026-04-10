from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.categories.models import CategoryModel


class CategoryDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, category_id: int) -> CategoryModel | None:
        stmt = select(CategoryModel).where(CategoryModel.id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
