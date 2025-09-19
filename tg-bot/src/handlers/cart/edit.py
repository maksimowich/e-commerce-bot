from uuid import UUID

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.cart import router
from src.services import CartService


class CartStates(StatesGroup):
    waiting_quantity = State()


@router.callback_query(lambda c: c.data.startswith("edit_cart_item_"))
async def start_edit_cart_item(
        callback: types.CallbackQuery,
        state: FSMContext,
):
    cart_item_id = UUID(callback.data.split("_")[-1])
    await state.update_data(cart_item_id=str(cart_item_id))
    await state.set_state(CartStates.waiting_quantity)
    await callback.message.answer("Введите количество товара:")
    await callback.answer()


@router.message(StateFilter(CartStates.waiting_quantity))
async def process_quantity_input(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession,
):
    try:
        data = await state.get_data()
        cart_item_id = UUID(data['cart_item_id'])

        new_quantity = int(message.text)
        if new_quantity <= 0:
            await message.answer("Количество должно быть больше 0.")
            return

        await CartService.edit_cart_item(
            session=session,
            cart_item_id=cart_item_id,
            quantity=new_quantity,
        )

        await state.clear()
        await message.answer("✅ Количество товара изменено")

    except ValueError:
        await message.answer("Пожалуйста, введите число.")
    except Exception:
        await message.answer("Произошла ошибка при обновлении количества.")
        await state.clear()
