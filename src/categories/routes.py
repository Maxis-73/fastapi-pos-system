from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from .schemas import CreateCategoryRequest, CreateCategoryResponse, AllCategoriesResponse
from .service import insert_category, get_active_categories
from src.auth.service import get_current_user


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/create", response_model=CreateCategoryResponse)
async def create_category(category_data: CreateCategoryRequest, db: Session = Depends(get_db)):
    return insert_category(db, category_data)

@router.get("/", response_model=AllCategoriesResponse)
async def get_all_categories(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_active_categories(db)

@router.get("/{category_id}")
async def get_category_by_id():
    pass

@router.put("/{category_id}")
async def update_category():
    pass

@router.patch("/deactivate/{category_id}")
async def deactivate_category():
    pass

@router.patch("/activate/{category_id}")
async def deactivate_category():
    pass