from utils import (get_excel_to_dicts_list, greetings, get_list_starting_from_month,
                   total_spent_splitting_by_cards, get_currency_rates, get_stock_prices, top_transactions)
import json
import logging
from typing import Any
import os

logger = logging.getLogger(__name__)


def compile_to_json(excel_file_path: str, date: str, user_settings: str) -> dict[Any, Any]:
    """
    Собирает в json файл из
    :param excel_file_path:
    :param date:
    :param user_settings:
    :return:
    """
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


print(compile_to_json('operations.xls', "31.03.2021 23:59:16", 'user_settings.json'))
