from math import ceil
from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import SubcategoryOrm


class SubcategoryService:
    @staticmethod
    async def get_subcategories(
            session: AsyncSession,
            category_id: UUID,
            page: int,
            page_size: int,
    ) -> Sequence[SubcategoryOrm]:
        offset = page * page_size
        query = (
            select(SubcategoryOrm)
            .where(SubcategoryOrm.category_id == category_id)
            .offset(offset)
            .limit(page_size)
        )
        result = await session.execute(query)
        subcategories = result.scalars().all()
        return subcategories

    @staticmethod
    async def get_subcategory_by_id(
            session: AsyncSession,
            subcategory_id: UUID,
    ) -> SubcategoryOrm:
        query = (
            select(SubcategoryOrm)
            .where(SubcategoryOrm.id == subcategory_id)
        )
        result = await session.execute(query)
        subcategory = result.scalars().first()
        return subcategory

    @staticmethod
    async def get_total_pages(
            session: AsyncSession,
            category_id: UUID,
            page_size: int,
    ) -> int:
        query = (
            select(func.count())
            .select_from(SubcategoryOrm)
            .where(SubcategoryOrm.category_id == category_id)
        )
        result = await session.execute(query)
        total_subcategories = result.scalar()
        total_pages = ceil(total_subcategories / page_size)
        return total_pages
