from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.core.config import app_settings


Base = declarative_base()


class SchemaBase(Base):
    __abstract__ = True
    __table_args__ = {"schema": app_settings.postgres.schema_}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
