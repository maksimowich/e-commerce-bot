from typing import Sequence
from uuid import UUID

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import app_settings
from src.db import SubcategoryOrm
from src.services import SubcategoryService


def get_subcategories_keyboard(
        subcategories: Sequence[SubcategoryOrm],
        category_id: UUID,
        page: int,
        total_pages: int,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for subcategory in subcategories:
        keyboard.add(
            InlineKeyboardButton(
                text=subcategory.name,
                callback_data=f"subcategory_{subcategory.id}"
            )
        )

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"category_{category_id}_subcategory_page_{page - 1}"
            )
        )
    if page < (total_pages - 1):
        pagination_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"category_{category_id}_subcategory_page_{page + 1}",
            )
        )

    if pagination_buttons:
        keyboard.row(*pagination_buttons)

    return keyboard.as_markup()


async def construct_subcategories_keyboard(
        callback: CallbackQuery,
        session: AsyncSession,
        category_id: UUID,
        page: int,
) -> None:
    page_size = app_settings.forms.subcategories_page_size
    subcategories = await SubcategoryService.get_subcategories(
        session=session,
        category_id=category_id,
        page=page,
        page_size=page_size,
    )
    if len(subcategories) == 0:
        await callback.message.answer("В выбранной категории нет подкатегорий.")
        return

    total_pages = await SubcategoryService.get_total_pages(
        session=session,
        category_id=category_id,
        page_size=page_size,
    )
    subcategories_keyboard = get_subcategories_keyboard(
        subcategories=subcategories,
        category_id=category_id,
        page=page,
        total_pages=total_pages,
    )
    if subcategories_keyboard:
        await callback.message.edit_text(
            "Список подкатегорий:",
            reply_markup=subcategories_keyboard,
        )
