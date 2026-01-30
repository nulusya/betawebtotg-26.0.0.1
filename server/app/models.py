from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, DECIMAL, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from datetime import datetime
import enum
from .db import Base

class OrderStatus(str, enum.Enum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    DELIVERY = "DELIVERY"
    DONE = "DONE"
    CANCELED = "CANCELED"

class FeatureStatus(str, enum.Enum):
    PENDING = "PENDING"
    DONE = "DONE"

class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(Integer, index=True)
    
    bot_token_enc: Mapped[str] = mapped_column(String, unique=True)
    webhook_secret: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    name: Mapped[str] = mapped_column(String, default="My Shop")
    settings: Mapped[dict] = mapped_column(JSON, default={})
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    categories: Mapped[List["Category"]] = relationship(back_populates="shop", cascade="all, delete-orphan")
    products: Mapped[List["Product"]] = relationship(back_populates="shop", cascade="all, delete-orphan")
    orders: Mapped[List["Order"]] = relationship(back_populates="shop", cascade="all, delete-orphan")
    mailings: Mapped[List["Mailing"]] = relationship(back_populates="shop", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    shop_id: Mapped[int] = mapped_column(Integer, ForeignKey("shops.id"))
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)
    name: Mapped[str] = mapped_column(String)

    shop: Mapped["Shop"] = relationship(back_populates="categories")
    parent: Mapped[Optional["Category"]] = relationship(remote_side=[id], backref="children")
    products: Mapped[List["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    shop_id: Mapped[int] = mapped_column(Integer, ForeignKey("shops.id"))
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_preorder: Mapped[bool] = mapped_column(Boolean, default=False)

    shop: Mapped["Shop"] = relationship(back_populates="products")
    category: Mapped["Category"] = relationship(back_populates="products")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    shop_id: Mapped[int] = mapped_column(Integer, ForeignKey("shops.id"))
    
    customer_tg_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.NEW)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    delivery_data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    shop: Mapped["Shop"] = relationship(back_populates="orders")


class Mailing(Base):
    __tablename__ = "mailings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    shop_id: Mapped[int] = mapped_column(Integer, ForeignKey("shops.id"))
    
    message_text: Mapped[str] = mapped_column(String)
    photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[FeatureStatus] = mapped_column(SQLEnum(FeatureStatus), default=FeatureStatus.PENDING)

    shop: Mapped["Shop"] = relationship(back_populates="mailings")
