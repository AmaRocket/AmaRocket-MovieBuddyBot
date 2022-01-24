from aiogram.dispatcher.filters.state import StatesGroup, State

# ================ FINITE STATE MACHINE ===============================================================================
class FormCriteria(StatesGroup):
    title = State()
    genre = State()
    voteaverage = State()
    year = State()

# =====================================================================================================================
