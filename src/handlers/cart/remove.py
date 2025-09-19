from uuid import UUID

from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.cart import router
from src.services import CartService

from .view import view_cart


@router.callback_query(lambda c: c.data.startswith("remove_from_cart_"))
async def remove_from_cart(
        callback: types.CallbackQuery,
        session: AsyncSession,
):
    cart_item_id = UUID(callback.data.split("_")[-1])

    await CartService.delete_cart_item(
        session=session,
        cart_item_id=cart_item_id,
    )

    await callback.message.delete()

    await callback.message.answer(f"Товар удалён из корзины!")
    await view_cart(callback, session)
