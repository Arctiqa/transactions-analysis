import json
import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()
STOCKS_API_KEY = os.environ.get('STOCKS_API_KEY')
CURRENCY_API_KEY = os.environ.get('CURRENCY_API_KEY')

logger = logging.getLogger(__name__)


def get_stock_prices(user_settings: str) -> list[dict[str, float]]:
    """
    Возвращает список словарей с ценами на акции заданных компаний
    :param user_settings: JSON файл настроек пользователя
    :return: список словарей вида {акция: цена акции}
    """
    path = f'{os.path.join(os.path.dirname(__file__), "..", "data", user_settings)}'

    with open(path, 'r') as jsn:
        settings = json.load(jsn)
        user_stocks = settings['user_stocks']

    stocks_url = f'https://financialmodelingprep.com/api/v3/stock/real-time-price?apikey={STOCKS_API_KEY}'
    try:
        response_stocks = requests.get(stocks_url)
        stocks = json.loads(response_stocks.text)['stockList']

        stock_prices = [{'stock': dct['symbol'],
                         'price': float(dct['price'])} for dct in stocks if dct['symbol'] in user_stocks]
        logger.info('stock rates has been received from API')
        return stock_prices
    except Exception as e:
        logger.error(f'Error during API request: {e}')
        return []


def get_currency_rates(user_settings: str) -> list[dict[str, float]] | None:
    """
    Возвращает курс валюты по отношению к рублю
    :param user_settings: JSON файл настроек пользователя
    :return: список словарей вида {валюта: курс к рублю}
    """
    path = f'{os.path.join(os.path.dirname(__file__), "..", "data", user_settings)}'

    with open(path, 'r') as jsn:
        settings = json.load(jsn)
        user_currencies = settings['user_currencies']

    currency_url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=" \
                   f"{'%2C%20'.join(user_currencies)}&base=RUB"

    try:
        if CURRENCY_API_KEY is None:
            raise ValueError('API не определен')
        response_currency = requests.get(currency_url, headers={"apikey": CURRENCY_API_KEY}).json()

        currencies = response_currency['rates']
        currency_rates = [{'currency': key,
                           'rate': round((1 / value), 2)} for key, value in currencies.items()]
        logger.info('currency has been received from API')
        return currency_rates
    except Exception as e:
        logger.error(f'Error during API request: {e}')
        return None
