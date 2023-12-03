import pandas as pd
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import json
from typing import Any
import logging

load_dotenv()
STOCKS_API_KEY = os.environ.get('STOCKS_API_KEY')
CURRENCY_API_KEY = os.environ.get('CURRENCY_API_KEY')

logger = logging.getLogger(__name__)


def get_excel_to_dicts_list(operations_file: str) -> list:
    """
    Возвращаеет
    :param operations_file:
    :return:
    """
    path = f'{os.path.join(os.path.dirname(__file__), "..", "data", operations_file)}'
    try:

        operations = pd.read_excel(path, engine='xlrd')
        operations_list = operations.to_dict(orient='records')
        logger.info(f'excel file {os.path.join(os.getcwd(), "data", operations_file)}'
                    f' converted into python format')
        return operations_list
    except pd.errors.EmptyDataError:
        logger.warning("Invalid excel file.")
        return []
    except FileNotFoundError:
        logger.warning(f"File {operations_file} not found.")
        return []


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


def greetings(date: str) -> str:
    """
    Приветствие в зависимости от времени суток
    :param date: текущее время
    :return: приветствие
    """
    hour = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").hour
    if 6 <= hour <= 11:
        greeting = 'Доброе утро'
    elif 12 <= hour <= 18:
        greeting = 'Добрый день'
    elif 19 <= hour <= 23:
        greeting = 'Добрый вечер'
    else:
        greeting = 'Доброй ночи'
    return greeting


def total_spent_splitting_by_cards(list_by_dates: list[dict[Any, Any]]) -> list[dict[Any, Any]]:
    """
    Возвращает список словарей, с номерами карт, общим количеством трат по покупкам
    и начисленный по ним кэшбэк
    :param list_by_dates: список произведенных транзакций
    :return: card_info = {'last_digits': 4 последних номера карты,
                          'total_spent': общая трата по покупкам,
                          'cashback': начисленный кэшбэк}
    """
    cashback_rate = 0.01
    card_list = []

    cards = list(set(dct['Номер карты'] for dct in list_by_dates))
    for card in cards:
        total_spent = sum(dct['Сумма платежа'] for dct in list_by_dates
                          if dct['Сумма платежа'] < 0 and dct['Номер карты'] == card
                          and dct['Статус'] == 'OK')
        total_cashback = sum(dct['Бонусы (включая кэшбэк)'] for dct in list_by_dates
                             if dct['Сумма платежа'] < 0 and dct['Номер карты'] == card
                             and dct['Статус'] == 'OK')

        if total_spent == 0:
            continue
        card_info = {'last_digits': str(card)[1:],
                     'total_spent': round(-total_spent, 2),
                     'cashback': round(total_spent * (-cashback_rate) + total_cashback, 2)}
        card_list.append(card_info)
    return card_list


def get_list_starting_from_month(operations_list: list, date: str) -> list[dict[Any, Any]]:
    """
    Функция фильтрует список транзакций с начала месяца до заданной даты
    :param operations_list: список всех транзакций
    :param date: текущая дата
    :return: отфильтрованный список
    """
    dt_form = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    starting_date = dt_form.replace(day=1, hour=0, minute=0, second=0)

    list_by_dates = [dct for dct in operations_list if
                     starting_date <= datetime.strptime(str(dct["Дата операции"]), "%d.%m.%Y %H:%M:%S") <= dt_form]
    return list_by_dates


def top_transactions(list_by_dates: list[dict[Any, Any]]) -> list[dict[str, float]]:
    """
    Возвращает пять самых больших платежей по карте
    :param list_by_dates: список транзакций
    :return: словари вида {'date': "Дата платежа",
                           'amount': "Сумма платежа",
                           'category': "Категория",
                           'description': "Описание"})
    """
    list_by_dates_sorted = []
    for dct in list_by_dates:
        if isinstance(dct["Номер карты"], float):
            continue
        else:
            list_by_dates_sorted.append(dct)

    sorted_list_by_dates = sorted(list_by_dates_sorted, key=lambda x: x['Сумма операции с округлением'])
    top_transactions_list = []
    for dct in sorted_list_by_dates[-5:]:
        top_transactions_list.append({'date': dct["Дата платежа"],
                                      'amount': dct["Сумма платежа"],
                                      'category': dct["Категория"],
                                      'description': dct["Описание"]})

    return top_transactions_list


def compile_to_json(excel_file_path: str, date: str, user_settings: str) -> dict[Any, Any]:
    transactions_list = get_excel_to_dicts_list(excel_file_path)
    time = greetings(date)
    chosen_transactions = get_list_starting_from_month(transactions_list, date)
    cards_info = total_spent_splitting_by_cards(chosen_transactions)
    currencies = get_currency_rates(user_settings)
    stocks = get_stock_prices(user_settings)
    top_five = top_transactions(chosen_transactions)
    info = {'greeting': time,
            'cards': cards_info,
            'top transactions': top_five,
            'currency_rates': currencies,
            'stock_prices': stocks}

    with open('user_information_set.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    logger.info('json has been compiled')
    return info
