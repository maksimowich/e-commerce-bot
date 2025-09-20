from uuid import UUID

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_file import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import app_settings
from src.services import ProductService


async def show_products(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession,
        subcategory_id: UUID | None,
):
    data = await state.get_data()
    current_page = data.get("current_page", 0)
    if subcategory_id is None:
        subcategory_id = data.get("subcategory_id")
    else:
        await state.update_data(subcategory_id=subcategory_id)

    page_size = app_settings.forms.products_page_size
    offset = current_page * page_size
    limit = page_size
    page_products = await ProductService.get_products(
        session=session,
        subcategory_id=subcategory_id,
        offset=offset,
        limit=limit,
    )
    if len(page_products) == 0:
        await message.answer("В выбранной подкатегории нет товаров.")
        return

    total_pages = await ProductService.get_total_pages(
        session=session,
        subcategory_id=subcategory_id,
        page_size=page_size,
    )

    for product in page_products:
        text = f"📦 {product.name}\n💰 {product.price} руб."
        builder = InlineKeyboardBuilder()
        builder.button(
            text="🛒 Положить в корзину",
            callback_data=f"add_to_cart_product_{product.id}",
        )
        if product.photo_link:
            try:
                await message.answer_photo(
                    photo=FSInputFile(product.photo_link),
                    caption=text,
                    reply_markup=builder.as_markup()
                )
                continue
            except Exception:
                pass
        await message.answer(
            text=text,
            reply_markup=builder.as_markup()
        )

    builder = InlineKeyboardBuilder()
    if current_page > 0:
        builder.button(
            text="⬅️ Назад",
            callback_data="prev_products_page",
        )
    if current_page < (total_pages - 1):
        builder.button(
            text="Вперёд ➡️",
            callback_data="next_products_page",
        )

    await message.answer(
        f"Страница {current_page + 1} из {total_pages}.",
        reply_markup=builder.as_markup(),
    )
