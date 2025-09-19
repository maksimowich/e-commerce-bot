from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID

from src.core.config import app_settings
from src.db.base import SchemaBase


class CartItemOrm(SchemaBase):
    __tablename__ = "cart_item"

    user_id = Column(String(255), nullable=False)
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{app_settings.postgres.schema_}.product.id",
            ondelete="CASCADE",
        ),
    )
    quantity = Column(Integer(), nullable=False)
