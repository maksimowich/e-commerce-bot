from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from yookassa import Configuration

from src.handlers import (
    start,
    category,
    subcategory,
    product,
    cart,
    order,
    faq,
)
from src.core.config import app_settings
from src.core.db_helper import db_helper
from src.middleware.database import DatabaseMiddleware


async def main():
    await db_helper.check_connection()

    Configuration.account_id = app_settings.yookassa.account_id
    Configuration.secret_key = app_settings.yookassa.secret_key

    bot = Bot(
        token=app_settings.tg.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(
        storage=MemoryStorage(),
    )
    dp.update.middleware.register(DatabaseMiddleware(db_helper.session_getter))

    dp.include_router(start.router)
    dp.include_router(category.router)
    dp.include_router(subcategory.router)
    dp.include_router(product.router)
    dp.include_router(cart.router)
    dp.include_router(order.router)
    dp.include_router(faq.router)

    await bot.delete_webhook()
    await bot.session.close()

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
