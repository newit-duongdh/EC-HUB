"""
Repository Interface for Product
Defines contract for product data access
Domain layer only knows about the interface, not the implementation
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.product import Product


class ProductRepository(ABC):
    """
    Repository interface for Product entity
    Implementation will be in Infrastructure layer
    """
    
    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Save or update a product
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        Get product by ID
        Returns None if not found
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get all products with pagination
        """
        pass

    @abstractmethod
    def delete(self, product_id: UUID) -> bool:
        """
        Delete a product by ID
        Returns True if deleted, False if not found
        """
        pass

    @abstractmethod
    def exists(self, product_id: UUID) -> bool:
        """
        Check if product exists
        """
        pass
