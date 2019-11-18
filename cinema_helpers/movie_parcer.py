import os
import yaml
import logging

from random import randint
from rotten_tomatoes_client import RottenTomatoesClient
from rotten_tomatoes_client.query import MovieBrowsingQuery
from rotten_tomatoes_client.query.parameters.browsing import Genre, MovieBrowsingCategory

from configs.config import USERS


# ToDo: Create a normal DB.
class MovieParser:
    @property
    def base_url(self):
        return 'https://www.rottentomatoes.com/'

    @staticmethod
    def get_config() -> dict:
        """ Get data from .yaml config file.

        :return: dict with data.
        """
        filename = USERS
        if not os.path.exists(filename):
            logging.info(f'No such file or directory:{filename}')
        else:
            with open(filename) as file:
                config = yaml.safe_load(file)
            return config

    @staticmethod
    def __change_config(data) -> dict:
        """ Change data in .yaml config file.

        :param data: new data to write in config.
        :return:     dict with data.
        """
        filename = USERS
        if not os.path.exists(filename):
            logging.info(f'No such file or directory:{filename}')
        else:
            with open(filename, 'w') as outfile:
                yaml.dump(data, outfile)
            return data

    @staticmethod
    def tomatoes_search(movie_name: str) -> dict:
        """ Get searching data from rotten tomatoes.

        :param movie_name: name of film.
        :return:           result of searching.
        """
        return RottenTomatoesClient.search(term=movie_name)

    @staticmethod
    def get_tomatoes_affiche():
        query = MovieBrowsingQuery(minimum_rating=80, maximum_rating=100,
                                   category=MovieBrowsingCategory.opening_in_theaters)
        return RottenTomatoesClient.browse_movies(query=query).get('results', '')

    @staticmethod
    def _get_random_movie(genre=None):
        if genre:
            genre = [genre]
        query = MovieBrowsingQuery(minimum_rating=80, maximum_rating=100,
                                   genres=genre,
                                   category=MovieBrowsingCategory.all_dvd_and_streaming)
        movies = RottenTomatoesClient.browse_movies(query=query).get('results', '')
        index = randint(0, len(movies) - 1)
        return movies[index]

    def output_data(self, movie: dict) -> str:
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

    def add_movie_at_list(self, chat_id: int, movie: str):
        user_ids = self.get_config()
        if chat_id in user_ids:
            if movie not in user_ids.get(chat_id, list):
                user_ids[chat_id].append(movie)
                self.__change_config(user_ids)
                return user_ids
            else:
                logging.info(f'Movie "{movie}" is already in the {chat_id} list')
        else:
            logging.info(f'No user with chat_id={chat_id}')

    def remove_movie_from_list(self, chat_id: int, movie_id: int):
        user_ids = self.get_config()
        if chat_id in user_ids:
            if movie_id <= len(user_ids.get(chat_id, list)):
                user_ids[chat_id].pop(movie_id)
                self.__change_config(user_ids)
                return user_ids
            else:
                logging.info(f'No "{movie_id}" in {chat_id} list')
        else:
            logging.info(f'No user with chat_id={chat_id}')

    def add_user_at_list(self, chat_id: int):
        user_ids = self.get_config()
        if chat_id in user_ids:
            logging.info(f'The user with chat_id={chat_id} is already in the list.')
        else:
            user_ids[chat_id] = [None]
            self.__change_config(user_ids)
            return user_ids

    def get_random_action(self) -> str:
        movie = self._get_random_movie(Genre.action)
        return self.output_data(movie)

    def get_random_animation(self) -> str:
        movie = self._get_random_movie(Genre.animation)
        return self.output_data(movie)

    def get_random_art_and_foreign(self) -> str:
        movie = self._get_random_movie(Genre.art_and_foreign)
        return self.output_data(movie)

    def get_random_classics(self) -> str:
        movie = self._get_random_movie(Genre.classics)
        return self.output_data(movie)

    def get_random_documentary(self) -> str:
        movie = self._get_random_movie(Genre.documentary)
        return self.output_data(movie)

    def get_random_drama(self) -> str:
        movie = self._get_random_movie(Genre.drama)
        return self.output_data(movie)

    def get_random_horror(self) -> str:
        movie = self._get_random_movie(Genre.horror)
        return self.output_data(movie)

    def get_random_kids_and_family(self) -> str:
        movie = self._get_random_movie(Genre.kids_and_family)
        return self.output_data(movie)

    def get_random_mystery(self) -> str:
        movie = self._get_random_movie(Genre.mystery)
        return self.output_data(movie)

    def get_random_romance(self) -> str:
        movie = self._get_random_movie(Genre.romance)
        return self.output_data(movie)

    def get_random_sci_fi_and_fantasy(self) -> str:
        movie = self._get_random_movie(Genre.sci_fi_and_fantasy)
        return self.output_data(movie)

    def get_random_comdedy(self) -> str:
        movie = self._get_random_movie(Genre.comedy)
        return self.output_data(movie)

    def get_random_genre_movie(self) -> str:
        movie = self._get_random_movie()
        return self.output_data(movie)

