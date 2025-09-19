from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.cart import router
from src.services import CartService


@router.callback_query(lambda c: c.data == "clear_cart")
async def clear_cart(
        callback: types.CallbackQuery,
        session: AsyncSession,
):
    user_id = callback.from_user.id

    await CartService.clear_cart(
        session=session,
        user_id=str(user_id),
    )

    await callback.message.delete()

    await callback.message.answer("Корзина очищена.")
