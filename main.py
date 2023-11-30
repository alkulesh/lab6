import webbrowser
import telebot
import requests
import json
import sqlite3
from telebot import types
import io
bot = telebot.TeleBot('6859663935:AAEBkscawdVK0vSvE3AMCdjv_kuKj173dy0')
API = '38480ae0394c728eec9bed273c563762'
conn = sqlite3.connect('weather_bot.sql')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, first_name TEXT, last_name TEXT, chat_id INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS cities (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, city_name TEXT)''')
conn.commit()
conn.close()

conn = sqlite3.connect('weather_bot.sql')
cursor = conn.cursor()
def add_user(user_id, first_name, last_name, chat_id):
    cursor.execute("INSERT INTO users (user_id, first_name, last_name, chat_id) VALUES (?,?,?,?)",
                   (user_id, first_name, last_name, chat_id))

    conn.commit()
def add_city(user_id,city_name):
    cursor.execute("INSERT INTO cities(user_id,city_name) VALUES (?, ?)",(user_id,city_name))
    conn.commit()
def get_all_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
def get_all_cities():
    cursor.execute("SELECT city_name FROM cities WHERE user_id=?", (user_id,))
    return cursor.fetchall()
conn.close()
def create_keyboard():
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Минск'))
    markup.add(types.KeyboardButton('Москва'))
    markup.add(types.KeyboardButton('Питер'))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот Погода! \nНапиши название города!', reply_markup=create_keyboard())
@bot.message_handler(commands=['help'])
def on_help(message):
    bot.send_message(message.chat.id,'Введите название города, для которого хотите узнать погоду!', reply_markup=create_keyboard())
@bot.message_handler(commands=['weather'])
def on_we(message):
    bot.send_message(message.chat.id, 'Нажмите на ссылку, чтобы перейти на сайт погоды: https://yandex.by/pogoda/')
@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code==200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        im = data["weather"][0]["main"]
        bot.reply_to(message, f'Сейчас температура: {temp} градусов')
        if im == "Snow":
            image = 'снегг.png'
            bot.send_message(message.chat.id, 'Снежная погода!')
        elif im == "Clear":
            image = 'солнце.jpg'
            bot.send_message(message.chat.id, 'Солнечная погода!')
        elif im == "Rain":
            image = 'дождь.png'
            bot.send_message(message.chat.id, 'Дождливая погода!')
        elif im== "Clouds":
            image = 'туман.png'
            bot.send_message(message.chat.id, 'Облачная погода!')
        else:
            image = 'погода.jpg'
        file = open('./'+image, 'rb')
        bot.send_photo(message.chat.id,file)
    else:
        bot.reply_to(message, 'Такого города не существует:(')
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'Извините, но я умею говорить только о погоде!')


bot.polling(none_stop = True)