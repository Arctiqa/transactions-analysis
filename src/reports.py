from functools import wraps
from typing import Optional, Callable
import pandas as pd
from datetime import datetime, timedelta
import logging
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


def spending_result(file_name: str = 'result.csv') -> Callable:
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_csv(fr'../data/{file_name}.csv', index=True)
            logger.info(f'Result written to file - {file_name}')
            return result

        return inner

    return wrapper


def gett_excel(operations_file):
    transactions = pd.read_excel(operations_file, index_col=0)
    return transactions


s = gett_excel(r'../data/operations.xls')


@spending_result()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
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


spending_by_category(s, "Супермаркеты", "22.08.2020")
