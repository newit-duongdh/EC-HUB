"""
FastAPI Application Entry Point
Main application setup and routing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.api.controllers.product_controller import router as product_router
from infrastructure.database.config import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Product Management API",
    description="Product management system built with DDD and Clean Architecture",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(product_router, prefix="/api")


@app.get("/")
def root():
    """
    Root endpoint
    """
    return {
        "message": "Product Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}
