from tmdbv3api import TMDb
from tmdbv3api import Movie
from config import api_key




# Popular Movies List
def popular_movie():
    tmdb = TMDb()
    tmdb.api_key = api_key

    tmdb.language = 'en'
    tmdb.debug = True
    movie = Movie()

    popular = movie.popular()
    popular_list = []
    for p in popular:
        popular_list.append(p)
    return(popular_list)




# Search for movies by title
def find_by_name(name):
    tmdb = TMDb()
    tmdb.api_key = api_key

    tmdb.language = 'en'
    tmdb.debug = True

    movie = Movie()
    search = movie.search(f'{name}')
    movie_list = []
    for res in search:
        movie_list.append(res)
    return movie_list

