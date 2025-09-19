from sqlalchemy import (
    Column,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID

from src.core.config import app_settings
from src.db.base import SchemaBase


class ProductOrm(SchemaBase):
    __tablename__ = "product"

    name = Column(String(100), unique=True)
    description = Column(String(500), nullable=True)
    price = Column(Numeric(19, 2), nullable=False)
    photo_link = Column(String(), nullable=True)

    subcategory_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{app_settings.postgres.schema_}.subcategory.id",
            ondelete="CASCADE",
        ),
    )
