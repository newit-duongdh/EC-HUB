"""
Application Service for Product
Orchestrates domain operations and coordinates with repositories
"""
from decimal import Decimal
from typing import List
from uuid import UUID

from application.dtos.product_dto import (
    CreateProductDTO,
    ProductResponseDTO,
    UpdateProductDTO,
    UpdateStockDTO,
)
from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository


class ProductService:
    """
    Application service for product use cases
    Coordinates between domain entities and repositories
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Initialize service with product repository
        """
        self._repository = product_repository

    def create_product(self, dto: CreateProductDTO) -> ProductResponseDTO:
        """
        Create a new product
        """
        # Create domain entity using factory method
        product = Product.create(
            name=dto.name,
            description=dto.description,
            price=dto.price,
            stock_quantity=dto.stock_quantity
        )

        # Save through repository
        saved_product = self._repository.save(product)

        # Convert to response DTO
        return self._to_response_dto(saved_product)

    def get_product_by_id(self, product_id: UUID) -> ProductResponseDTO:
        """
        Get product by ID
        Raises exception if not found
        """
        product = self._repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        return self._to_response_dto(product)

    def get_all_products(self, skip: int = 0, limit: int = 100) -> List[ProductResponseDTO]:
        """
        Get all products with pagination
        """
        products = self._repository.get_all(skip=skip, limit=limit)
        return [self._to_response_dto(product) for product in products]

    def update_product(self, product_id: UUID, dto: UpdateProductDTO) -> ProductResponseDTO:
        """
        Update product information
        """
        # Get existing product
        product = self._repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        # Update fields using domain methods
        if dto.name is not None:
            product.update_name(dto.name)
        
        if dto.description is not None:
            product.update_description(dto.description)
        
        if dto.price is not None:
            product.update_price(dto.price)
        
        if dto.stock_quantity is not None:
            product.update_stock(dto.stock_quantity)

        # Save updated product
        saved_product = self._repository.save(product)
        return self._to_response_dto(saved_product)

    def increase_stock(self, product_id: UUID, dto: UpdateStockDTO) -> ProductResponseDTO:
        """
        Increase product stock
        """
        product = self._repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        # Use domain method to increase stock
        product.increase_stock(dto.quantity)

        # Save updated product
        saved_product = self._repository.save(product)
        return self._to_response_dto(saved_product)

    def reduce_stock(self, product_id: UUID, dto: UpdateStockDTO) -> ProductResponseDTO:
        """
        Reduce product stock
        """
        product = self._repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        # Use domain method to reduce stock (includes validation)
        product.reduce_stock(dto.quantity)

        # Save updated product
        saved_product = self._repository.save(product)
        return self._to_response_dto(saved_product)

    def delete_product(self, product_id: UUID) -> bool:
        """
        Delete a product
        """
        if not self._repository.exists(product_id):
            raise ValueError(f"Product with ID {product_id} not found")
        
        return self._repository.delete(product_id)

    def _to_response_dto(self, product: Product) -> ProductResponseDTO:
        """
        Convert domain entity to response DTO
        """
        return ProductResponseDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
