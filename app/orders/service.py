from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CustomerNotFoundError,
    InsufficientStockError,
    InvalidQuantityError,
    OrderItemNotFoundError,
    OrderNotFoundError,
    ProductNotFoundError,
)
from app.orders.dao import OrderDAO, OrderItemDAO
from app.orders.schemas import (
    AddItemRequest,
    OrderCreate,
    OrderItemResponse,
    OrderResponse,
    RemoveItemRequest,
)
from app.products.dao import ProductDAO


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_dao = OrderDAO(session)
        self.order_item_dao = OrderItemDAO(session)
        self.product_dao = ProductDAO(session)

    async def add_item_to_order(self, data: AddItemRequest) -> OrderItemResponse:
        order = await self.order_dao.get_with_items(data.order_id)
        if not order:
            raise OrderNotFoundError(data.order_id)

        product = await self.product_dao.get_for_update(data.product_id)
        if not product:
            raise ProductNotFoundError(data.product_id)

        if product.stock_quantity < data.quantity:
            raise InsufficientStockError(data.product_id, product.stock_quantity)

        existing_item = await self.order_item_dao.find_by_order_and_product(
            data.order_id, data.product_id
        )

        if existing_item:
            await self.order_item_dao.update_quantity(existing_item.id, data.quantity)
            await self.product_dao.decrease_stock(product.id, data.quantity)
            await self.session.commit()
            await self.session.refresh(existing_item)
            return OrderItemResponse(
                order_id=existing_item.order_id,
                product_id=existing_item.product_id,
                quantity=existing_item.quantity,
                price_at_moment=existing_item.price_at_moment,
            )
        else:
            new_item = await self.order_item_dao.create(
                order_id=data.order_id,
                product_id=data.product_id,
                quantity=data.quantity,
                price=product.price,
            )
            await self.product_dao.decrease_stock(product.id, data.quantity)
            await self.session.commit()
            await self.session.refresh(new_item)
            return OrderItemResponse(
                order_id=new_item.order_id,
                product_id=new_item.product_id,
                quantity=new_item.quantity,
                price_at_moment=new_item.price_at_moment,
            )

    async def remove_item_from_order(
        self, data: RemoveItemRequest
    ) -> OrderItemResponse | dict:
        order = await self.order_dao.get_with_items(data.order_id)
        if not order:
            raise OrderNotFoundError(data.order_id)

        order_item = await self.order_item_dao.find_by_order_and_product(
            data.order_id, data.product_id
        )
        if not order_item:
            raise OrderItemNotFoundError(data.order_id, data.product_id)

        if order_item.quantity < data.quantity:
            raise InvalidQuantityError(
                f"Невозможно удалить {data.quantity} товаров. В заказе только {order_item.quantity} товаров."
            )

        await self.product_dao.increase_stock(data.product_id, data.quantity)

        if order_item.quantity == data.quantity:
            await self.order_item_dao.delete(order_item.id)
            await self.session.commit()
            return {"message": "Все товары удалены"}
        else:
            await self.order_item_dao.decrease_quantity(order_item.id, data.quantity)
            await self.session.commit()
            await self.session.refresh(order_item)
            return OrderItemResponse(
                order_id=order_item.order_id,
                product_id=order_item.product_id,
                quantity=order_item.quantity,
                price_at_moment=order_item.price_at_moment,
            )

    async def create_order(self, data: OrderCreate) -> OrderResponse:
        from app.customers.dao import CustomerDAO

        cust_dao = CustomerDAO(self.session)
        customer = await cust_dao.get_by_id(data.customer_id)
        if not customer:
            raise CustomerNotFoundError(data.customer_id)

        order = await self.order_dao.create(data.customer_id)
        await self.session.commit()
        await self.session.refresh(order)

        return OrderResponse(
            id=order.id,
            customer_id=order.customer_id,
            created_at=order.created_at,
            items=[],
        )

    async def get_order(self, order_id: int) -> OrderResponse:
        order = await self.order_dao.get_with_items(order_id)
        if not order:
            raise OrderNotFoundError(order_id)

        items = []
        for item in order.items:
            items.append(
                OrderItemResponse(
                    order_id=item.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_moment=item.price_at_moment,
                )
            )
        return OrderResponse(
            id=order.id,
            customer_id=order.customer_id,
            created_at=order.created_at,
            items=items,
        )

    async def list_orders(self, skip: int = 0, limit: int = 100) -> list[OrderResponse]:
        orders = await self.order_dao.get_all(skip, limit)
        result = []
        for order in orders:
            items = [
                OrderItemResponse(
                    order_id=item.order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_moment=item.price_at_moment,
                )
                for item in order.items
            ]
            result.append(
                OrderResponse(
                    id=order.id,
                    customer_id=order.customer_id,
                    created_at=order.created_at,
                    items=items,
                )
            )
        return result
