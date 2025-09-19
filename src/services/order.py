from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import OrderOrm


class OrderService:
    @staticmethod
    async def add_order(
            session: AsyncSession,
            order_id: UUID,
            user_id: str,
            address: str,
            payment_amount: float,
            payment_link: str,
    ) -> OrderOrm:
        order = OrderOrm(
            id=order_id,
            user_id=user_id,
            address=address,
            payment_amount=payment_amount,
            payment_link=payment_link,
        )
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order
