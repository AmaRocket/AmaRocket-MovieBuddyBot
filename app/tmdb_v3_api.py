from tmdbv3api import Discover, Movie, TMDb

from config import API_KEY


class TheMovie(TMDb):
    """
    Class TMDB for searching movies in TMDBapi library
    """

    tmdb = TMDb()
    tmdb.api_key = API_KEY

    tmdb.language = "en"
    tmdb.debug = True

    movie = Movie()
    discover = Discover()


d = TheMovie.movie.details(movie_id=603)
print(d)
