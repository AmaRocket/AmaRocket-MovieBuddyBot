from aiogram.dispatcher.filters.state import State, StatesGroup


# ================ FINITE STATE MACHINE ===============================================================================
class FormCriteria(StatesGroup):
    """
    save state of searching criteria
    """

    title = State()
    genre = State()
    voteaverage = State()
    year = State()


# =====================================================================================================================
