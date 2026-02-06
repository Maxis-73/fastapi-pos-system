from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional

class Category(BaseModel):
    id: UUID
    name: str
    description: str
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class CreateCategoryRequest(BaseModel):
    name: str
    description: str

class CreateCategoryResponse(BaseModel):
    message: str = "Categoria creada correctamente"
    id: UUID

class AllCategoriesResponse(BaseModel):
    categories: List[Category]