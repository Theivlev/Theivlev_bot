import os
import random

from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater)
import requests

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)

command_descriptions = {
    'Команда /my_hobby': ' Пост о моём главном увлечении',
    'Отправка сообщения «Селфи»': ' Пришлю вам мое последнее селфи',
    'Отправка сообщения «Школа»': ' Пришлю вам мое фото со школьных времен',
    'Отправка сообщения «Котопёс»': 'Пришлю вам фото котика или собачки',
    'Команда /gpt_voice': ' Объясняю своей бабушке, что такое GPT',
    'Команда /sql_vs_nosql_voice': ' Отличие SQL от NoSQL',
    'Команда /first_love_voice': ' История первой любви',
    'Команда /my_code': 'Ссылка на исходный код телеграмм бота'
}


URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'
AUDIO_DIR = 'media'


def get_new_image() -> str:
    """Отправка изображения (котик или пёс)"""
    URL = random.choice([URL_CAT, URL_DOG])
    response = requests.get(URL).json()
    random_image = response[0].get('url')
    return random_image


def start(update: Update, context: CallbackContext) -> None:
    """Старт работы бота"""
    chat = update.effective_chat
    name = update.message.chat.first_name
    reply_keyboard = [
        ['/info'],
        ['/my_hobby'],
        ['/sql_vs_nosql_voice', '/gpt_voice', '/first_love_voice'],
        ['/my_code'],
        ]

    button = ReplyKeyboardMarkup(
        reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
        )

    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что включили меня, {name}! \nВведи команду /info, '
        'чтобы увидеть, что я умею.',
        reply_markup=button
        )


def handle_action(update: Update, context: CallbackContext, text: str) -> None:
    "Отправка соотвествующего сообщения после действия, возврат кнопок"
    chat = update.effective_chat

    reply_keyboard = [
        ['/info'],
        ['/my_hobby'],
        ['/sql_vs_nosql_voice', '/gpt_voice', '/first_love_voice'],
        ['/my_code'],
        ]

    button = ReplyKeyboardMarkup(
        reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
        )

    context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=button
        )


def info(update: Update, context: CallbackContext) -> None:
    """Выводит информацию о возможностях бота"""
    command_info = ''
    for command, description in command_descriptions.items():
        command_info += f'{command}: {description}\n'

    update.message.reply_text(command_info)


def send_audio(
        update: Update,
        context: CallbackContext,
        path: str,
        caption: str) -> None:
    """Функция для голосовых сообщений"""
    chat_id = update.effective_chat.id
    audio_file = open(path, 'rb')
    context.bot.send_audio(chat_id=chat_id, audio=audio_file, caption=caption)


def gpt_voice(update: Update, context: CallbackContext) -> None:
    """Отправка голосового сообщения «gpt»"""
    path = os.path.join(AUDIO_DIR, 'gpt_voice.ogg')
    caption = "Объясняю своей бабушке, что такое GPT"
    send_audio(update, context, path, caption)


def sql_vs_nosql_voice(update: Update, context: CallbackContext) -> None:
    """Отправка голосового сообщения «Отличия SQL от NoSQL»"""
    path = os.path.join(AUDIO_DIR, 'sql_vs_nosql_voice.ogg')
    caption = "Отличия SQL от NoSQL"
    send_audio(update, context, path, caption)


def first_love_voice(update: Update, context: CallbackContext) -> None:
    """Отправка голосового сообщения «История первой любви»"""
    path = os.path.join(AUDIO_DIR, 'first_love.ogg')
    caption = "Сказочная история первой любви"
    send_audio(update, context, path, caption)


def my_hobby(update: Update, context: CallbackContext) -> None:
    """Отправка поста о главном увлечении"""
    chat = update.effective_chat
    with open('media/my_hobby.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    bot.send_message(chat_id=chat.id, text=text)
    context.bot.send_photo(
            chat_id=chat.id,
            photo=open('media/achievement.jpg', 'rb')
        )


def my_code(update: Update, context: CallbackContext) -> None:
    """Отправляет ссылку на исходный код бота"""
    update.message.reply_text(
        'Исходный код доступен по ссылке: '
        'https://github.com/Theivlev/Theivlev_bot.git')


def photo(update: Update, context: CallbackContext) -> None:
    """Отправка фото"""
    chat = update.effective_chat
    text = update.message.text.lower()
    phrases = [
        "Милый питомец",
        "Прекрасный питомец",
        "Красивый малыш",
        "Интересный друг",
        "Восхитительное создание",
        "Уникальное создание",
        ]
    if text == 'селфи':
        text = 'Моё последнее селфи'
        context.bot.send_photo(
            chat_id=chat.id,
            photo=open('media/selfie.jpg', 'rb')
        )
        handle_action(update, context, text)

    elif text == 'школа':
        text = 'Мое школьное фото'
        context.bot.send_photo(
            chat_id=chat.id,
            photo=open('media/school.jpg', 'rb')
        )
        handle_action(update, context, text)

    elif text == 'котопес' or text == 'котопёс':
        text = random.choice(phrases)
        context.bot.send_photo(chat.id, get_new_image())
        handle_action(update, context, text)

    else:
        text = ('Отправте сообщение «Селфи» и '
                'я отправлю вам свое последнее селфи. '
                '\nОтправте сообщение «Школа» и '
                'вам будет доступно мое фото из '
                'школьных времен.'
                '\nОтправте сообщение «Котопёс» '
                'и пришлю вам котика или собачку')
        handle_action(update, context, text)


def main():
    commands = [
        ('start', start),
        ('info', info),
        ('gpt_voice', gpt_voice),
        ('sql_vs_nosql_voice', sql_vs_nosql_voice),
        ('first_love_voice', first_love_voice),
        ('my_code', my_code),
        ('my_hobby', my_hobby),
    ]

    for command, handler in commands:
        updater.dispatcher.add_handler(CommandHandler(command, handler))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, photo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
