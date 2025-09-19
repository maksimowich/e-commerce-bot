from sqlalchemy import (
    Column,
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import UUID

from src.core.config import app_settings
from src.db.base import SchemaBase


class SubcategoryOrm(SchemaBase):
    __tablename__ = "subcategory"

    name = Column(String(100), unique=True)
    description = Column(String(500), nullable=True)

    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{app_settings.postgres.schema_}.category.id",
            ondelete="CASCADE",
        ),
    )
