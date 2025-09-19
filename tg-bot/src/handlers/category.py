import re
from uuid import UUID

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import app_settings, uuid_regex
from src.keyboards.categories_keyboard import get_categories_keyboard
from src.keyboards.subcategories_keyboard import construct_subcategories_keyboard
from src.services import CategoryService

router = Router()


@router.callback_query(lambda c: re.match(r"category_page_\d+$", c.data))
async def handle_page(
        callback: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    page = int(callback.data.split("_")[-1])
    data = await state.get_data()
    first_opened = data.get("first_opened", True)

    page_size = app_settings.forms.categories_page_size
    categories = await CategoryService.get_categories(
        session=session,
        page=page,
        page_size=page_size,
    )
    total_pages = await CategoryService.get_total_pages(
        session=session,
        page_size=page_size,
    )
    categories_keyboard = get_categories_keyboard(
        categories=categories,
        page=page,
        total_pages=total_pages,
    )

    if first_opened:
        await callback.message.answer(
            "Список категорий:",
            reply_markup=categories_keyboard,
        )
        await state.update_data(first_opened=False)
    else:
        await callback.message.edit_text(
            "Список категорий:",
            reply_markup=categories_keyboard,
        )
        await callback.answer()


@router.callback_query(lambda c: re.match(fr"category_{uuid_regex}$", c.data))
async def handle_category(
        callback: types.CallbackQuery,
        session: AsyncSession,
):
    logger.info(callback.data)
    category_id = UUID(callback.data.split("_")[-1])
    category = await CategoryService.get_category_by_id(
        session=session,
        category_id=category_id,
    )

    if category:
        await construct_subcategories_keyboard(
            callback=callback,
            session=session,
            category_id=category_id,
            page=0,
        )
    await callback.answer()
