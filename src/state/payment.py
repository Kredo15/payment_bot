from aiogram.filters.state import State, StatesGroup


class PaymentState(StatesGroup):
    subscription = State()
