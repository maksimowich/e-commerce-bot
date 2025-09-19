from aiogram import types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.dispatcher.router import Router

router = Router()


faq_data = {
    "Как начать пользоваться ботом?": "Чтобы начать, нажмите /start и следуйте инструкциям.",
    "Как связаться с поддержкой?": "Вы не можете связаться с поддержкой.",
    "Какие команды доступны?": "Доступные команды: /start",
    "Как изменить настройки?": "Вы не можете изменить настройки.",
}


@router.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery):
    query = inline_query.query.lower()
    results = []

    for question, answer in faq_data.items():
        if query in question.lower():
            results.append(
                InlineQueryResultArticle(
                    id=question,
                    title=question,
                    input_message_content=InputTextMessageContent(message_text=answer),
                    description=answer,
                )
            )

    await inline_query.answer(results)
