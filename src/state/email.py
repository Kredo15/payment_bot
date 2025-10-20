from aiogram.filters.state import State, StatesGroup


class EmailState(StatesGroup):
    change_email = State()
