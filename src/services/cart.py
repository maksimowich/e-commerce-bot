from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import CartItemOrm, ProductOrm


class CartService:
    @staticmethod
    async def add_cart_item(
        session: AsyncSession,
        user_id: str,
        product_id: UUID,
        quantity: int,
    ) -> CartItemOrm:
        cart_item = CartItemOrm(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
        )
        session.add(cart_item)
        await session.commit()
        await session.refresh(cart_item)
        return cart_item

    @staticmethod
    async def edit_cart_item(
        session: AsyncSession,
        cart_item_id: UUID,
        quantity: int,
    ) -> UUID:
        query = (
            select(CartItemOrm)
            .where(CartItemOrm.id == cart_item_id)
        )
        result = await session.execute(query)
        cart_item = result.scalar()
        cart_item.quantity = quantity
        await session.commit()
        return cart_item_id


    @staticmethod
    async def get_cart_items(
        session: AsyncSession,
        user_id: str,
    ) -> Sequence[CartItemOrm]:
        query = (
            select(CartItemOrm)
            .where(CartItemOrm.user_id == user_id)
        )
        result = await session.execute(query)
        cart_items = result.scalars().all()
        return cart_items

    @staticmethod
    async def clear_cart(
        session: AsyncSession,
        user_id: str,
    ) -> None:
        query = (
            select(CartItemOrm)
            .where(CartItemOrm.user_id == user_id)
        )
        result = await session.execute(query)
        cart_items = result.scalars().all()
        for cart_item in cart_items:
            await session.delete(cart_item)
        await session.commit()

    @staticmethod
    async def delete_cart_item(
            session: AsyncSession,
            cart_item_id: UUID,
    ) -> UUID:
        query = (
            select(CartItemOrm)
            .where(CartItemOrm.id == cart_item_id)
        )
        result = await session.execute(query)
        cart_item = result.scalar()
        await session.delete(cart_item)
        await session.commit()
        return cart_item.product_id

    @staticmethod
    async def get_payment_amount(
            session: AsyncSession,
            cart_items: Sequence[CartItemOrm],
    ) -> float:
        products_ids = [
            cart_item.product_id
            for cart_item in cart_items
        ]
        query = (
            select(ProductOrm.price, CartItemOrm.quantity)
            .join(CartItemOrm, ProductOrm.id == CartItemOrm.product_id)
            .where(CartItemOrm.product_id.in_(products_ids))
        )

        result = await session.execute(query)
        items = result.all()
        total_amount = sum(item.price * item.quantity for item in items)
        return total_amount
