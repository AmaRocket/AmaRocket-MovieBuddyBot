from aiogram import types


def start():
    buttons = [
        types.InlineKeyboardButton(text='Search Movies', callback_data='movies'),
        types.InlineKeyboardButton(text='My Movie List', callback_data='movie_list_0')
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def my_movies(first, movie, title, movie_id):
    buttons = []

    buttons.append(types.InlineKeyboardButton(
        text='Trailer YouTube',
        url=f'https://www.youtube.com/results?search_query=+{title}+trailer'
    ))

    buttons.append(types.InlineKeyboardButton(
        text='More Info On TMDB',
        url=f'https://www.themoviedb.org/movie/{movie_id}'
    ))

    if not first <= 0:
        buttons.append(types.InlineKeyboardButton(text='<', callback_data=f'movie_list_{first - 1}'))

    if not first >= movie - 1:
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'movie_list_{first + 1}'))

    buttons.append(types.InlineKeyboardButton(text='Back To Movies Option', callback_data='movies'))

    # buttons.append(types.InlineKeyboardButton(text='Add To Movie List', callback_data='add_to_movie_list'))

    buttons.append(types.InlineKeyboardButton(text='Movie Like This', callback_data='similar_0'))

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def menu_():
    buttons = [
        types.InlineKeyboardButton(text='Popular Movies List', callback_data='popular_0'),
        types.InlineKeyboardButton(text='Find Film By Title', callback_data='title_0'),
        types.InlineKeyboardButton(text='Find Film By Criteria', callback_data='criteria_0')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


# Inline buttons for a message with a popular movies.
def popular_movie_buttons(first, popular_list, original_name, id):
    buttons = []
    buttons.append(types.InlineKeyboardButton(
        text='Trailer YouTube',
        url=f'https://www.youtube.com/results?search_query=+{original_name}+trailer'
    ))

    buttons.append(types.InlineKeyboardButton(
        text='More Info On TMDB',
        url=f'https://www.themoviedb.org/movie/{id}'
    ))

    if not first <= 0:
        buttons.append(types.InlineKeyboardButton(text='<', callback_data=f'popular_{first - 1}'))

    if not first >= popular_list - 1:
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'popular_{first + 1}'))

    buttons.append(types.InlineKeyboardButton(text='Back To Movies Option', callback_data='movies'))

    buttons.append(types.InlineKeyboardButton(text='Add To Movie List', callback_data='add_to_movie_list'))

    buttons.append(types.InlineKeyboardButton(text='Movie Like This', callback_data='similar_0'))

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def similar_movie_keyboard(first, movie_list, original_name, id):
    buttons = []
    buttons.append(types.InlineKeyboardButton(
        text='Trailer YouTube',
        url=f'https://www.youtube.com/results?search_query=+{original_name}+trailer'
    ))

    buttons.append(types.InlineKeyboardButton(
        text='More Info On TMDB',
        url=f'https://www.themoviedb.org/movie/{id}'
    ))

    if not first <= 0:
        buttons.append(types.InlineKeyboardButton(text='<', callback_data=f'similar_{first - 1}'))

    if not first >= movie_list - 1:
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'similar_{first + 1}'))

    buttons.append(types.InlineKeyboardButton(text='Back To Movies Option', callback_data='movies'))

    buttons.append(types.InlineKeyboardButton(text='Add To Movie List', callback_data='add_to_movie_list'))

    buttons.append(types.InlineKeyboardButton(text='Movie Like This', callback_data='similar_0'))

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
        text='More Info On TMDB',
        url=f'https://www.themoviedb.org/movie/{id}'
    ))

    if not first <= 0:
        buttons.append(types.InlineKeyboardButton(text='<', callback_data=f'find_{first - 1}'))

    if not first >= movie_list - 1:
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'find_{first + 1}'))

    buttons.append(types.InlineKeyboardButton(text='Back To Movies Option', callback_data='movies'))

    buttons.append(types.InlineKeyboardButton(text='Add To Movie List', callback_data='add_to_movie_list'))

    buttons.append(types.InlineKeyboardButton(text='Movie Like This', callback_data='similar_0'))

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
    buttons = []

    buttons.append(types.InlineKeyboardButton(
        text='Trailer YouTube',
        url=f'https://www.youtube.com/results?search_query=+{original_name}+trailer'
    ))

    buttons.append(types.InlineKeyboardButton(
        text='More Info On TMDB',
        url=f'https://www.themoviedb.org/movie/{id}'
    ))

    if not first <= 0:
        buttons.append(types.InlineKeyboardButton(text='<', callback_data=f'total_{first - 1}'))

    if not first >= data - 1:
        buttons.append(types.InlineKeyboardButton(text='>', callback_data=f'total_{first + 1}'))

    buttons.append(types.InlineKeyboardButton(text='Back To Movies Option', callback_data='movies'))

    buttons.append(types.InlineKeyboardButton(text='Add To Movie List', callback_data='add_to_movie_list'))

    buttons.append(types.InlineKeyboardButton(text='Movie Like This', callback_data='similar_0'))

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


# genres keyboard
def genres_keyboard():
    buttons = []

    buttons.append(types.InlineKeyboardButton(text='Action', callback_data='28'))
    buttons.append(types.InlineKeyboardButton(text='Adventure', callback_data='12'))
    buttons.append(types.InlineKeyboardButton(text='Animation', callback_data='16'))
    buttons.append(types.InlineKeyboardButton(text='Comedy', callback_data='35'))
    buttons.append(types.InlineKeyboardButton(text='Crime', callback_data='80'))
    buttons.append(types.InlineKeyboardButton(text='Documentary', callback_data='99'))
    buttons.append(types.InlineKeyboardButton(text='Drama', callback_data='18'))
    buttons.append(types.InlineKeyboardButton(text='Family', callback_data='10751'))
    buttons.append(types.InlineKeyboardButton(text='Fantasy', callback_data='14'))
    buttons.append(types.InlineKeyboardButton(text='History', callback_data='36'))
    buttons.append(types.InlineKeyboardButton(text='Horror', callback_data='27'))
    buttons.append(types.InlineKeyboardButton(text='Music', callback_data='10402'))
    buttons.append(types.InlineKeyboardButton(text='Mystery', callback_data='9648'))
    buttons.append(types.InlineKeyboardButton(text='Romance', callback_data='10749'))
    buttons.append(types.InlineKeyboardButton(text='Science Fiction', callback_data='878'))
    buttons.append(types.InlineKeyboardButton(text='TV Movie', callback_data='10770'))
    buttons.append(types.InlineKeyboardButton(text='Thriller', callback_data='53'))
    buttons.append(types.InlineKeyboardButton(text='War', callback_data='10752'))
    buttons.append(types.InlineKeyboardButton(text='Western', callback_data='37'))

    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.insert(types.InlineKeyboardButton(text='Back To Movies Option', callback_data='finish'))
    keyboard.add(*buttons)

    return keyboard
