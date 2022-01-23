from tmdbv3api import TMDb, Discover
from tmdbv3api import Movie
from config import API_KEY



class Tmdb(TMDb):
    """
    Class TMDB for searching movies in TMDBapi library
    """


    # Popular Movies List
    def popular_movie(self):
        tmdb = TMDb()
        tmdb.api_key = API_KEY

        tmdb.language = 'en'
        tmdb.debug = True
        movie = Movie()

        popular = movie.popular()
        self.popular_list = []
        for p in popular:
            self.popular_list.append(p)
        return self.popular_list




    # Search for movies by title
    def find_by_name(self, name):
        tmdb = TMDb()
        tmdb.api_key = API_KEY

        tmdb.language = 'en'
        tmdb.debug = True

        movie = Movie()
        search = movie.search(f'{name}')
        self.movie_list = []
        for res in search:
            self.movie_list.append(res)
        return self.movie_list


    # Search Movie by criteria
    def find_by_criteria(self, genre, voteaverage, year):
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
        self.movie_list = []
        for i in movie:
            self.movie_list.append(i)

        return self.movie_list


