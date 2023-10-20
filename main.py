import telebot
from telebot import types

bot = telebot.TeleBot('6853421878:AAEMv3-_PF8FF7GNG8c_o-Ep4iEMB2-Arn8')

# Состояния бота
states = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Введите свои ФИО')
    states[message.chat.id] = "waiting_for_name"
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    if states.get(message.chat.id) == "waiting_for_name":
        # Обработка фамилии пользователя
        user_name = message.text
        send_menu(message)
        states[message.chat.id] = "waiting_for_command"

@bot.message_handler(func=lambda message: states.get(message.chat.id) == "waiting_for_command")
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    catalog = types.KeyboardButton('Каталог товаров')
    info = types.KeyboardButton('Аккаунт')
    wallet = types.KeyboardButton('Кошелек')
    markup.add(catalog, info, wallet)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)

@bot.message_handler(func=lambda message: states.get(message.chat.id) == "waiting_for_command", content_types=['text'])
def handle_menu(message):
    if message.text == 'Каталог товаров':
        send_catalog_menu(message.chat.id)
    elif message.text == 'Аккаунт':
        bot.send_message(message.chat.id, 'Вы выбрали Аккаунт')
    elif message.text == 'Кошелек':
        bot.send_message(message.chat.id, 'Вы выбрали Кошелек')

def send_catalog_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    test_product = types.KeyboardButton('First')
    markup.add(test_product)
    bot.send_message(chat_id, 'Выберите товар:', reply_markup=markup)

bot.polling(none_stop=True)
