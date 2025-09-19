from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import CartService, ProductService


async def construct_cart_keyboard(
        callback: types.CallbackQuery,
        session: AsyncSession,
) -> None:
    user_id = callback.from_user.id

    cart_items = await CartService.get_cart_items(
        session=session,
        user_id=str(user_id),
    )

    if not cart_items:
        await callback.message.answer("Ваша корзина пуста.")

    else:
        text = "Ваша корзина:\n\n"
        builder = InlineKeyboardBuilder()

        for cart_item in cart_items:
            product = await ProductService.get_product(session, cart_item.product_id)
            item_price = cart_item.quantity * product.price
            text += f"📦 Товар {product.name} — {cart_item.quantity} шт. {item_price} руб.\n"
            builder.button(
                text=f"❌ Удалить товар {product.name}",
                callback_data=f"remove_from_cart_{cart_item.id}",
            )
            builder.button(
                text=f"✏️ Изменить кол-во {product.name}",
                callback_data=f"edit_cart_item_{cart_item.id}",
            )
        payment_amount = await CartService.get_payment_amount(
            session=session,
            cart_items=cart_items,
        )
        text += f"\nИтоговая сумма заказа: {payment_amount} руб."

        builder.button(
            text="Очистить корзину",
            callback_data="clear_cart",
        )

        builder.button(
            text="️Сделать заказ",
            callback_data="make_order",
        )

        await callback.message.answer(
            text,
            reply_markup=builder.as_markup(),
        )
        await callback.answer()
