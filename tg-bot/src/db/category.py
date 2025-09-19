from sqlalchemy import (
    Column,
    String,
)

from src.db.base import SchemaBase


class CategoryOrm(SchemaBase):
    __tablename__ = "category"

    name = Column(String(100), unique=True)
    description = Column(String(500), nullable=True)
