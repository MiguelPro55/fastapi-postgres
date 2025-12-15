from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None
    cellphone: str | None = None
    active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    active: bool

class PaginatedUserResponse(BaseModel):
    items: List[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
