"""
Domain Entity: Product
Contains business logic and validation rules
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Product:
    """
    Product Domain Entity
    Contains business logic for product operations
    """
    id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    stock_quantity: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        name: str,
        description: Optional[str],
        price: Decimal,
        stock_quantity: int,
        product_id: Optional[UUID] = None
    ) -> "Product":
        """
        Factory method to create a new Product
        Validates business rules during creation
        """
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty")
        
        if price <= 0:
            raise ValueError("Product price must be greater than zero")
        
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        
        now = datetime.utcnow()
        return cls(
            id=product_id or uuid4(),
            name=name.strip(),
            description=description.strip() if description else None,
            price=price,
            stock_quantity=stock_quantity,
            created_at=now,
            updated_at=now
        )

    def update_price(self, new_price: Decimal) -> None:
        """
        Update product price with validation
        """
        if new_price <= 0:
            raise ValueError("Product price must be greater than zero")
        
        self.price = new_price
        self.updated_at = datetime.utcnow()

    def update_stock(self, new_stock: int) -> None:
        """
        Update stock quantity with validation
        """
        if new_stock < 0:
            raise ValueError("Stock quantity cannot be negative")
        
        self.stock_quantity = new_stock
        self.updated_at = datetime.utcnow()

    def increase_stock(self, quantity: int) -> None:
        """
        Increase stock quantity
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        self.stock_quantity += quantity
        self.updated_at = datetime.utcnow()

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce stock quantity with validation
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        if self.stock_quantity < quantity:
            raise ValueError(f"Insufficient stock. Available: {self.stock_quantity}, Requested: {quantity}")
        
        self.stock_quantity -= quantity
        self.updated_at = datetime.utcnow()

    def is_in_stock(self, quantity: int = 1) -> bool:
        """
        Check if product has sufficient stock
        """
        return self.stock_quantity >= quantity

    def update_name(self, new_name: str) -> None:
        """
        Update product name with validation
        """
        if not new_name or not new_name.strip():
            raise ValueError("Product name cannot be empty")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()

    def update_description(self, new_description: Optional[str]) -> None:
        """
        Update product description
        """
        self.description = new_description.strip() if new_description else None
        self.updated_at = datetime.utcnow()
