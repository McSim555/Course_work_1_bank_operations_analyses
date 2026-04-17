from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) \
        -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца от переданной даты.
    Формат даты YYYY-MM-DD"""

    required_columns = ["Категория", "Сумма операции", "Дата платежа"]
    missing_columns = [col for col in required_columns if col not in transactions.columns]
    if missing_columns:
        raise ValueError(f"Отсутствуют колонки: {missing_columns}")

    transactions = transactions.fillna("")

    date = pd.to_datetime(date)

    if date is None:
        reference_date = datetime.now()
    else:
        reference_date = pd.to_datetime(date)

    start_date = reference_date - timedelta(days=90)

    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)

    filtered = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата платежа"] >= start_date)
        & (transactions["Дата платежа"] <= reference_date)
    ]

    result = (
        filtered.groupby("Категория", as_index=False)
        .agg({"Сумма операции": "sum"})
        .rename(columns={"Сумма операции": "Сумма трат"})
    )
    result["Сумма трат"] = result["Сумма трат"].abs()

    # Если данных нет, возвращаем пустой DataFrame с нужной структурой
    if result.empty:
        result = pd.DataFrame({"Категория": [category], "Сумма трат": [0]})

    return result


def my_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result.to_csv("../data/reports/report.csv", index=False, encoding="utf-8")
        return result

    return wrapper


# spending_by_category = my_decorator(spending_by_category)
# spending_by_category(pd.read_excel('../data/operations.xlsx'), 'Каршеринг', '2021-11-25')


def my_decorator_with_param(file_name: str):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            full_path = f"../data/reports/{file_name}"
            result = func(*args, **kwargs)
            result.to_csv(full_path, index=False)
            return result

        return wrapper

    return my_decorator


# spending_by_category = my_decorator_with_param('report_new.csv')(spending_by_category)
# spending_by_category(pd.read_excel('../data/operations.xlsx'), 'Фастфуд', '2021-11-25')

# print(spending_by_category(pd.read_excel('../data/operations.xlsx'), 'Супермаркеты', '2021-11-25'))
