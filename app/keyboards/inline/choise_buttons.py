from aiogram import types


def menu_():
    btn = [
        types.InlineKeyboardButton(text='Popular Movies', callback_data='popular_0'),
        types.InlineKeyboardButton(text='Find By Title', callback_data='title_0'),
        types.InlineKeyboardButton(text='Criteria', callback_data='criteria_0')
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*btn)
    return keyboard


# Inline buttons for a message with a popular movies.
def popular_movie_buttons(first, popular_list, original_name, id):
    buttons = []
    buttons.append(types.InlineKeyboardButton(
        text='Trailer YouTube',
        url=f'https://www.youtube.com/results?search_query=+{original_name}+trailer'
    ))

    buttons.append(types.InlineKeyboardButton(
        text="More Info On TMDB",
        url=f'https://www.themoviedb.org/movie/{id}'
    ))

    if not first <= 0:
        buttons.append(types.InlineKeyboardButton(text="<", callback_data=f"popular_{first - 1}"))

    if not first >= popular_list:
        buttons.append(types.InlineKeyboardButton(text=">", callback_data=f"popular_{first + 1}"))

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def title_keyboard():
    buttons = []
    buttons.append(types.InlineKeyboardButton(text='Find', callback_data='find_0'))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


# Inline buttons for a message (find_by_title).
def title_movie_buttons(first, movie_list, original_name, id):
    buttons = []

    buttons.append(types.InlineKeyboardButton(
        text='Trailer YouTube',
        url=f'https://www.youtube.com/results?search_query=+{original_name}+trailer'
    ))

    buttons.append(types.InlineKeyboardButton(
        text="More Info On TMDB",
        url=f'https://www.themoviedb.org/movie/{id}'
    ))

    if not first <= 0:
        buttons.append(types.InlineKeyboardButton(text="<", callback_data=f"find_{first - 1}"))

    if not first >= movie_list:
        buttons.append(types.InlineKeyboardButton(text=">", callback_data=f"find_{first + 1}"))

    buttons.append(types.InlineKeyboardButton(text='Finish', callback_data='finish'))

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def total_keyboard():
    buttons = []
    buttons.append(types.InlineKeyboardButton(text='Result', callback_data='total_0'))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def result_keyboard(first, data, original_name, id):
    # Trailer Buttons

    buttons = []

    buttons.append(types.InlineKeyboardButton(
        text='Trailer YouTube',
        url=f'https://www.youtube.com/results?search_query=+{original_name}+trailer'
    ))

    buttons.append(types.InlineKeyboardButton(
        text="More Info On TMDB",
        url=f'https://www.themoviedb.org/movie/{id}'
    ))

    if not first <= 0:
        buttons.append(types.InlineKeyboardButton(text="<", callback_data=f"total_{first - 1}"))

    if not first >= data:
        buttons.append(types.InlineKeyboardButton(text=">", callback_data=f"total_{first + 1}"))

    buttons.append(types.InlineKeyboardButton(text='Finish', callback_data='finish'))

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard
