import requests

from config import api_key


# https://api.themoviedb.org/3/movie/76341?api_key=36e581515b6f8ef06c571d0ef6a2327a


# v3 search movies list
# search movies by genre etc
def search_by_year_genre(genre, release_year, api_key):
    try:

        api_version = 3
        api_base_url = f'https://api.themoviedb.org/{api_version}'
        endpoint_path = f'/discover/movie'
        endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}&sort_by=popularity.desc&include_video=true&primary_release_year={release_year}&page=1&with_genres={genre}'
        print(endpoint)
        print('---------------------------------------------------------------------------------------')
        r = requests.get(endpoint)
        data = r.json()
        # pprint.pprint(data)

        for info in data['results']:
            id = info['id']
            genre_ids = info['genre_ids']
            original_name = info['original_title']
            original_language = info['original_language']
            overview = info['overview']
            vote_average = info['vote_average']
            vote_count = info['vote_count']
            release_date = info['release_date']
            popularity = info['popularity']
            poster_path = info['poster_path']
            print(
                f' Movie: {original_name}\n movie_id: {id}\n genre id: {genre_ids}\n'
                f' original languare {original_language}\n overwiew: {overview}\n '
                f'voteaverage: {vote_average}\n vote count: {vote_count}\n '
                f'release date: {release_date}\n popularity: {popularity}\n '
                f'poster path: https://www.themoviedb.org/t/p/original{poster_path}\n'
                f'------------------------------------------------------------------------------------------')

    except Exception as ex:
        print(ex)
        print('Check Your Enter!')
        print('---------------------------------------------------------------------------------------')


def main():
    release_year = input('Release Year: ')
    genre = input('Genre: ')
    search_by_year_genre(genre, release_year, api_key)


if __name__ == '__main__':
    main()

# using v3 api
# search movie by id
# movie_id = 12
# api_version = 3
# api_base_url = f'https://api.themoviedb.org/{api_version}'
# endpoint_path = f'/movie/{movie_id}'
# endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}'
# print(endpoint)
#
# r = requests.get(endpoint)
#
# print(r.status_code)
# pprint.pprint(r.text)
print('---------------------------------------------------------------------------------------')

'''
# using v4 api

movie_id = 501
api_version = 4
api_base_url = f'https://api.themoviedb.org/{api_version}'
endpoint_path = f'/movie/{movie_id}'
endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}'
headers = {
    'Authorization': f'Bearer {api_key_v4} ',
    'Content-Type': 'application/json; charset=utf-8'
}

r = requests.get(endpoint, headers=headers)

print(r.status_code)
print(r.text)
'''

"""
# v3 search movies list
# search movies by name
movie_name = input('Name of movie: ')
api_base_url = f'https://api.themoviedb.org/{api_version}'
endpoint_path = f'/search/movie'
endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}&query={movie_name}'
print(endpoint)
print('---------------------------------------------------------------------------------------')
r = requests.get(endpoint)
pprint.pprint(r.json())
print('---------------------------------------------------------------------------------------')



# v3 search movies list
# search movies by keyword
keyword = input('KeyWord: ')
api_base_url = f'https://api.themoviedb.org/{api_version}'
endpoint_path = f'/search/keyword'
endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}&query={keyword}'
print(endpoint)
print('---------------------------------------------------------------------------------------')
r = requests.get(endpoint)
pprint.pprint(r.json())
print('---------------------------------------------------------------------------------------')

"""

# v3 search movies list
# movies genre list
# api_version = 3
# api_base_url = f'https://api.themoviedb.org/{api_version}'
# endpoint_path = f'/genre/movie/list'
# endpoint = f'{api_base_url}{endpoint_path}?api_key={api_key}'
# print(endpoint)
# print('---------------------------------------------------------------------------------------')
# r = requests.get(endpoint)
# pprint.pprint(r.json())
# print('---------------------------------------------------------------------------------------')
#
