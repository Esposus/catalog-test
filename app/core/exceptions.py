# app/core/exceptions.py
from fastapi import HTTPException, status


class OrderNotFoundError(HTTPException):
    """Исключение, возникающее, когда заказ с указанным ID не найден."""

    def __init__(self, order_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с id {order_id} не найден",
        )


class ProductNotFoundError(HTTPException):
    """Исключение, возникающее, когда товар с указанным ID не найден."""

    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Товар с id {product_id} не найден",
        )


class InsufficientStockError(HTTPException):
    """Исключение, возникающее при недостаточном количестве товара на складе."""

    def __init__(self, product_id: int, available: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недостаточно товара с id {product_id}. Доступно: {available}",
        )


class CategoryNotFoundError(HTTPException):
    """Исключение, возникающее, когда категория с указанным ID не найдена."""

    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с id {category_id} не найдена",
        )


class OrderItemNotFoundError(HTTPException):
    """Исключение, возникающее, когда позиция заказа не найдена."""

    def __init__(self, order_id: int, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Позиция с товаром {product_id} не найдена в заказе {order_id}",
        )


class InvalidQuantityError(HTTPException):
    """Исключение, возникающее при некорректном количестве товара."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class CustomerNotFoundError(HTTPException):
    """Исключение, возникающее, когда клиент с указанным ID не найден."""

    def __init__(self, customer_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Клиент с id {customer_id} не найден",
        )
