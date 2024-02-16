import json
import requests
from config import keys


class APIExeption(Exception): # класс исключения для вызова при ошибке пользователя
    pass


class CryptoConverter: # класс для отправки запросов к API
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIExeption("Невозможно перевести одну и ту же валюту.")
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIExeption(f"Не удалось обработать валюту {quote}.\nУвидеть список всех доступных валют: /values")
        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIExeption(f"Не удалось обработать валюту {base}.\nУвидеть список всех доступных валют: /values")
        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f"Не удалось обработать число {amount}.")
        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        price = json.loads(response.content)[base_ticker] * amount
        return price
