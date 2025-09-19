from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.cart import router
from src.keyboards.cart_keyboard import construct_cart_keyboard


@router.callback_query(lambda c: c.data == "view_cart")
async def view_cart(
        callback: types.CallbackQuery,
        session: AsyncSession,
):
    await construct_cart_keyboard(
        callback=callback,
        session=session,
    )
