from tmdbv3api import Discover, Movie, TMDb

from config import API_KEY
from language_middleware import get_lang


class TheMovie(TMDb):
    """
    Class TMDB for searching movies in TMDBapi library
    with custom changing library request language  for current user.
    """

    def __init__(self, language, obj_cached=True, session=None):
        super().__init__(obj_cached, session)
        self.language = language
        self.api_key = API_KEY

    movie = Movie()
    discover = Discover()


async def get_api_for_context(context):
    language = await get_lang(context) or "en"
    return TheMovie(language)
