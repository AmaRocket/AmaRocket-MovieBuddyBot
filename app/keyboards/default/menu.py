from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# # buttons for criteria choose
# criteria = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text='Genre'),
#             KeyboardButton(text='Vote Average'),
#             KeyboardButton(text='Year'),
#         ],
#         [
#             KeyboardButton(text='Cancel')
#         ],
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True
# )
# #

# # buttons for genres
# genres = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text='Action, 28'),
#             KeyboardButton(text='Adventure, 12'),
#             KeyboardButton(text='Animation, 16'),
#             KeyboardButton(text='Comedy, 35'),
#             KeyboardButton(text='Crime, 80')
#         ],
#         [
#
#             KeyboardButton(text='Documentary, 99'),
#             KeyboardButton(text='Drama, 18'),
#             KeyboardButton(text='Family, 10751'),
#             KeyboardButton(text='Fantasy, 14'),
#             KeyboardButton(text='History, 36')
#         ],
#         [
#
#             KeyboardButton(text='Horror, 27'),
#             KeyboardButton(text='Music, 10402'),
#             KeyboardButton(text='Mystery, 9648'),
#             KeyboardButton(text='Romance, 10749'),
#             KeyboardButton(text='Science Fiction, 878')
#         ],
#         [
#
#             KeyboardButton(text='TV Movie, 10770'),
#             KeyboardButton(text='Thriller, 53'),
#             KeyboardButton(text='War, 10752'),
#             KeyboardButton(text='Western, 37')
#         ],
#         [
#             KeyboardButton(text='Cancel')
#         ],
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True
# )

vote_average = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3'),
            KeyboardButton(text='4'),
            KeyboardButton(text='5'),
            KeyboardButton(text='6'),
            KeyboardButton(text='7'),
            KeyboardButton(text='8'),
            KeyboardButton(text='9')
        ],
        [
            KeyboardButton(text='Cancel')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

totalkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Finish')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
