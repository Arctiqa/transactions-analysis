from src.reports import gett_excel, spending_by_category


def test_spending_by_category():
    transactions = gett_excel('../data/operations.xls')
    result = spending_by_category(transactions, "Различные товары", '09.08.2021')

    assert len(result) == 28
    assert result['Сумма операции с округлением'].values[0] == 18.2


def test_spending_by_category_without_date():
    transactions = gett_excel('../data/operations.xls')
    result = spending_by_category(transactions, "Супермаркеты")

    assert len(result) == 0
    assert result['Сумма операции с округлением'].empty
