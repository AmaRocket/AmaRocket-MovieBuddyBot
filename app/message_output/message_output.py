import re


class MessageText:
    """
    this class made for outputting info
    about movie from tmdbv3api.
    """

    @staticmethod
    def message(movie_list, first):
        movie_id = movie_list[first]['id']
        genre_ids = movie_list[first]['genre_ids']
        original_name = movie_list[first]['title']
        original_language = movie_list[first]['original_language']
        overview = movie_list[first]['overview']
        vote_average = movie_list[first]['vote_average']
        vote_count = movie_list[first]['vote_count']
        release_date = movie_list[first]['release_date']
        popularity = movie_list[first]['popularity']
        poster_path = movie_list[first]['poster_path']

        text_value = f' ID: {movie_id}\n Movie: {original_name}\n Release date: {release_date}\n Genre id: {genre_ids}\n' \
                     f' Original languare {original_language}\n Overwiew: {overview}\n Voteaverage: {vote_average}\n' \
                     f' Vote count: {vote_count}\n Popularity: {popularity}\n Genre id: {genre_ids}\n ' \
                     f' Poster path: https://image.tmdb.org/t/p/original{poster_path}\n' \
                     f'------------------------------------------------------------------------------------------'

        return text_value

    @staticmethod
    def original_title(text_value):
        original_name = ((re.findall(r'Movie: (.+)', text_value))[-1])

        return original_name

    @staticmethod
    def movie_id(text_value):
        movie_id = ((re.findall(r'ID: (\d+)', text_value))[-1])

        return movie_id
