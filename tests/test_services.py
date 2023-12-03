import json

from src.services import cashback_profit


def test_cashback_profit():
    result = cashback_profit('operations.xls', 2021, 5)
    print(result)
    expected = {
        "Отели": 294,
        "Супермаркеты": 176,
        "Ж/д билеты": 121,
        "Транспорт": 80,
        "Аптеки": 71,
        "Госуслуги": 51,
        "Фастфуд": 47,
        "Различные товары": 25,
        "Дом и ремонт": 21,
        "Красота": 3,
        "Сувениры": 3,
        "Книги": 1,
        "Рестораны": 1,
        "Бонусы": 0,
        "Наличные": 0,
        "Переводы": 0,
        "Пополнения": 0,
        "Связь": 0,
        "Сервис": 0,
        "Турагентства": 0,
        "Услуги банка": 0
    }
    assert json.loads(result) == expected


def test_cashback_profit_errors():
    result = cashback_profit('operation.xls', 2021, 5)
    assert result == ''
