import re
from uuid import UUID

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import uuid_regex
from src.keyboards.subcategories_keyboard import construct_subcategories_keyboard
from src.keyboards.products_keyboard import show_products
from src.services import SubcategoryService

router = Router()


@router.callback_query(lambda c: re.match(fr"category_{uuid_regex}_subcategory_page_\d+$", c.data))
async def handle_page(
        callback: types.CallbackQuery,
        session: AsyncSession,
):
    match = re.match(fr"category_({uuid_regex})_subcategory_page_(\d+)", callback.data)
    if match:
        category_id = UUID(match.group(1))
        page = int(match.group(2))
    else:
        raise Exception(
            f"Invalid callback path: {callback.data}"
        )

    await construct_subcategories_keyboard(
        callback=callback,
        session=session,
        category_id=category_id,
        page=page,
    )
    await callback.answer()


@router.callback_query(lambda c: re.match(fr"subcategory_{uuid_regex}$", c.data))
async def handle_subcategory(
        callback: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    match = re.match(fr"subcategory_({uuid_regex})", callback.data)
    if match:
        subcategory_id = UUID(match.group(1))
    else:
        raise Exception(
            f"Invalid callback path: {callback.data}"
        )

    subcategory = await SubcategoryService.get_subcategory_by_id(
        session=session,
        subcategory_id=subcategory_id,
    )
    if subcategory:
        await show_products(
            message=callback.message,
            state=state,
            session=session,
            subcategory_id=subcategory_id,
        )
