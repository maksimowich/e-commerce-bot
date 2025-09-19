from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.keyboards.products_keyboard import show_products

router = Router()


@router.callback_query(lambda c: c.data == "prev_products_page")
async def prev_products_page(
        callback: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    current_page = data.get("current_page", 0)
    subcategory_id = data.get("subcategory_id")

    if current_page > 0:
        await state.update_data(current_page=current_page - 1)
        await show_products(
            message=callback.message,
            state=state,
            session=session,
            subcategory_id=subcategory_id,
        )
    await callback.answer()


@router.callback_query(lambda c: c.data == "next_products_page")
async def next_products_page(
        callback: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    current_page = data.get("current_page", 0)
    subcategory_id = data.get("subcategory_id")

    await state.update_data(current_page=current_page + 1)
    await show_products(
        message=callback.message,
        state=state,
        session=session,
        subcategory_id=subcategory_id,
    )
    await callback.answer()
