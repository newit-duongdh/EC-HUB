"""
SQLAlchemy ORM Models
Database representation of domain entities
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, DateTime
from sqlalchemy.dialects.mysql import CHAR
from uuid import uuid4

from infrastructure.database.config import Base


class ProductModel(Base):
    """
    SQLAlchemy model for Product table
    Maps to domain Product entity
    """
    __tablename__ = "products"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def from_domain_entity(cls, product) -> "ProductModel":
        """
        Convert domain Product entity to database model
        """
        return cls(
            id=str(product.id),
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity,
            created_at=product.created_at,
            updated_at=product.updated_at
        )

    def to_domain_entity(self):
        """
        Convert database model to domain Product entity
        """
        from domain.entities.product import Product
        from uuid import UUID

        return Product(
            id=UUID(self.id),
            name=self.name,
            description=self.description,
            price=Decimal(str(self.price)),
            stock_quantity=self.stock_quantity,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
