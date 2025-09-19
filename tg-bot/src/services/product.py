from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import ProductOrm


class ProductService:
    @staticmethod
    async def get_products(
            session: AsyncSession,
            subcategory_id: UUID,
            offset: int,
            limit: int,
    ) -> Sequence[ProductOrm]:
        query = (
            select(ProductOrm)
            .where(ProductOrm.subcategory_id == subcategory_id)
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(query)
        products = result.scalars().all()
        return products

    @staticmethod
    async def get_total_pages(
            session: AsyncSession,
            subcategory_id: UUID,
            page_size: int,
    ) -> int:
        query = (
            select(func.count())
            .select_from(ProductOrm)
            .where(ProductOrm.subcategory_id == subcategory_id)
        )
        result = await session.execute(query)
        total_products = result.scalar()
        total_pages = (
                (total_products // page_size) + (1 if total_products % page_size != 0 else 0)
        )
        return total_pages

    @staticmethod
    async def get_product_name(
            session: AsyncSession,
            product_id: UUID,
    ) -> str | None:
        query = (
            select(ProductOrm)
            .where(ProductOrm.id == product_id)
        )
        result = await session.execute(query)
        product = result.scalar()
        return product.name if product else None

    @staticmethod
    async def get_product(
            session: AsyncSession,
            product_id: UUID,
    ) -> ProductOrm | None:
        query = (
            select(ProductOrm)
            .where(ProductOrm.id == product_id)
        )
        result = await session.execute(query)
        return result.scalar()
