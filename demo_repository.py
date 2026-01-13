"""
Demo Script: Repository Pattern trong hành động
Minh họa cách Repository đóng vai trò cầu nối giữa Domain và Data Source
"""
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session

# Import Domain Layer
from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository

# Import Infrastructure Layer
from infrastructure.database.config import get_db, engine, Base
from infrastructure.repositories.product_repository_impl import MySQLProductRepository
from infrastructure.database.models import ProductModel

# Import Application Layer
from application.services.product_service import ProductService
from application.dtos.product_dto import CreateProductDTO, UpdateStockDTO


def demo_repository_flow():
    """
    Demo luồng hoạt động của Repository Pattern
    """
    print("=" * 80)
    print("DEMO: Repository Pattern - Cầu Nối Giữa Domain và Data Source")
    print("=" * 80)
    print()
    
    # Tạo database tables nếu chưa có
    Base.metadata.create_all(bind=engine)
    
    # Lấy database session
    db: Session = next(get_db())
    
    print("📦 BƯỚC 1: Tạo Repository Implementation")
    print("-" * 80)
    print("Repository được tạo với database session từ Infrastructure layer")
    repository: ProductRepository = MySQLProductRepository(db)
    print(f"✅ Repository type: {type(repository).__name__}")
    print(f"✅ Repository implements: {ProductRepository.__name__}")
    print()
    
    print("🏗️  BƯỚC 2: Tạo Domain Entity (từ Domain Layer)")
    print("-" * 80)
    print("Domain Entity được tạo với business logic và validation")
    product = Product.create(
        name="Laptop Dell XPS 15",
        description="High-performance laptop for developers",
        price=Decimal("2500.00"),
        stock_quantity=10
    )
    print(f"✅ Product Entity created:")
    print(f"   - ID: {product.id}")
    print(f"   - Name: {product.name}")
    print(f"   - Price: ${product.price}")
    print(f"   - Stock: {product.stock_quantity}")
    print()
    
    print("💾 BƯỚC 3: Repository Lưu Domain Entity vào Database")
    print("-" * 80)
    print("Repository chuyển đổi Domain Entity → Database Model → SQL → Database")
    saved_product = repository.save(product)
    print(f"✅ Product saved to database:")
    print(f"   - ID: {saved_product.id}")
    print(f"   - Created at: {saved_product.created_at}")
    print()
    
    print("🔍 BƯỚC 4: Repository Lấy Dữ Liệu từ Database")
    print("-" * 80)
    print("Repository query database → Database Model → Domain Entity")
    retrieved_product = repository.get_by_id(saved_product.id)
    print(f"✅ Product retrieved from database:")
    print(f"   - ID: {retrieved_product.id}")
    print(f"   - Name: {retrieved_product.name}")
    print(f"   - Price: ${retrieved_product.price}")
    print(f"   - Stock: {retrieved_product.stock_quantity}")
    print()
    
    print("🔄 BƯỚC 5: Repository Chuyển Đổi Giữa Domain và Database")
    print("-" * 80)
    print("Minh họa quá trình chuyển đổi:")
    
    # Lấy model từ database
    product_model = db.query(ProductModel).filter(
        ProductModel.id == str(saved_product.id)
    ).first()
    
    print(f"📊 Database Model (ProductModel):")
    print(f"   - Type: {type(product_model).__name__}")
    print(f"   - Table: {product_model.__tablename__}")
    print(f"   - ID (string): {product_model.id}")
    print(f"   - Name: {product_model.name}")
    print()
    
    # Chuyển sang Domain Entity
    domain_entity = product_model.to_domain_entity()
    print(f"🏛️  Domain Entity (Product):")
    print(f"   - Type: {type(domain_entity).__name__}")
    print(f"   - ID (UUID): {domain_entity.id}")
    print(f"   - Name: {domain_entity.name}")
    print(f"   - Has business methods: {hasattr(domain_entity, 'increase_stock')}")
    print()
    
    print("📈 BƯỚC 6: Sử Dụng Business Logic từ Domain Entity")
    print("-" * 80)
    print("Domain Entity có business logic, không phụ thuộc database")
    domain_entity.increase_stock(5)
    print(f"✅ Stock increased by 5")
    print(f"   - New stock: {domain_entity.stock_quantity}")
    
    # Lưu lại sau khi thay đổi
    updated_product = repository.save(domain_entity)
    print(f"✅ Updated product saved:")
    print(f"   - Stock: {updated_product.stock_quantity}")
    print()
    
    print("🎯 BƯỚC 7: Sử Dụng Repository Qua Application Service")
    print("-" * 80)
    print("Application Service sử dụng Repository interface, không biết implementation")
    service = ProductService(repository)
    
    # Tạo product mới qua service
    create_dto = CreateProductDTO(
        name="MacBook Pro M3",
        description="Apple's latest laptop",
        price=Decimal("3000.00"),
        stock_quantity=5
    )
    new_product = service.create_product(create_dto)
    print(f"✅ Product created via Service:")
    print(f"   - ID: {new_product.id}")
    print(f"   - Name: {new_product.name}")
    print(f"   - Price: ${new_product.price}")
    print()
    
    # Tăng stock qua service
    stock_dto = UpdateStockDTO(quantity=3)
    updated = service.increase_stock(new_product.id, stock_dto)
    print(f"✅ Stock increased via Service:")
    print(f"   - New stock: {updated.stock_quantity}")
    print()
    
    print("📋 BƯỚC 8: Lấy Tất Cả Products")
    print("-" * 80)
    all_products = repository.get_all()
    print(f"✅ Total products in database: {len(all_products)}")
    for idx, p in enumerate(all_products, 1):
        print(f"   {idx}. {p.name} - ${p.price} (Stock: {p.stock_quantity})")
    print()
    
    print("🗑️  BƯỚC 9: Xóa Product")
    print("-" * 80)
    deleted = repository.delete(new_product.id)
    print(f"✅ Product deleted: {deleted}")
    print()
    
    print("=" * 80)
    print("✅ DEMO HOÀN TẤT!")
    print("=" * 80)
    print()
    print("📝 TÓM TẮT:")
    print("   1. Domain Layer định nghĩa Repository Interface (contract)")
    print("   2. Infrastructure Layer implement interface với MySQL")
    print("   3. Repository chuyển đổi giữa Domain Entity ↔ Database Model")
    print("   4. Application Service sử dụng Repository interface")
    print("   5. Domain không biết về database, Database không biết về business logic")
    print()
    
    # Cleanup
    db.close()


def demo_repository_isolation():
    """
    Demo tính độc lập của Repository - Domain không biết về database
    """
    print("=" * 80)
    print("DEMO: Repository Isolation - Domain Không Phụ Thuộc Database")
    print("=" * 80)
    print()
    
    print("🏛️  Domain Layer chỉ biết về:")
    print("   - Product Entity (business logic)")
    print("   - ProductRepository Interface (contract)")
    print()
    
    print("❌ Domain Layer KHÔNG biết về:")
    print("   - SQLAlchemy")
    print("   - MySQL/PostgreSQL")
    print("   - Database tables")
    print("   - SQL queries")
    print()
    
    print("🔌 Infrastructure Layer biết về:")
    print("   - MySQLProductRepository (implementation)")
    print("   - ProductModel (SQLAlchemy ORM)")
    print("   - Database connection")
    print()
    
    print("✅ Điều này cho phép:")
    print("   - Thay đổi database mà không ảnh hưởng Domain")
    print("   - Test business logic với Mock Repository")
    print("   - Tách biệt concerns rõ ràng")
    print()


if __name__ == "__main__":
    try:
        demo_repository_flow()
        print()
        demo_repository_isolation()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
