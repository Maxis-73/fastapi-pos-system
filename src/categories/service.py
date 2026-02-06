from sqlalchemy.orm import Session
from .schemas import CreateCategoryRequest, CreateCategoryResponse, AllCategoriesResponse, Category as CategorySchema
from .models import Category

def insert_category(db: Session, category_data: CreateCategoryRequest):
    # 1. Instancia del objeto para ORM
    category_db = Category(
        name=category_data.name,
        description=category_data.description
    )

    # 2. Persistir
    db.add(category_db)
    db.commit()
    db.refresh(category_db)

    # 3. Respuesta
    return CreateCategoryResponse(
        message = "Categoria creada correctamente",
        id = category_db.id
    )

def get_active_categories(db: Session):
    # 1. Obtenemos todas las categorias activas
    categories_db = db.query(Category).filter(Category.is_active == True).all()
    
    # 2. Convertir objetos SQLAlchemy a schemas Pydantic
    categories_schema = [
        CategorySchema(
            id=cat.id,
            name=cat.name,
            description=cat.description,
            is_active=cat.is_active,
            created_at=cat.created_at,
            updated_at=cat.updated_at
        )
        for cat in categories_db
    ]
    
    # 3. Retornar respuesta
    return AllCategoriesResponse(categories=categories_schema)