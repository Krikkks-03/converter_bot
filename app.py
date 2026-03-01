import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ("Чтобы начать работу, введите команду боту в следующем формате:\n"
        "<имя валюты><в какую валюту перевести><количество переводимой валюты>\n"
        "Например: евро доллар 150\n"
        "Увидеть список всех доступных валют: /values")
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += f"\n{key}"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров. Введите 3 параметра: <название валюты><в какую валюту><количество валюты>')

        quote, base, amount = values
        quote = quote.lower()
        base = base.lower()

        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base:.2f} {base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)