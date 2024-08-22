import logging
import os
import requests

from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()

secret_token = os.getenv('TOKEN')

bot = TeleBot(token=secret_token)

logging.basicConfig(
    filename='main.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    encoding='utf-8',
)

URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'


def get_cat_image():
    try:
        response = requests.get(URL_CAT)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = URL_DOG
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_dog_image():
    try:
        response = requests.get(URL_DOG)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = URL_CAT
        response = requests.get(new_url)

    response = response.json()
    random_dog = response[0].get('url')
    return random_dog


# Добавляем хендлер для команды Пришли мне котика!:
@bot.message_handler(func=lambda message: message.text == 'Пришли мне котика!')
def new_cat(message):
    chat = message.chat
    name = message.chat.first_name
    bot.send_photo(chat.id, get_cat_image())
    logging.info(f'Картинка котика отправлена пользователю по имени {name}')


# Добавляем хендлер для команды Пришли мне собачку!:
@bot.message_handler(func=lambda message: message.text == 'Пришли мне собачку!')
def new_dog(message):
    chat = message.chat
    name = message.chat.first_name
    bot.send_photo(chat.id, get_dog_image())
    logging.info(f'Картинка собачки отправлена пользователю по имени {name}')


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаём объект кнопки:
    button_newcat = types.KeyboardButton('Пришли мне котика!')
    button_newdog = types.KeyboardButton('Пришли мне собачку!')
    # Добавляем объект кнопки на клавиатуру:
    keyboard.add(button_newcat)
    keyboard.add(button_newdog)

    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого животного тебе прислать?',
        # Отправляем клавиатуру в сообщении бота: передаём объект клавиатуры
        # в параметр reply_markup объекта send_message.
        # Telegram-клиент "запомнит" клавиатуру и будет отображать её.
        reply_markup=keyboard,
    )


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаём объект кнопки:
    button_newcat = types.KeyboardButton('Пришли мне котика!')
    button_newdog = types.KeyboardButton('Пришли мне собачку!')
    # Добавляем объект кнопки на клавиатуру:
    keyboard.add(button_newcat)
    keyboard.add(button_newdog)
    bot.send_message(
        chat_id=chat_id,
        text='Привет, я Mateo! Я еще не очень общительный, поэтому предпочитаю не отвечать на разные сообщения, хочешь фото котика? Жми на кнопку!',
        reply_markup=keyboard,
        )


def main():
    bot.polling()


if __name__ == '__main__':
    main()
