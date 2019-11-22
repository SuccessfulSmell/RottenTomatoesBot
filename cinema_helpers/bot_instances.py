from aiogram import Bot, Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from configs.config import token
from cinema_helpers.movie_parcer import MovieParser

bot = Bot(token=token)
storage = MemoryStorage()
db = Dispatcher(bot, storage=storage)
vote_cb = CallbackData('vote', 'action')
parser = MovieParser()


class BotCommand:
    start = ['📄info', '&#128196;start', '&#128196;help',
             '/info', '/start', '/help']
    search = ['🔎search', '/search']
    random = ['🎬random', '/random']
    movies = ['🎞movies', '/movies']
    opening_this_week = ['🎥opening this week', '/opening_this_week']
    donate = ['💡donate', '/donate']


class Form(StatesGroup):
    first_name = State()
    last_name = State()
    user_id = State()
    search_item = State()
    movie = State()
