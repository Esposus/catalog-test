from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CategoryNotFoundError
from app.products.dao import ProductDAO
from app.products.schemas import ProductCreate, ProductResponse


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_dao = ProductDAO(session)

    async def create_product(self, data: ProductCreate) -> ProductResponse:
        if data.category_id:
            from app.categories.dao import CategoryDAO

            cat_dao = CategoryDAO(self.session)
            category = await cat_dao.get_by_id(data.category_id)
            if not category:
                raise CategoryNotFoundError(data.category_id)

        product_dict = data.model_dump()
        product = await self.product_dao.create(product_dict)
        await self.session.commit()
        await self.session.refresh(product)
        return ProductResponse.model_validate(product)
