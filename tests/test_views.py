from math import nan
from unittest.mock import patch

import pytest

from src.views import (get_excel_to_dicts_list, get_list_starting_from_month, greetings, top_transactions,
                       total_spent_splitting_by_cards)


@pytest.fixture
def data_file_excel():
    result = get_excel_to_dicts_list('operations.xls')
    return result


@patch('src.views.pd.read_excel')
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


@pytest.mark.parametrize('time, expected', [('20.08.2020 07:52:48', 'Доброе утро'),
                                            ('20.08.2020 12:52:48', 'Добрый день'),
                                            ('20.08.2020 19:52:48', 'Добрый вечер'),
                                            ('20.08.2020 05:52:48', 'Доброй ночи')])
def test_greetings(time, expected):
    assert greetings(time) == expected


def test_get_list_starting_from_month(data_file_excel):
    result = get_list_starting_from_month(data_file_excel, '01.07.2021 13:00:58')

    expected = [
        {'Дата операции': '01.07.2021 12:57:58', 'Дата платежа': '03.07.2021', 'Номер карты': '*7197', 'Статус': 'OK',
         'Сумма операции': -182.0, 'Валюта операции': 'RUB', 'Сумма платежа': -182.0, 'Валюта платежа': 'RUB',
         'Кэшбэк': nan,
         'Категория': 'Транспорт', 'MCC': 4121.0, 'Описание': 'Яндекс Такси', 'Бонусы (включая кэшбэк)': 3,
         'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 182.0}]

    assert result[0]['Дата операции'] == expected[0]['Дата операции']
    assert result[0]['Сумма операции'] == expected[0]['Сумма операции']
    assert result[0]['Бонусы (включая кэшбэк)'] == expected[0]['Бонусы (включая кэшбэк)']
    assert result[0]['Сумма операции с округлением'] == expected[0]['Сумма операции с округлением']


def test_total_spent_splitting_by_cards(data_file_excel):
    lst = get_list_starting_from_month(data_file_excel, "25.08.2021 23:59:16")
    result = total_spent_splitting_by_cards(lst)
    expected1 = {'last_digits': '4556', 'total_spent': 3734.5, 'cashback': 194.34}
    expected2 = {'last_digits': '7197', 'total_spent': 9344.96, 'cashback': 251.45}

    assert expected1 in result
    assert expected2 in result


def test_top_transactions(data_file_excel):
    lst = get_list_starting_from_month(data_file_excel, "17.05.2020 2:50:16")
    result = top_transactions(lst)

    expected1 = {'date': '06.05.2020', 'amount': -297.48, 'category': 'Супермаркеты', 'description': 'Колхоз'}
    expected2 = {'date': '07.05.2020', 'amount': -426.6, 'category': 'Супермаркеты', 'description': 'Prisma'}

    assert expected1 in result
    assert expected2 in result
