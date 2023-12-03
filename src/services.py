import json
import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


def cashback_profit(operations_list: str, year: int, month: int) -> str:
    """
    Функция позволяет проанализировать,
    какие категории были наиболее выгодными для выбора в качестве
    категорий повышенного кэшбэка, результат возвращается в формате JSON
    :param operations_list: список транзакций
    :param year: заданный год
    :param month: заданный месяц
    :return: JSON файл по категориям кэшбэка
    """
    path = f'{os.path.join(os.path.dirname(__file__), "..", "data", operations_list)}'
    try:
        operations = pd.read_excel(path)
        df = pd.DataFrame(operations)

        dates = pd.to_datetime(df['Дата платежа'], dayfirst=True)
        filtered_data = df[(dates.dt.year == year) & (dates.dt.month == month)]

        cashback = filtered_data.groupby('Категория')["Бонусы (включая кэшбэк)"].sum()
        cashback_dict = cashback.to_dict()
        sorted_dict = dict(sorted(cashback_dict.items(), key=lambda x: x[1], reverse=True))
        to_json = json.dumps(sorted_dict, indent=2, ensure_ascii=False)
        logger.info('cashback profit by category converted to JSON')
        return to_json
    except pd.errors.EmptyDataError:
        logger.error(f'file {operations_list} not found')
        return ''
    except FileNotFoundError as e:
        logger.error(f'{e}')
        return ''


# result = cashback_profit('operations.xls', 2020, 6)
# print(result)
