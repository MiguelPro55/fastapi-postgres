from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(**user.model_dump())
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        raise

async def update_user(db: AsyncSession, user_id: int, user: UserUpdate):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user is None:
        return None
    for key, value in user.model_dump().items():
        setattr(existing_user, key, value)
    db.add(existing_user)
    await db.commit()
    await db.refresh(existing_user)
    return existing_user

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user is None:
        return False
    await db.delete(existing_user)
    await db.commit()
    return True

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    # Obtener el total de usuarios
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar()
    
    # Obtener los usuarios paginados
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    
    return users, total

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
