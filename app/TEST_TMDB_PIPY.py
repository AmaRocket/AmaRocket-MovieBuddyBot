from tmdbv3api import TMDb, Discover
from tmdbv3api import Movie
from config import API_KEY




# Popular Movies List
def popular_movie():
    tmdb = TMDb()
    tmdb.api_key = API_KEY

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
    tmdb.api_key = API_KEY

    tmdb.language = 'en'
    tmdb.debug = True

    movie = Movie()
    search = movie.search(f'{name}')
    movie_list = []
    for res in search:
        movie_list.append(res)
    return movie_list


# Search Movie by criteria

# genre = 'action'
# voteaverage = '5'
# year = '2000'

def find_by_criteria(genre,voteaverage, year):
    tmdb = TMDb()
    tmdb.api_key = API_KEY

    tmdb.language = 'ru'
    tmdb.debug = True

    discover = Discover()
    movie = discover.discover_movies({
        'sort_by': 'popularity.desc',
        'with_genres': f'{genre}',
        'vote_average.gte': f'{voteaverage}',
        'primary_release_year': f'{year}'
    })
    movie_list = []
    for i in movie:
        movie_list.append(i)

    return movie_list

# .print(find_by_criteria(genre, voteaverage, year))

