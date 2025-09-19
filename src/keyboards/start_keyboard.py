from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Каталог", callback_data="category_page_0"))
    keyboard.add(InlineKeyboardButton(text="Корзина", callback_data="view_cart"))
    return keyboard.as_markup()
