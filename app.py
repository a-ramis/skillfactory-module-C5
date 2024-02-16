import telebot
from config import TOKEN, keys
from extensions import CryptoConverter, APIExeption

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])  # обработчик команд start и help
def help(message: telebot.types.Message):
    text = """Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nПример: "доллар рубль 10"\nУвидеть список всех доступных валют: /values"""
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])  # обрабочик команды values
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text']) # обработчик запроса конвертации валют
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(" ")
        if len(val) != 3:
            raise APIExeption("Недопустимый формат запроса. Для помощи введите /help.")
        quote, base, amount = val
        total_price = CryptoConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} равна {total_price}."
        bot.reply_to(message, text)


bot.polling()
