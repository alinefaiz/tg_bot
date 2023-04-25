# pip install pyTelegramBotAPI
# pip install Faker
from secrets import token_urlsafe
import json
from faker import Faker

bot = TeleBot(token='ТВОЙ_ТОКЕН', parse_mode='html') # создание бота
faker = Faker('ru_RU')

@bot.message_handler(commands=['start'])# обработчик команды '/start'

def start(message):
	#клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Словарик')
    item2 = types.KeyboardButton('Сгенерировать тестовые данные пользователя')
    item3 = types.KeyboardButton('В главное меню')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Привет! Ты можешь спросить у меня определение какого-нибудь слова. \nИли же я могу сгенерировать тестовые данные пользователя. \nВыбери то, что тебе нужно!', reply_markup=markup)

DEFINITOINS = {#Словарик
    'регресс': 'Проверить что новый функционал не сломал существующий',
    'новое_слово': 'Определение',
}

# обработчик всех остальных сообщений
@bot.message_handler()

def message_handler(message: types.Message):
    if message.text == 'В главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Словарик')
        item2 = types.KeyboardButton('Сгенерировать тестовые данные пользователя')
        item3 = types.KeyboardButton('В главное меню')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Ты в главном меню. \nВыбери то, что тебе нужно!', reply_markup=markup)
    elif message.text == 'Словарик':
        bot.send_message(message.chat.id, 'Введи слово.')
        bot.register_next_step_handler(message, word)
    elif message.text == 'Сгенерировать тестовые данные пользователя':
        bot.send_message(message.chat.id, 'Введи количество пользователей. (Максимум 20)')
        bot.register_next_step_handler(message, generate_user_data)
    else: # если текст не совпал ни с одной из кнопок выводим ошибку
        bot.send_message(
        chat_id=message.chat.id,
        text='Не понимаю тебя :(',
    )
        
def word(message):
    if message.text == 'В главное меню':
        bot.register_next_step_handler(message, message_handler(message))
        return
    elif message.text == 'Сгенерировать тестовые данные пользователя':
        bot.register_next_step_handler(message, message_handler(message))
        return
    definition = DEFINITOINS.get(
    message.text.lower(), # приводим текст сообщения к нижнему регистру
    )
    if definition is None:
        bot.send_message(
            chat_id=message.chat.id,
            text='Я пока не знаю такого определения.',
        )
        message.text='Словарик'
        bot.register_next_step_handler(message, message_handler(message))
        return
    # если ключевая фраза была найдена, формируем текст сообщения и отправляем его
    # если перед строкой поставить букву f, то в фигурных скобках {} можно использовать переменные :)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Определение:\n<code>{definition}</code>',
    )
    message.text='Словарик'
    bot.register_next_step_handler(message, message_handler(message))

def generate_user_data(message):
    payload_len = 0
    if message.text == 'В главное меню':
        bot.register_next_step_handler(message, message_handler(message))
        return
    elif message.text == 'Словарик':
        bot.register_next_step_handler(message, message_handler(message))
        return
    elif message.text.isdigit() and int(message.text)<=20 and int(message.text)>0:
        payload_len = int(message.text)
    else:
        bot.send_message(chat_id=message.chat.id, text='Я так не могу :(')
        message.text='Сгенерировать тестовые данные пользователя'
        bot.register_next_step_handler(message, message_handler(message))
        return

    # генерируем тестовые данные для выбранного количества пользователей при помощи метода simple_profile
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        # при помощи библиотеки secrets генерируем пароль
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # сериализуем данные в строку
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )
    # отправляем результат
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    message.text='Сгенерировать тестовые данные пользователя'
    bot.register_next_step_handler(message, message_handler(message))

# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()