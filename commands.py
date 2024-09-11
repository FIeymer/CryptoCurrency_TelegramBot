import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, CallbackQuery, Message

from bot_db import User, History
from config import BOT_TOKEN
from phrase import phrase_dict
import api_data
from typing import Dict

bot = telebot.TeleBot(BOT_TOKEN)

# creating user states
user_states: Dict[int, Dict[str, str]] = {}
STEP_ASK_TOKEN = "ask_token"
STEP_ASK_CURRENCY = "ask_currency"
STEP_PROCESS_DATA = "process_data"

# creating hint for bot commands
commands_eng = [
    BotCommand("/start", "Start interacting with the bot"),
    BotCommand("/help", "Show help message"),
    BotCommand("/lastprice", "Get the last price of a cryptocurrency"),
    BotCommand("/lowprice", "Get the lowest price of a cryptocurrency"),
    BotCommand("/highprice", "Get the highest price of a cryptocurrency"),
    BotCommand("/price_change", "Get the price change of a cryptocurrency"),
    BotCommand("/price_change_percent", "Get the price change percentage of a cryptocurrency"),
    BotCommand("/history", "Show requsts history")
]

commands_rus = [
    BotCommand("/start", "Начать взаимодействие с ботом"),
    BotCommand("/help", "Показать справку"),
    BotCommand("/lastprice", "Получить последнюю цену криптовалюты"),
    BotCommand("/lowprice", "Получить самую низкую цену криптовалюты"),
    BotCommand("/highprice", "Получить самую высокую цену криптовалюты"),
    BotCommand("/price_change", "Получить изменение цены криптовалюты"),
    BotCommand("/price_change_percent", "Получить процент изменения цены"),
    BotCommand("/history", "Показать историю запрсов")
]


def choose_langs() -> InlineKeyboardMarkup:
    # Creating buttons
    button_1 = InlineKeyboardButton(text="Eng", callback_data="Eng")
    button_2 = InlineKeyboardButton(text="Rus", callback_data="Rus")

    # Creating keyboard and adding buttons to keyboard
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2)
    return keyboard


def coin_markup() -> ReplyKeyboardMarkup:
    # creating buttons to chose coin
    button_1 = KeyboardButton(text="USDT")
    button_2 = KeyboardButton(text="USDC")

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(button_1, button_2)
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery) -> None:
    # Получаем данные пользователя и выбраный язык и записываем эти данные в базу данных
    # Getting user data and language and writtting it to database
    bot.send_message(call.message.chat.id, phrase_dict[call.data]['chose_lang'])
    if call.data == "Eng":
        bot.set_my_commands(commands_eng)
    elif call.data == "Rus":
        bot.set_my_commands(commands_rus)

    bot.send_message(call.message.chat.id, phrase_dict[call.data]['help_text'])
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    # Использование insert_or_update для обновления записи, если она существует
    # Using insert_or_update to update data if it exist
    User.insert(
        user_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        language=call.data
    ).on_conflict(
        conflict_target=[User.user_id],
        preserve=[User.username, User.first_name, User.last_name, User.language]
    ).execute()


@bot.message_handler(commands=['start'])
def handle_start(message: Message) -> None:
    # Отвечаем пользователю на старт бота на двух языках и предостовляем возможность выбора языка
    # Answering user to bot start in 2 languges and giving possibility to choose language
    bot.send_message(message.from_user.id, 'Welcome to the test version!\n Choose your language below.⤵️\n\n'
                                           'Добро пожаловать в тестовую версию!\n Выберите ваш язык ниже.⤵️\n\n',
                     reply_markup=choose_langs())


def get_user_language(user_id: int) -> str:
    # Получаем язык пользователя по его id
    # getting user langauge by his id
    user = User.get(User.user_id == user_id)
    return user.language


@bot.message_handler(commands=['help'])
def help_command(message: Message) -> None:
    # Выдаёт пользователю список доступных команд
    # answering user list of avaliable commands
    lang = get_user_language(message.from_user.id)
    text = phrase_dict[lang]['help_text']
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['lastprice'])
def lastprice_command(message: Message) -> None:
    # giving user last price coin

    # asking user for the coin, he wants
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, phrase_dict[lang]['get_coin'])

    user_states[message.chat.id] = {
        'step': STEP_ASK_TOKEN,
        'command': 'lastprice'
    }


@bot.message_handler(commands=['highprice'])
def highprice_command(message: Message) -> None:
    # giving user the high price coin in 24 hour

    # asking user for the coin, he wants
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, phrase_dict[lang]['get_coin'])

    user_states[message.chat.id] = {
        'step': STEP_ASK_TOKEN,
        'command': 'highprice'
    }


@bot.message_handler(commands=['lowprice'])
def lowprice_command(message: Message) -> None:
    # giving user the low price coin in 24 hour

    # asking user for the coin, he wants
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, phrase_dict[lang]['get_coin'])

    user_states[message.chat.id] = {
        'step': STEP_ASK_TOKEN,
        'command': 'lowprice'
    }


@bot.message_handler(commands=['price_change_percent'])
def price_change_percent_command(message: Message) -> None:
    # giving user the pice change coin in percent

    # asking user for the coin, he wants
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, phrase_dict[lang]['get_coin'])

    user_states[message.chat.id] = {
        'step': STEP_ASK_TOKEN,
        'command': 'price_change_percent'
    }


@bot.message_handler(commands=['price_change'])
def price_change_command(message: Message) -> None:
    # giving user the price change coin in 24h

    # asking user for the coin, he wants
    lang = get_user_language(message.from_user.id)
    bot.send_message(message.chat.id, phrase_dict[lang]['get_coin'])

    user_states[message.chat.id] = {
        'step': STEP_ASK_TOKEN,
        'command': 'price_change'
    }


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('step') == STEP_ASK_TOKEN)
def handle_token(message: Message) -> None:
    token = message.text.upper()
    lang = get_user_language(message.from_user.id)

    # Сохраняем токен и переходим к следующему шагу - запросу валюты
    # Saving token and coming to next step - getting currency token
    user_states[message.chat.id]['token'] = token
    user_states[message.chat.id]['step'] = STEP_ASK_CURRENCY

    bot.send_message(message.chat.id, phrase_dict[lang]['get_currency'], reply_markup=coin_markup())


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('step') == STEP_ASK_CURRENCY)
def handle_currency(message: Message) -> None:
    # getting currency coin and giving user result
    lang = get_user_language(message.from_user.id)
    currency = message.text.upper()

    user_states[message.chat.id]['currency'] = currency
    user_states[message.chat.id]['step'] = STEP_PROCESS_DATA

    pair = str(user_states[message.chat.id]['token'] + currency)

    if user_states[message.chat.id]['command'] == 'lowprice':
        result = api_data.get_lowprice(pair)
    elif user_states[message.chat.id]['command'] == 'price_change_percent':
        result = api_data.get_price_change_percent(pair)
    elif user_states[message.chat.id]['command'] == 'price_change':
        result = api_data.get_price_change(pair)
    elif user_states[message.chat.id]['command'] == 'highprice':
        result = api_data.get_highprice(pair)
    elif user_states[message.chat.id]['command'] == 'lastprice':
        result = api_data.get_lastprice(pair)

    if 'msg' in result:
        bot.send_message(message.chat.id, f'{phrase_dict[lang]['error']} : {result['msg']}')
    else:
        bot.send_message(message.chat.id, f'{pair} : {result}', reply_markup=ReplyKeyboardRemove())
        History.create(user=message.chat.id, command=user_states[message.chat.id]['command'], pair=pair, result=result)


@bot.message_handler(commands=['history'])
def price_change_command(message: Message) -> None:
    # giving user history request
    lang = get_user_language(message.from_user.id)
    try:
        user = User.get(User.user_id == message.chat.id)
    except User.DoesNotExist:
        bot.send_message(message.chat.id, phrase_dict[lang]['no_history'])
        return

    history_records = History.select().where(History.user == user).order_by(History.timestamp.desc())

    if not history_records:
        bot.send_message(message.chat.id, phrase_dict[lang]['no_history1'])
    else:
        history_text = f"{phrase_dict[lang]['history']}\n"
        for record in history_records:
            history_text += f"{record.timestamp}: {record.command}: {record.pair} - {record.result}\n"
        bot.send_message(message.chat.id, history_text)
