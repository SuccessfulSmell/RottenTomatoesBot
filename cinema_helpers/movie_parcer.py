from random import randint
from rotten_tomatoes_client import RottenTomatoesClient
from rotten_tomatoes_client.query import MovieBrowsingQuery
from rotten_tomatoes_client.query.parameters.browsing import Genre, MovieBrowsingCategory


class MovieParser:
    @property
    def base_url(self):
        return 'https://www.rottentomatoes.com/'

    @staticmethod
    def tomatoes_search(movie_name: str) -> dict:
        """ Get searching data from rotten tomatoes.

        :param movie_name: name of movie.
        :return:           result of searching.
        """
        return RottenTomatoesClient.search(term=movie_name)

    @staticmethod
    def get_tomatoes_affiche() -> dict:
        """ Get last premieres from rotten tomatoes.
        
        :return: dict with premieres.
        """
        query = MovieBrowsingQuery(minimum_rating=80, maximum_rating=100,
                                   category=MovieBrowsingCategory.opening_in_theaters)
        return RottenTomatoesClient.browse_movies(query=query).get('results', '')

    @staticmethod
    def _get_random_movie(genre=None) -> dict:
        """ Get random movie from list by genre.
        
        :param genre: genre of movie.
        :return:      data for random movie.
        """
        if genre:
            genre = [genre]
        query = MovieBrowsingQuery(minimum_rating=80, maximum_rating=100,
                                   genres=genre,
                                   category=MovieBrowsingCategory.all_dvd_and_streaming)
        movies = RottenTomatoesClient.browse_movies(query=query).get('results', '')
        index = randint(0, len(movies) - 1)
        return movies[index]

    def output_data(self, movie: dict) -> str:
        """ Generate a simple html report from dict.
        
        :param movie: dict of movie data.
        :return:      html report.
        """
        url = f'{self.base_url}{movie.get("url", "")}'
        actors = str([actor for actor in movie.get("actors", "")])
        for symbol in ("]", "[", "'"):
            actors = actors.replace(symbol, "")
        return f'<b>&#127813; {movie.get("title", "")}</b>\n\n' \
               f'<b>Score: </b>{movie.get("tomatoScore", "")}\n' \
               f'<b>Theater Release Date: </b>{movie.get("theaterReleaseDate", "")}\n' \
               f'<b>DVD Release Date: </b>{movie.get("dvdReleaseDate", "")}\n' \
               f'<b>Runtime: </b>{movie.get("runtime", "")}\n' \
               f'<b>Actors: </b>{actors}\n\n' \
               f'<a href="{url}">MoreInfo»</a>\n\n'

    def get_random_action(self) -> str:
        """ Get random action movie from rotten tomatoes.
        
        :return: html report.
        """
        movie = self._get_random_movie(Genre.action)
        return self.output_data(movie)

    def get_random_animation(self) -> str:
        """ Get random animation movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.animation)
        return self.output_data(movie)

    def get_random_art_and_foreign(self) -> str:
        """ Get random art & foreign movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.art_and_foreign)
        return self.output_data(movie)

    def get_random_classics(self) -> str:
        """ Get random classic movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.classics)
        return self.output_data(movie)

    def get_random_documentary(self) -> str:
        """ Get random documentary movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.documentary)
        return self.output_data(movie)

    def get_random_drama(self) -> str:
        """ Get random drama movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.drama)
        return self.output_data(movie)

    def get_random_horror(self) -> str:
        """ Get random horror movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.horror)
        return self.output_data(movie)

    def get_random_kids_and_family(self) -> str:
        """ Get random movie for all family from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.kids_and_family)
        return self.output_data(movie)

    def get_random_mystery(self) -> str:
        """ Get random mystery movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.mystery)
        return self.output_data(movie)

    def get_random_romance(self) -> str:
        """ Get random romance movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.romance)
        return self.output_data(movie)

    def get_random_sci_fi_and_fantasy(self) -> str:
        """ Get random fantasy movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.sci_fi_and_fantasy)
        return self.output_data(movie)

    def get_random_comedy(self) -> str:
        """ Get random comedy movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie(Genre.comedy)
        return self.output_data(movie)

    def get_random_genre_movie(self) -> str:
        """ Get random movie from rotten tomatoes.

        :return: html report.
        """
        movie = self._get_random_movie()
        return self.output_data(movie)
