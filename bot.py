# !/usr/bin/python
# -*- coding: utf-8 -*-
from aiogram import executor, types
from aiogram.dispatcher.storage import FSMContext

from configs.text_info import *
from cinema_helpers.logger import logger
from cinema_helpers.bot_instances import BotCommand, Form, parser, db, vote_cb


@db.message_handler(text=BotCommand.start)
async def start_info(message: types.Message):
    user_murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_murkup.row(BotCommand.random[0], BotCommand.search[0])
    user_murkup.row(BotCommand.opening_this_week[0], BotCommand.movies[0])
    user_murkup.row(BotCommand.start[0], BotCommand.donate[0])
    await message.answer(text=START_INFO, reply_markup=user_murkup, parse_mode='HTML')


@db.message_handler(text=BotCommand.opening_this_week)
async def opening_this_week(message: types.Message):
    msg = ''
    for movie in parser.get_tomatoes_affiche():
        msg += parser.output_data(movie)
    await message.answer(text=msg, parse_mode='HTML')


@db.message_handler(text=BotCommand.movies)
async def list_of_films(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('add at list',
                                            callback_data=vote_cb.new(action='add')))
    keyboard.add(types.InlineKeyboardButton('delete from list',
                                            callback_data=vote_cb.new(action='del')))
    await message.answer(text=EMPTY_LIST_MSG, reply_markup=keyboard)
    await message.answer(text=NO_WORK_FEATURE_MSG)


@db.message_handler(text=BotCommand.donate)
async def donate(message: types.Message):
    await message.answer(text=NO_WORK_FEATURE_MSG)


@db.message_handler(text=BotCommand.random)
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
    keyboard.add(types.InlineKeyboardButton('all', callback_data=vote_cb.new(action='13')))
    await message.answer(text=GENRE_CHOOSE, parse_mode='HTML', reply_markup=keyboard)


@db.callback_query_handler(vote_cb.filter(action=[str(index) for index in range(1, 14)]))
async def callback_vote_action(query: types.CallbackQuery, callback_data: dict):
    logger.info('Got callback data: %r', callback_data)
    await query.answer()
    callback_data_action = callback_data['action']
    if callback_data_action == '1':
        msg = parser.get_random_action()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '2':
        msg = parser.get_random_animation()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '3':
        msg = parser.get_random_art_and_foreign()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '4':
        msg = parser.get_random_classics()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '5':
        msg = parser.get_random_comedy()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '6':
        msg = parser.get_random_documentary()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '7':
        msg = parser.get_random_drama()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '8':
        msg = parser.get_random_horror()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '9':
        msg = parser.get_random_kids_and_family()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '10':
        msg = parser.get_random_mystery()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '11':
        msg = parser.get_random_romance()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '12':
        msg = parser.get_random_sci_fi_and_fantasy()
        await query.message.answer(msg, parse_mode='HTML')
    elif callback_data_action == '13':
        msg = parser.get_random_genre_movie()
        await query.message.answer(text=msg, parse_mode='HTML')


@db.message_handler(text=BotCommand.search)
async def search(message: types.Message):
    await Form.search_item.set()
    await message.answer(text=SEARCH_MSG)


@db.message_handler(state=Form.search_item)
async def get_search(message: types.Message, state: FSMContext):
    if message.text:
        search_result = parser.tomatoes_search(message.text).get('movies')
        if search_result:
            msg = SEARCH_FOR.format(message.text)
            for result in search_result:
                url = f'{parser.base_url}{result.get("url", "")}'
                movie = result.get("name", "")
                msg += SEARCH_RESULT.format(movie, url)
            await message.answer(msg, parse_mode='HTML')
        else:
            await message.answer(text=NO_SEARCH_RESULTS.format(message.text))
    await state.finish()


if __name__ == '__main__':
    try:
        executor.start_polling(db, skip_updates=True)
    except Exception as err:
        logger.warning(err)
