from aiogram.dispatcher.filters.state import State, StatesGroup


class FormMailing(StatesGroup):
    """
    save state of mailing text
    """

    text = State()
    language = State()
