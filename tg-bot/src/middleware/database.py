from aiogram import BaseMiddleware


class DatabaseMiddleware(BaseMiddleware):
    def __init__(
            self,
            session_getter,
    ) -> None:
        self.session_getter = session_getter

    async def __call__(
        self,
        handler,
        event,
        data,
    ) -> any:
        async with self.session_getter() as session:
            data["session"] = session
            return await handler(event, data)
