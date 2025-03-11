from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    Text,
    Float,
    Boolean,
    ForeignKey,
    BigInteger,
    func,
)
from sqlalchemy.orm import relationship
from app.core.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    def __repr__(self):
        return f"<Product {self.name}>"