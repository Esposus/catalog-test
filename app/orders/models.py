from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class OrderModel(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("OrderItemModel", back_populates="order", lazy="selectin")


class OrderItemModel(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True)
    order_id = Column(
        Integer, ForeignKey("order.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_moment = Column(Numeric(10, 2), nullable=False)

    __table_args__ = (UniqueConstraint("order_id", "product_id"),)

    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel")
