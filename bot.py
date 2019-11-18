# !/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData

from configs.config import token
from cinema_helpers.movie_parcer import MovieParser

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)
vote_cb = CallbackData('vote', 'action')
parser = MovieParser()


@dp.message_handler(commands=['info', 'start', 'help'])
async def start_info(message: types.Message):
    user_murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_murkup.row('/random', '/films')
    user_murkup.row('/opening_this_week', '/donate')
    user_murkup.row('/info')
    await bot.send_message(message.chat.id, text='Start Info', reply_markup=user_murkup)


@dp.message_handler(commands=['opening_this_week'])
async def opening_this_week(message: types.Message):
    msg = ''
    for movie in parser.get_tomatoes_affiche():
        msg += parser.output_data(movie)
    await bot.send_message(message.chat.id, text=msg, parse_mode='HTML')


@dp.message_handler(commands=['films'])
async def list_of_films(message: types.Message):
    await bot.send_message(message.chat.id, text='This feature is not  available yet...')


@dp.message_handler(commands=['donate'])
async def opening_this_week(message: types.Message):
    await bot.send_message(message.chat.id, text='This feature is not  available yet...')


@dp.message_handler(commands=['random'])
async def random_movie(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton('action', callback_data=vote_cb.new(action='1')),
        types.InlineKeyboardButton('animation', callback_data=vote_cb.new(action='2')),
        types.InlineKeyboardButton('art & foreign', callback_data=vote_cb.new(action='3')),
        types.InlineKeyboardButton('classics', callback_data=vote_cb.new(action='4')),
        types.InlineKeyboardButton('comedy', callback_data=vote_cb.new(action='5')),
        types.InlineKeyboardButton('documentary', callback_data=vote_cb.new(action='6')),
        types.InlineKeyboardButton('drama', callback_data=vote_cb.new(action='7')),
        types.InlineKeyboardButton('horror', callback_data=vote_cb.new(action='8')),
        types.InlineKeyboardButton('kids & family', callback_data=vote_cb.new(action='9')),
        types.InlineKeyboardButton('mystery', callback_data=vote_cb.new(action='10')),
        types.InlineKeyboardButton('romance', callback_data=vote_cb.new(action='11')),
        types.InlineKeyboardButton('sci fi & fantasy', callback_data=vote_cb.new(action='12'))
    )
    keyboard.add(
        types.InlineKeyboardButton('all', callback_data=vote_cb.new(action='13')))
    await bot.send_message(message.chat.id, text='<b>Choose a genre:</b>',
                           parse_mode='HTML', reply_markup=keyboard)


@dp.callback_query_handler(vote_cb.filter(action=[str(index) for index in range(1, 14)]))
async def callback_vote_action(query: types.CallbackQuery, callback_data: dict):
    logging.info('Got this callback data: %r', callback_data)
    await query.answer()
    callback_data_action = callback_data['action']
    message_id = query.message.message_id
    user_id = query.from_user.id
    if callback_data_action == '1':
        msg = parser.get_random_action()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '2':
        msg = parser.get_random_animation()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '3':
        msg = parser.get_random_art_and_foreign()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '4':
        msg = parser.get_random_classics()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '5':
        msg = parser.get_random_comedy()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '6':
        msg = parser.get_random_documentary()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '7':
        msg = parser.get_random_drama()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '8':
        msg = parser.get_random_horror()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '9':
        msg = parser.get_random_kids_and_family()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '10':
        msg = parser.get_random_mystery()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '11':
        msg = parser.get_random_romance()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '12':
        msg = parser.get_random_sci_fi_and_fantasy()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')
    elif callback_data_action == '13':
        msg = parser.get_random_genre_movie()
        await bot.edit_message_text(msg, user_id, message_id, parse_mode='HTML')


@dp.message_handler(content_types=['text'])
async def search(message: types.Message):
    if message:
        search_result = parser.tomatoes_search(message.text).get('movies', '')
        if search_result:
            msg = '<b>Search results:</b>\n\n'
            for result in search_result:
                msg += f'\n<b>&#127813;{result.get("name", "")}</b>' \
                       f'\n{parser.base_url}{result.get("url", "")}\n'
            await bot.send_message(message.chat.id, text=msg, parse_mode='HTML')
        else:
            msg = f'No results were found for "{message.text}" request . Sorry...'
            await bot.send_message(message.chat.id, text=msg, parse_mode='HTML')


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as err:
        logging.warning(err)
