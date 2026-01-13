"""
Data Transfer Objects for Product
Used for request/response between layers
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CreateProductDTO(BaseModel):
    """
    DTO for creating a new product
    """
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    price: Decimal = Field(..., gt=0, description="Product price")
    stock_quantity: int = Field(..., ge=0, description="Initial stock quantity")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()


class UpdateProductDTO(BaseModel):
    """
    DTO for updating product information
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Product name cannot be empty")
        return v.strip() if v else None


class UpdateStockDTO(BaseModel):
    """
    DTO for updating stock quantity
    """
    quantity: int = Field(..., gt=0, description="Stock quantity to add or subtract")


class ProductResponseDTO(BaseModel):
    """
    DTO for product response
    """
    id: UUID
    name: str
    description: Optional[str]
    price: Decimal
    stock_quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponseDTO(BaseModel):
    """
    DTO for paginated product list response
    """
    products: List[ProductResponseDTO]
    total: int
    skip: int
    limit: int
