from aiogram import types

from loader import _


def starting():
    buttons = [types.InlineKeyboardButton(text=_("🔥 Lets Go! 🔥"), callback_data="go")]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def start():
    buttons = [
        types.InlineKeyboardButton(text=_("🎬 Find Movies"), callback_data="movies"),
        types.InlineKeyboardButton(
            text=_("🍿 My Movie List"), callback_data="movie_list_0"
        ),
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def my_movies(first, movie, title, movie_id):
    buttons = []

    buttons.append(
        types.InlineKeyboardButton(
            text=_("📺 Trailer YouTube"),
            url=f"https://www.youtube.com/results?search_query=+{title}+trailer",
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("ℹ️ More Info On TMDB"),
            url=f"https://www.themoviedb.org/movie/{movie_id}",
        )
    )

    if not first <= 0:
        buttons.append(
            types.InlineKeyboardButton(
                text="◀️", callback_data=f"movie_list_{first - 1}"
            )
        )

    if not first >= movie - 1:
        buttons.append(
            types.InlineKeyboardButton(
                text="▶", callback_data=f"movie_list_{first + 1}"
            )
        )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("↩️ Back To Search Movies"), callback_data="movies"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(text=_("Ⓜ️️ Back To Menu"), callback_data="go")
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("🗑 Delete From Movie List"), callback_data="delete_from_movie_list"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("🎱 Movie Like This"), callback_data="similar_0"
        )
    )

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def menu_():
    buttons = [
        types.InlineKeyboardButton(text=_("🔍 Popular List"), callback_data="popular_0"),
        types.InlineKeyboardButton(text=_("🔍 By Title"), callback_data="title_0"),
        types.InlineKeyboardButton(text=_("🔍 By Criteria"), callback_data="criteria_0"),
        types.InlineKeyboardButton(text=_("Ⓜ Back To Menu"), callback_data="go"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


# Inline buttons for a message with a popular movies.
def popular_movie_buttons(first, popular_list, original_name, movie_id):
    buttons = []
    buttons.append(
        types.InlineKeyboardButton(
            text=_("📺 Trailer YouTube"),
            url=f"https://www.youtube.com/results?search_query=+{original_name}+trailer",
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("ℹ️ More Info On TMDB"),
            url=f"https://www.themoviedb.org/movie/{movie_id}",
        )
    )

    if not first <= 0:
        buttons.append(
            types.InlineKeyboardButton(text="◀", callback_data=f"popular_{first - 1}")
        )

    if not first >= popular_list - 1:
        buttons.append(
            types.InlineKeyboardButton(text="▶", callback_data=f"popular_{first + 1}")
        )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("↩️ Back To Search Movies"), callback_data="movies"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(text=_("Ⓜ️️ Back To Menu"), callback_data="go")
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("📝 Add To Movie List"), callback_data="add_to_movie_list"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("🎱 Movie Like This"), callback_data="similar_0"
        )
    )

    # For The Future
    # buttons.append(
    #     types.InlineKeyboardButton(text=_("Details"), callback_data="movie_details")
    # )

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def similar_movie_keyboard(first, movie_list, original_name, movie_id):
    buttons = []
    buttons.append(
        types.InlineKeyboardButton(
            text=_("📺 Trailer YouTube"),
            url=f"https://www.youtube.com/results?search_query=+{original_name}+trailer",
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("ℹ️ More Info On TMDB"),
            url=f"https://www.themoviedb.org/movie/{movie_id}",
        )
    )

    if not first <= 0:
        buttons.append(
            types.InlineKeyboardButton(text="◀", callback_data=f"similar_{first - 1}")
        )

    if not first >= movie_list - 1:
        buttons.append(
            types.InlineKeyboardButton(text="▶", callback_data=f"similar_{first + 1}")
        )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("↩️ Back To Search Movies"), callback_data="movies"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(text=_("Ⓜ️️ Back To Menu"), callback_data="go")
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("📝 Add To Movie List"), callback_data="add_to_movie_list"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("🎱 Movie Like This"), callback_data="similar_0"
        )
    )

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def title_keyboard():
    buttons = []
    buttons.append(types.InlineKeyboardButton(text=_("Find"), callback_data="find_0"))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


# Inline buttons for a message (find_by_title).
def title_movie_buttons(first, movie_list, original_name, movie_id):
    buttons = []

    buttons.append(
        types.InlineKeyboardButton(
            text=_("📺 Trailer YouTube"),
            url=f"https://www.youtube.com/results?search_query=+{original_name}+trailer",
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("ℹ️ More Info On TMDB"),
            url=f"https://www.themoviedb.org/movie/{movie_id}",
        )
    )

    if not first <= 0:
        buttons.append(
            types.InlineKeyboardButton(text="◀", callback_data=f"find_{first - 1}")
        )

    if not first >= movie_list - 1:
        buttons.append(
            types.InlineKeyboardButton(text="▶", callback_data=f"find_{first + 1}")
        )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("↩️ Back To Search Movies"), callback_data="movies"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(text=_("Ⓜ️️ Back To Menu"), callback_data="go")
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("📝 Add To Movie List"), callback_data="add_to_movie_list"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("🎱 Movie Like This"), callback_data="similar_0"
        )
    )

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def total_keyboard():
    buttons = []
    buttons.append(types.InlineKeyboardButton(text=_("Find"), callback_data="total_0"))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def result_keyboard(first, data, original_name, movie_id):
    buttons = []

    buttons.append(
        types.InlineKeyboardButton(
            text=_("📺 Trailer YouTube"),
            url=f"https://www.youtube.com/results?search_query=+{original_name}+trailer",
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("ℹ️ More Info On TMDB"),
            url=f"https://www.themoviedb.org/movie/{movie_id}",
        )
    )

    if not first <= 0:
        buttons.append(
            types.InlineKeyboardButton(text="◀", callback_data=f"total_{first - 1}")
        )

    if not first >= data - 1:
        buttons.append(
            types.InlineKeyboardButton(text="▶", callback_data=f"total_{first + 1}")
        )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("↩️ Back To Search Movies"), callback_data="movies"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(text=_("Ⓜ️️ Back To Menu"), callback_data="go")
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("📝 Add To Movie List"), callback_data="add_to_movie_list"
        )
    )

    buttons.append(
        types.InlineKeyboardButton(
            text=_("🎱 Movie Like This"), callback_data="similar_0"
        )
    )

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


# genres keyboard
def genres_keyboard():
    buttons = []

    buttons.append(types.InlineKeyboardButton(text=_("Action"), callback_data="28"))
    buttons.append(types.InlineKeyboardButton(text=_("Adventure"), callback_data="12"))
    buttons.append(types.InlineKeyboardButton(text=_("Animation"), callback_data="16"))
    buttons.append(types.InlineKeyboardButton(text=_("Comedy"), callback_data="35"))
    buttons.append(types.InlineKeyboardButton(text=_("Crime"), callback_data="80"))
    buttons.append(
        types.InlineKeyboardButton(text=_("Documentary"), callback_data="99")
    )
    buttons.append(types.InlineKeyboardButton(text=_("Drama"), callback_data="18"))
    buttons.append(types.InlineKeyboardButton(text=_("Family"), callback_data="10751"))
    buttons.append(types.InlineKeyboardButton(text=_("Fantasy"), callback_data="14"))
    buttons.append(types.InlineKeyboardButton(text=_("History"), callback_data="36"))
    buttons.append(types.InlineKeyboardButton(text=_("Horror"), callback_data="27"))
    buttons.append(types.InlineKeyboardButton(text=_("Music"), callback_data="10402"))
    buttons.append(types.InlineKeyboardButton(text=_("Mystery"), callback_data="9648"))
    buttons.append(types.InlineKeyboardButton(text=_("Romance"), callback_data="10749"))
    buttons.append(
        types.InlineKeyboardButton(text=_("Science Fiction"), callback_data="878")
    )
    buttons.append(
        types.InlineKeyboardButton(text=_("TV Movie"), callback_data="10770")
    )
    buttons.append(types.InlineKeyboardButton(text=_("Thriller"), callback_data="53"))
    buttons.append(types.InlineKeyboardButton(text=_("War"), callback_data="10752"))
    buttons.append(types.InlineKeyboardButton(text=_("Western"), callback_data="37"))

    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.insert(
        types.InlineKeyboardButton(
            text=_("↩️ Back To Search Movies"), callback_data="finish"
        )
    )
    keyboard.add(*buttons)

    return keyboard
