import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType, Message
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, input_file, user

from read import get_image, get_books, get_script_dir, delete_image


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
states = ['home','search','open','read']
bot = Bot(token='TOKEN')
reader = Dispatcher(bot)
users = {}
just_choice_book = ReplyKeyboardMarkup(resize_keyboard=True)
just_choice_book.add(KeyboardButton('Выбрать книгу 📚'))
in_home = ReplyKeyboardMarkup(resize_keyboard=True)
in_home.add(KeyboardButton('В начало ⬆️'))
page_book = ReplyKeyboardMarkup(resize_keyboard=True)
page_book.add(KeyboardButton('Назад ⬅️'))
page_book.add(KeyboardButton('В начало ⬆️'))
page_book.add(KeyboardButton('Вперед ➡️'))



@reader.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {}
        await message.reply("Привет!\nЯ создан для чтения книг!\nДавай для начала выберем книгу для чтения :)", reply_markup=just_choice_book)

@reader.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")

@reader.message_handler(content_types=ContentType.TEXT)
async def choice_book(message: types.Message):
    if message.text == 'В начало ⬆️':
        users[message.from_user.id] = {}
        users[message.from_user.id]['state'] = 'home'

        await message.reply("Привет!\nЯ создан для чтения книг!\nДавай для начала выберем книгу для чтения :)", reply_markup=just_choice_book)

    if message.text == 'Выбрать книгу 📚':
        if message.from_user.id not in users:
            users[message.from_user.id] = {}
        users[message.from_user.id]['state'] = 'search'
        for book in get_books():
            await bot.send_message(message.from_user.id, str(book), reply_markup=in_home)
        await bot.send_message(message.from_user.id, 'Пожалуйста, напиши название книги')
    
    if users[message.from_user.id]['state'] == 'open':
        try:
            if get_image(users[message.from_user.id]['book'], int(message.text)) != None:
                users[message.from_user.id]['page'] = int(message.text)
                users[message.from_user.id]['state'] = 'read'
                logging.info('Закинул данные в словарь')
                file = get_script_dir() + '/images/{}{}.jpg'.format(users[message.from_user.id]['book'], users[message.from_user.id]['page'])
                photo = open(file, 'rb')
                logging.info('Открыл файл')
                await bot.send_photo(message.from_user.id, photo, reply_markup=page_book)
                logging.info('Отправил фото')
                delete_image(file)
                logging.info('Удалил файл')
        except:
            await bot.send_message(message.from_user.id, 'Не удалось найти эту страницу')
    
    if users[message.from_user.id]['state'] == 'read' and message.text == 'Вперед ➡️':
        users[message.from_user.id]['page'] += 1
        if get_image(users[message.from_user.id]['book'], users[message.from_user.id]['page']):
            file = get_script_dir() + '/images/{}{}.jpg'.format(users[message.from_user.id]['book'], users[message.from_user.id]['page'])
            photo = open(file, 'rb')
            await bot.send_photo(message.from_user.id, photo, reply_markup=page_book)
            delete_image(file)
    
    if users[message.from_user.id]['state'] == 'read' and message.text == 'Назад ⬅️':
        users[message.from_user.id]['page'] -= 1
        if get_image(users[message.from_user.id]['book'], users[message.from_user.id]['page']):
            file = get_script_dir() + '/images/{}{}.jpg'.format(users[message.from_user.id]['book'], users[message.from_user.id]['page'])
            photo = open(file, 'rb')
            await bot.send_photo(message.from_user.id, photo, reply_markup=page_book)
            delete_image(file)

    if users[message.from_user.id]['state'] == 'search':
        if message.text in get_books():
            users[message.from_user.id]['book'] = message.text[:-4]
            await bot.send_message(message.from_user.id, 'Пожалуйста, укажи номер страницы')
            users[message.from_user.id]['state'] = 'open'

    if users[message.from_user.id]['state'] == 'read' and message.text == 'В начало ⬆️':
        choice_book(message=message)

if __name__ == '__main__':
    executor.start_polling(reader)