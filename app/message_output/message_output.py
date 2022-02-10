from collections import OrderedDict

from loader import _


class MessageText:
    """
    this class made for outputting info
    about movie from tmdbv3api.
    """

    def __init__(self, movie_dict):
        self.__movie_dict = movie_dict

    @property
    def message(self):
        field = OrderedDict(
            id=_("<b>#️⃣ ID: </b>"),
            title=_("<b>🎞 Movie: </b>"),
            release_date=_("<b>📅 Release date: </b>"),
            original_language=_("<b>🌐 Original language: </b>"),
            vote_average=_("<b>💎 Voteaverage: </b>"),
            vote_count=_("<b>🔄 Vote count: </b>"),
            popularity=_("<b>🍿 Popularity: </b>"),
            overview=_("<b>📜 Overwiew: </b>"),
        )
        text_value = ""
        for key, title in field.items():
            text_value += f"{title} {self.__movie_dict[key]}\n\n"
        return text_value

    @property
    def original_title(self):
        return self.__movie_dict["title"]

    @property
    def movie_id(self):
        return int(self.__movie_dict["id"])

    @property
    def movie_image(self):
        return self.__movie_dict["poster_path"]
