import requests
import json
from config import keys

class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')


        try:
            amount_float = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        if amount_float <= 0:
            raise APIException('Количество должно быть положительным числом')


        try:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
            data = r.json()
        except requests.exceptions.RequestException as e:
            raise ConversionException(f'Ошибка подключения к API: {e}')
        except json.JSONDecodeError:
            raise ConversionException('Ошибка обработки ответа от API')

        if base_ticker not in data:
            raise ConversionException(f'Курс для {base} не получен')

        total_base = amount_float * data[base_ticker]
        return total_base