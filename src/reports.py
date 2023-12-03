from functools import wraps
from typing import Optional, Callable
import pandas as pd
from datetime import datetime
import logging
from dateutil.relativedelta import relativedelta
import os

logger = logging.getLogger(__name__)


def spending_result(file_name: str = 'result') -> Callable:
    """
    Декоратор для записи результата функции в csv файл
    :param file_name: название записываемого файла
    :return: результат выполняемой функции
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            path = f'{os.path.join(os.path.dirname(__file__), "..", "data", file_name)}.csv'
            result.to_csv(path, index=True)
            logger.info(f'Result written to file - {file_name}')
            return result

        return inner

    return wrapper


def gett_excel(operations_file):
    path = f'{os.path.join(os.path.dirname(__file__), "..", "data", operations_file)}'
    transactions = pd.read_excel(path, index_col=0)
    return transactions


@spending_result(file_name='result')
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние 3 месяца (от переданной даты)
    :param transactions: датафрейм с транзакциями
    :param category: название категории
    :param date: дата
    :return:
    """
    if date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(date, '%d.%m.%Y')

    transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'], dayfirst=True)
    three_months_date = current_date - relativedelta(month=3)

    filtered_transactions = transactions[
        (transactions['Категория'] == category) & (transactions['Дата платежа'] > three_months_date)
        & (transactions['Дата платежа'] <= current_date)]
    result = filtered_transactions[['Сумма операции с округлением', 'Описание']]
    return result


# transactions_data = gett_excel('operations.xls')
# categories = spending_by_category(transactions_data,
#                                   "Супермаркеты",
#                                   '17.07.2021')
