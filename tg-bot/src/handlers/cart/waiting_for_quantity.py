from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.cart import CartState, router
from src.services.product import ProductService


@router.message(CartState.waiting_for_quantity)
async def process_quantity(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    product_id = data.get("product_id")
    product_name = await ProductService.get_product_name(
        session=session,
        product_id=product_id,
    )

    try:
        quantity = int(message.text)
        if quantity <= 0:
            await message.answer("Количество должно быть больше 0.")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите число.")
        return

    await state.update_data(quantity=quantity)
    await state.set_state(CartState.waiting_for_confirmation)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data="confirm_add"),
            InlineKeyboardButton(text="❌ Нет", callback_data="cancel_add"),
        ]
    ])

    await message.answer(
        f"Вы хотите добавить товар {product_name} в количестве {quantity} шт. в корзину?",
        reply_markup=keyboard,
    )
