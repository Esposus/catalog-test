from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class CustomerModel(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(Text, nullable=False)
