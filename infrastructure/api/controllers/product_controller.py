"""
Product Controller
Handles HTTP requests and responses for product endpoints
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from application.dtos.product_dto import (
    CreateProductDTO,
    ProductResponseDTO,
    UpdateProductDTO,
    UpdateStockDTO,
)
from application.services.product_service import ProductService
from infrastructure.database.config import get_db
from infrastructure.repositories.product_repository_impl import MySQLProductRepository

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """
    Dependency injection for ProductService
    Creates repository and service instances
    """
    repository = MySQLProductRepository(db)
    return ProductService(repository)


@router.post("", response_model=ProductResponseDTO, status_code=status.HTTP_201_CREATED)
def create_product(
    dto: CreateProductDTO,
    service: ProductService = Depends(get_product_service)
):
    """
    Create a new product
    """
    try:
        return service.create_product(dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{product_id}", response_model=ProductResponseDTO)
def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service)
):
    """
    Get product by ID
    """
    try:
        return service.get_product_by_id(product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("", response_model=List[ProductResponseDTO])
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_product_service)
):
    """
    Get all products with pagination
    """
    return service.get_all_products(skip=skip, limit=limit)


@router.put("/{product_id}", response_model=ProductResponseDTO)
def update_product(
    product_id: UUID,
    dto: UpdateProductDTO,
    service: ProductService = Depends(get_product_service)
):
    """
    Update product information
    """
    try:
        return service.update_product(product_id, dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{product_id}/stock/increase", response_model=ProductResponseDTO)
def increase_stock(
    product_id: UUID,
    dto: UpdateStockDTO,
    service: ProductService = Depends(get_product_service)
):
    """
    Increase product stock
    """
    try:
        return service.increase_stock(product_id, dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{product_id}/stock/reduce", response_model=ProductResponseDTO)
def reduce_stock(
    product_id: UUID,
    dto: UpdateStockDTO,
    service: ProductService = Depends(get_product_service)
):
    """
    Reduce product stock
    """
    try:
        return service.reduce_stock(product_id, dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service)
):
    """
    Delete a product
    """
    try:
        service.delete_product(product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
