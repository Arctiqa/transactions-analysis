import pandas as pd
import os
import json
import logging

logger = logging.getLogger(__name__)


def cashback_profit(operations_list, year, month):
    path = os.path.join('..', 'data', operations_list)
    try:
        operations = pd.read_excel(path)
        df = pd.DataFrame(operations)

        dates = pd.to_datetime(df['Дата платежа'], dayfirst=True)
        filtered_data = df[(dates.dt.year == year) & (dates.dt.month == month)]

        cashback = filtered_data.groupby('Категория')["Бонусы (включая кэшбэк)"].sum()
        cashback_dict = cashback.to_dict()
        sorted_dict = dict(sorted(cashback_dict.items(), key=lambda x: x[1], reverse=True))
        return json.dumps(sorted_dict, indent=2, ensure_ascii=False)
    except pd.errors.EmptyDataError:
        logger.error(f'file {operations_list} not found')
    except pd.errors.DataError as e:
        logger.error(f'{e}')


print(cashback_profit('operations.xls', 2021, 3))
