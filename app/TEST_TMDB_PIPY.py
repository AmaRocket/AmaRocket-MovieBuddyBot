from tmdbv3api import TMDb, Discover, Movie

from config import API_KEY



class TheMovie(TMDb):
    """
    Class TMDB for searching movies in TMDBapi library
    """
    tmdb = TMDb()
    tmdb.api_key = API_KEY

    tmdb.language = 'en'
    tmdb.debug = True

    movie = Movie()
    discover = Discover()



# a = TheMovie()
#
# people = a.movie.details(1488)
# print(people['genres'])
# print(people)