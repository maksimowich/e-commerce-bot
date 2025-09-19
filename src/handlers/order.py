from uuid import uuid4

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.create_payment import create_payment
from src.services import CartService, OrderService

router = Router()


class OrderStates(StatesGroup):
    waiting_for_address = State()


@router.callback_query(lambda c: c.data == 'make_order')
async def process_make_order(
        callback_query: types.CallbackQuery,
        state: FSMContext,
):
    await callback_query.message.answer("Введите адрес для доставки:")
    await state.set_state(OrderStates.waiting_for_address)


@router.message(OrderStates.waiting_for_address)
async def process_address(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession,
):
    user_id = str(message.from_user.id)

    address = message.text
    await state.update_data(address=address)

    cart_items = await CartService.get_cart_items(
        session=session,
        user_id=user_id,
    )
    payment_amount = await CartService.get_payment_amount(
        session=session,
        cart_items=cart_items,
    )
    order_id = uuid4()

    payment_link = await create_payment(
        order_id=order_id,
        user_id=user_id,
        address=address,
        payment_amount=payment_amount,
    )

    order = await OrderService.add_order(
        session=session,
        order_id=order_id,
        user_id=user_id,
        address=address,
        payment_amount=payment_amount,
        payment_link=payment_link,
    )
    await message.answer(
        f"Ваш заказ на сумму {payment_amount} руб. по адресу {address} оформлен.\n"
        f"Номер заказа: {order_id}\n\n"
        f"Ссылка для оплаты: {payment_link}"
    )
    await state.clear()
