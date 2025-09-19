from uuid import UUID

from aiogram import types
from aiogram.fsm.context import FSMContext

from src.handlers.cart import CartState, router


@router.callback_query(lambda c: c.data.startswith("add_to_cart_product_"))
async def add_to_cart(
        callback: types.CallbackQuery,
        state: FSMContext,
):
    product_id = UUID(callback.data.split("_")[-1])

    await state.update_data(product_id=product_id)
    await state.set_state(CartState.waiting_for_quantity)

    await callback.message.answer(
        f"Товар добавлен в корзину. Введите количество:"
    )
    await callback.answer()
