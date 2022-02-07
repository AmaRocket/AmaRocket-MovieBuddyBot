from collections import OrderedDict


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
            id="#️⃣ ID:",
            title="🎞 Movie:",
            release_date="📅 Release date:",
            original_language="🌐 Original language:",
            vote_average="💎 Voteaverage:",
            vote_count="🔄 Vote count:",
            popularity="🍿 Popularity:",
            overview="📜 Overwiew:",
            genre_ids="🎭 Genre id:",
            # poster_path="🏤 Poster path: https://image.tmdb.org/t/p/original"
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

    # @staticmethod
    # def message(movie_list, first):
    #     movie_id = movie_list[first]['id']
    #     genre_ids = movie_list[first]['genre_ids']
    #     original_name = movie_list[first]['title']
    #     original_language = movie_list[first]['original_language']
    #     overview = movie_list[first]['overview']
    #     vote_average = movie_list[first]['vote_average']
    #     vote_count = movie_list[first]['vote_count']
    #     release_date = movie_list[first]['release_date']
    #     popularity = movie_list[first]['popularity']
    #     poster_path = movie_list[first]['poster_path']
    #
    #     text_value = f' #️⃣ ID: {movie_id}\n\n 🎞 Movie: {original_name}\n\n 📅 Release date: {release_date}\n\n' \
    #                  f'🌐 Original languare {original_language}\n\n📜 Overwiew: {overview}\n\n' \
    #                  f'💎 Voteaverage: {vote_average}\n\n' \
    #                  f'🔄 Vote count: {vote_count}\n\n🍿 Popularity: {popularity}\n\n🎭 Genre id: {genre_ids}\n\n ' \
    #                  f'🏤 Poster path: https://image.tmdb.org/t/p/original{poster_path}\n' \
    #                  f'------------------------------------------------------------------------------------------'
    #
    #     return text_value

    # @staticmethod
    # def movie_id(text_value):
    #     movie_id = ((re.findall(r'ID: (\d+)', text_value))[-1])
    #
    #     return movie_id
