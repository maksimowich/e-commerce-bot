from uuid import UUID

from yookassa import Payment


async def create_payment(
        order_id: UUID,
        user_id: str,
        address: str,
        payment_amount: float,
) -> str:
    payment = Payment.create({
        "amount": {
            "value": str(payment_amount),
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.com/",
        },
        "description": f"Payment for Order {str(order_id)}",
        "metadata": {
            "user_id": user_id,
            "address": address,
        },
        "capture": False,
        "test": True,
    }, order_id)

    return payment.confirmation.confirmation_url
