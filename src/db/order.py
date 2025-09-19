from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Numeric,
    String,
)

from src.db.base import SchemaBase


class OrderOrm(SchemaBase):
    __tablename__ = "order"

    creation_dttm = Column(DateTime(), default=datetime.now, nullable=False)
    user_id = Column(String(255), nullable=False)
    address = Column(String(), nullable=False)
    payment_amount = Column(Numeric(19, 2), nullable=False)
    payment_link = Column(String(), nullable=False)
