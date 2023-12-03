from unittest.mock import patch
import json
from src.utils import get_stock_prices, get_currency_rates


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
