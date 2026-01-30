from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Base Models
class ShopBase(BaseModel):
    name: str

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    photo_url: Optional[str] = None
    is_available: bool = True
    is_preorder: bool = False

# Read Models
class ShopRead(ShopBase):
    id: int
    webhook_secret: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryRead(CategoryBase):
    id: int
    shop_id: int
    
    class Config:
        from_attributes = True

class ProductRead(ProductBase):
    id: int
    shop_id: int
    category_id: int
    
    class Config:
        from_attributes = True

# Create Models
class ShopCreate(ShopBase):
    bot_token: str # Raw token, will be encrypted
    owner_id: int

class CategoryCreate(CategoryBase):
    shop_id: int

class ProductCreate(ProductBase):
    shop_id: int
    category_id: int
