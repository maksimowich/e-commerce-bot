from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

router = Router()


class CartState(StatesGroup):
    waiting_for_quantity = State()
    waiting_for_confirmation = State()


from src.handlers.cart import add  # noqa
from src.handlers.cart import add_cancel  # noqa
from src.handlers.cart import add_confirm  # noqa
from src.handlers.cart import clear  # noqa
from src.handlers.cart import edit  # noqa
from src.handlers.cart import remove  # noqa
from src.handlers.cart import view  # noqa
from src.handlers.cart import waiting_for_quantity  # noqa
