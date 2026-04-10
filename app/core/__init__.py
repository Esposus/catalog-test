"""
Для демонстрации работы создадим 1 продукт, 1 категорию и 1 пользователя
"""

from sqlalchemy import select

from app.categories.models import CategoryModel
from app.core.database import AsyncSessionLocal
from app.customers.models import CustomerModel
from app.products.models import ProductModel


async def create_test_entities():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(CustomerModel).limit(1))
        customer = result.scalar_one_or_none()
        if not customer:
            test_customer = CustomerModel(
                name="Тестовый клиент", address="г. Москва, ул. Тестовая, д. 1"
            )
            session.add(test_customer)
            await session.commit()
            await session.refresh(test_customer)
            print(f"Создан тестовый клиент с id={test_customer.id}")
        else:
            print("Клиенты уже существуют, тестовый клиент не создаётся.")

        result = await session.execute(select(CategoryModel).limit(1))
        category = result.scalar_one_or_none()
        if not category:
            root_category = CategoryModel(name="Бытовая техника", parent_id=None)
            session.add(root_category)
            await session.commit()
            await session.refresh(root_category)
            print(f"Создана корневая категория с id={root_category.id}")

        result = await session.execute(select(ProductModel).limit(1))
        product = result.scalar_one_or_none()
        if not product:
            cat_result = await session.execute(select(CategoryModel).limit(1))
            cat = cat_result.scalar_one()
            test_product = ProductModel(
                name="Ноутбук тестовый",
                stock_quantity=10,
                price=50000,
                category_id=cat.id,
            )
            session.add(test_product)
            await session.commit()
            await session.refresh(test_product)
            print(f"Создан тестовый товар с id={test_product.id}")
