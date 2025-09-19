from math import ceil
from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import CategoryOrm


class CategoryService:
    @staticmethod
    async def get_categories(
            session: AsyncSession,
            page: int,
            page_size: int,
    ) -> Sequence[CategoryOrm]:
        offset = page * page_size
        query = (
            select(CategoryOrm)
            .offset(offset)
            .limit(page_size)
        )
        result = await session.execute(query)
        categories = result.scalars().all()
        return categories

    @staticmethod
    async def get_category_by_id(
            session: AsyncSession,
            category_id: UUID,
    ) -> CategoryOrm:
        query = (
            select(CategoryOrm)
            .where(CategoryOrm.id == category_id)
        )
        result = await session.execute(query)
        category = result.scalars().first()
        return category

    @staticmethod
    async def get_total_pages(
            session: AsyncSession,
            page_size: int,
    ) -> int:
        query = (
            select(func.count())
            .select_from(CategoryOrm)
        )
        result = await session.execute(query)
        total_categories = result.scalar()
        total_pages = ceil(total_categories / page_size)
        return total_pages
