"""
Product Repository Implementation
Implements ProductRepository interface from domain layer
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository
from infrastructure.database.models import ProductModel


class MySQLProductRepository(ProductRepository):
    """
    MySQL implementation of ProductRepository
    Handles database operations for Product entity
    """

    def __init__(self, session: Session):
        """
        Initialize repository with database session
        """
        self._session = session

    def save(self, product: Product) -> Product:
        """
        Save or update a product
        """
        # Check if product exists
        product_model = self._session.query(ProductModel).filter(
            ProductModel.id == str(product.id)
        ).first()

        if product_model:
            # Update existing product
            product_model.name = product.name
            product_model.description = product.description
            product_model.price = product.price
            product_model.stock_quantity = product.stock_quantity
            product_model.updated_at = product.updated_at
        else:
            # Create new product
            product_model = ProductModel.from_domain_entity(product)
            self._session.add(product_model)

        self._session.commit()
        self._session.refresh(product_model)

        # Return domain entity
        return product_model.to_domain_entity()

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        Get product by ID
        """
        product_model = self._session.query(ProductModel).filter(
            ProductModel.id == str(product_id)
        ).first()

        if not product_model:
            return None

        return product_model.to_domain_entity()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get all products with pagination
        """
        product_models = self._session.query(ProductModel).offset(skip).limit(limit).all()
        return [model.to_domain_entity() for model in product_models]

    def delete(self, product_id: UUID) -> bool:
        """
        Delete a product by ID
        """
        product_model = self._session.query(ProductModel).filter(
            ProductModel.id == str(product_id)
        ).first()

        if not product_model:
            return False

        self._session.delete(product_model)
        self._session.commit()
        return True

    def exists(self, product_id: UUID) -> bool:
        """
        Check if product exists
        """
        count = self._session.query(ProductModel).filter(
            ProductModel.id == str(product_id)
        ).count()
        return count > 0
