from unittest.mock import patch
import json
import pytest

from src.utils import (get_excel_to_dicts_list, get_stock_prices, get_list_starting_from_month,
                       get_currency_rates, greetings, total_spent_splitting_by_cards)

import pandas as pd


@pytest.fixture
def settings():
    return {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }


@patch('src.utils.pd.read_excel')
def test_get_excel_to_dicts_list(mock_get):
    mock_object = {'col1': [1, 2], 'col2': ['a', 'b']}
    mock_get.return_value.to_dict.return_value = mock_object

    result = get_excel_to_dicts_list('operations.xls')
    assert result == mock_object


def test_get_excel_to_dict_errors():
    result_empty = get_excel_to_dicts_list('operations_empty.xls')
    assert result_empty == []

    result_not_exist = get_excel_to_dicts_list('operations_not_exist.xls')
    assert result_not_exist == []


@patch('requests.get')
def test_get_stock_prices_success(mock_get):
    mock_response = {
        'stockList': [
            {'symbol': 'AAPL', 'price': 150.0},
            {'symbol': 'GOOGL', 'price': 200.0},
            {'symbol': 'MSFT', 'price': 250.0}
        ]
    }
    mock_get.return_value.text = json.dumps(mock_response)

    expected_result = [
        {'stock': 'AAPL', 'price': 150.0},
        {'stock': 'GOOGL', 'price': 200.0},
        {'stock': 'MSFT', 'price': 250.0}
    ]
    actual_result = get_stock_prices('user_settings.json')

    assert actual_result == expected_result


@patch('requests.get')
def test_get_stock_prices_api_error(mock_get):
    mock_get.return_value.text = None

    result = get_stock_prices('user_settings.json')
    assert result == []


@patch('requests.get')
def test_get_currency_rates(mock_get):
    mock_response = {'rates': {'USD': 0.013, 'EUR': 0.011, 'GBP': 0.009}}
    mock_get.return_value.json.return_value = mock_response
    expected = [
        {'currency': 'USD', 'rate': 76.92},
        {'currency': 'EUR', 'rate': 90.91},
        {'currency': 'GBP', 'rate': 111.11}
    ]

    result = get_currency_rates(r'user_settings.json')

    assert result == expected


@patch('requests.get')
def test_get_currency_rates_error(mock_get):
    mock_get.return_value.json.return_value = None
    result = get_currency_rates(r'user_settings.json')

    assert result is None


@pytest.mark.parametrize('time, expected', [('20.08.2020 07:52:48', 'Доброе утро'),
                                            ('20.08.2020 12:52:48', 'Добрый день'),
                                            ('20.08.2020 19:52:48', 'Добрый вечер'),
                                            ('20.08.2020 05:52:48', 'Доброй ночи')])
def test_greetings(time, expected):
    assert greetings(time) == expected


def test_total_spent_splitting_by_cards():
    pass