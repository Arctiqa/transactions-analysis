import pandas as pd
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import json
from typing import Any

load_dotenv()
STOCKS_API_KEY = os.environ.get('STOCKS_API_KEY')
CURRENCY_API_KEY = os.environ.get('CURRENCY_API_KEY')


def get_stock_prices(user_settings: str) -> list[dict[str, float]]:
    path = os.path.join('..', 'data', user_settings)

    with open(path, 'r') as jsn:
        settings = json.load(jsn)
        user_stocks = settings['user_stocks']

    stocks_url = f'https://financialmodelingprep.com/api/v3/stock/real-time-price?apikey={STOCKS_API_KEY}'
    response_stocks = requests.get(stocks_url)

    stocks = json.loads(response_stocks.text)['stockList']

    stock_prices = [{'stock': dct['symbol'],
                     'price': dct['price']} for dct in stocks if dct['symbol'] in user_stocks]
    return stock_prices


def get_currency_rates(user_settings: str) -> list[dict[str, float]]:
    path = os.path.join('..', 'data', user_settings)

    with open(path, 'r') as jsn:
        settings = json.load(jsn)
        user_currencies = settings['user_currencies']

    currency_url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=" \
                   f"{'%2C%20'.join(user_currencies)}&base=RUB"
    response_currency = requests.get(currency_url, headers={"apikey": CURRENCY_API_KEY}).json()

    currencies = response_currency['rates']
    currency_rates = [{'currency': key,
                       'rate': round((1 / value), 2)} for key, value in currencies.items()]
    return currency_rates


def greetings(date):
    hour = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").day
    if 6 <= hour <= 11:
        greeting = 'Доброе утро'
    elif 12 <= hour <= 18:
        greeting = 'Добрый день'
    elif 19 <= hour <= 23:
        greeting = 'Добрый вечер'
    else:
        greeting = 'Доброй ночи'

    return greeting


def total_spent_splitting_by_cards(list_by_dates: list[dict[Any]]):
    cashback_rate = 0.01
    card_list = []

    cards = list(set(dct['Номер карты'] for dct in list_by_dates))
    for card in cards:
        total_spent = sum(dct['Сумма платежа'] for dct in list_by_dates
                          if dct['Сумма платежа'] < 0 and dct['Номер карты'] == card
                          and dct['Статус'] == 'OK')
        if total_spent == 0:
            continue
        card_info = {'last_digits': str(card)[1:],
                     'total_spent': round(-total_spent, 2),
                     'cashback': round(total_spent * (-cashback_rate), 2)}
        card_list.append(card_info)
    return card_list


def get_list_starting_from_month(operations_file: str, date: str) -> list[dict[Any]]:
    dt_form = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    starting_date = dt_form.replace(day=1, hour=0, minute=0, second=0)

    path = os.path.join('..', 'data', operations_file)
    operations = pd.read_excel(path)
    group = operations.groupby('Номер карты')
    print(group.size())
    operations_list = operations.to_dict(orient='records')

    list_by_dates = [dct for dct in operations_list if
                     starting_date <= datetime.strptime(str(dct["Дата операции"]), "%d.%m.%Y %H:%M:%S") <= dt_form]

    return list_by_dates


def top_transactions(list_by_dates):
    sorted_list_by_dates = sorted(list_by_dates, key=lambda x: x['Сумма операции с округлением'])
    top_transactions_list = []
    for dct in sorted_list_by_dates[-5:]:
        top_transactions_list.append({'date': dct["Дата платежа"],
                                      'amount': dct["Сумма платежа"],
                                      'category': dct["Категория"],
                                      'description': dct["Описание"]})
    return top_transactions_list


lst = get_list_starting_from_month('operations.xls', '31.07.2020 23:53:50')
print(lst)
card = total_spent_splitting_by_cards(lst)
print(card)
