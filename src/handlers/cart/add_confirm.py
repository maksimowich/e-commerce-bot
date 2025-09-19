from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.handlers.cart import CartState, router
from src.services import CartService


@router.callback_query(CartState.waiting_for_confirmation, lambda c: c.data == "confirm_add")
async def confirm_add(
        callback: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    user_id = callback.from_user.id

    await CartService.add_cart_item(
        session=session,
        user_id=str(user_id),
        product_id=product_id,
        quantity=quantity,
    )

    await callback.message.delete()
    await callback.message.answer(
        f"Товар в количестве {quantity} шт. добавлен в корзину!"
    )
    await callback.answer()
