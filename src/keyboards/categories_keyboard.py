from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from src.db import CategoryOrm


def get_categories_keyboard(
        categories: Sequence[CategoryOrm],
        page: int,
        total_pages: int,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for category in categories:
        logger.info(f"category_{category.id}")
        keyboard.add(
            InlineKeyboardButton(
                text=category.name,
                callback_data=f"category_{category.id}"
            )
        )

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"category_page_{page - 1}"
            )
        )
    if page < (total_pages - 1):
        pagination_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"category_page_{page + 1}",
            )
        )

    if pagination_buttons:
        keyboard.row(*pagination_buttons)

    return keyboard.as_markup()
