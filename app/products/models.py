from sqlalchemy import Column, ForeignKey, Integer, Numeric, String

from app.core.database import Base


class ProductModel(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="SET NULL"))
