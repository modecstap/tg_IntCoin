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
        # Обработка фио юзера
        user_name = message.text
        send_menu(message)
        # меняем состояние ботинка
        states[message.chat.id] = "waiting_for_command"


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "waiting_for_command")
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    catalog = types.KeyboardButton('Каталог товаров')
    info = types.KeyboardButton('Аккаунт')
    wallet = types.KeyboardButton('Кошелек')
    markup.add(catalog, info, wallet)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    handle_menu(message)


@bot.message_handler(func=lambda message: states.get(message.chat.id) == "waiting_for_command", content_types=['text'])
def handle_menu(message):
    if message.text == 'Каталог товаров':
        send_catalog_menu(message.chat.id)
    elif message.text == 'Аккаунт':
        send_account_info(message.chat.id)
    elif message.text == 'Кошелек':
        send_wallet_info(message.chat.id)


# вывод кнопок внутри сообщений(категории)
def send_catalog_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Fist', callback_data='first'))
    bot.send_message(chat_id, 'Выберите категорию:', reply_markup=markup)


def send_account_info(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('second', callback_data='second'))
    bot.send_message(chat_id, 'Выберите категорию:', reply_markup=markup)


def send_wallet_info(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('thried', callback_data='thried'))
    bot.send_message(chat_id, 'Выберите категорию:', reply_markup=markup)


# Обработчик нажатий на кнопАчки в менюшке
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    if call.data == 'first':
        bot.send_message(call.message.chat.id, 'Вы выбрали категорию "First"')
    elif call.data == 'second':
        bot.send_message(call.message.chat.id, 'Вы выбрали категорию "second"')
    elif call.data == 'thried':
        bot.send_message(call.message.chat.id, 'Вы выбрали категорию "три"')


# нонстоп работа
bot.polling(none_stop=True)
