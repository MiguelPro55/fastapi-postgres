from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PaginatedUserResponse
from app.crud.user import create_user, get_users, get_user_by_id, update_user, delete_user
from math import ceil

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("", response_model=UserResponse, status_code=201)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists")

@router.get("", response_model=PaginatedUserResponse)
async def read_users(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Cantidad de items por página"),
    db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * page_size
    users, total = await get_users(db, skip=skip, limit=page_size)
    total_pages = ceil(total / page_size) if total > 0 else 1
    
    return PaginatedUserResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/{user_id}", response_model=UserResponse)
async def read(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=204)
async def delete(user_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return