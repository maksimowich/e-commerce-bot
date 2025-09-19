from aiogram import types
from aiogram.fsm.context import FSMContext

from src.handlers.cart import CartState, router


@router.callback_query(CartState.waiting_for_confirmation, lambda c: c.data == "cancel_add")
async def cancel_add(
        callback: types.CallbackQuery,
        state: FSMContext,
):
    await state.update_data(quantity=None, product_id=None)
    await callback.message.delete()
    await callback.message.answer("Добавление товара отменено.")
    await callback.answer()
