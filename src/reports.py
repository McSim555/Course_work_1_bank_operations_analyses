import json
import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="../logs/reports.log",
    filemode="w",
    encoding="utf-8",
)

main_logger = logging.getLogger("reports")


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца от переданной даты.
    Формат даты YYYY-MM-DD"""

    required_columns = ["Категория", "Сумма операции", "Дата платежа"]
    missing_columns = [col for col in required_columns if col not in transactions.columns]
    if missing_columns:
        main_logger.error(f"Отсутствуют колонки: {missing_columns}")
        raise ValueError(f"Отсутствуют колонки: {missing_columns}")

    main_logger.info("Все необходимые колонки присутствуют")

    transactions = transactions.fillna("")

    date = pd.to_datetime(date)

    if date is None:
        reference_date = datetime.now()
    else:
        reference_date = pd.to_datetime(date)

    main_logger.info(f"Референтная дата {reference_date}")

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

    main_logger.info("Результат ОК")

    return result


def my_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        json_string = result.to_json()
        json_decoded = json_string.encode().decode("unicode_escape")
        with open("../data/json_outputs/spending_by_category.json", "w", encoding="utf-8") as f:
            json.dump(json_decoded, f, ensure_ascii=False, indent=4)
        return result

    return wrapper


# spending_by_category = my_decorator(spending_by_category)
# spending_by_category(pd.read_excel('../data/operations.xlsx'), 'Каршеринг', '2021-11-25')


def my_decorator_with_param(file_name: str):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            full_path = f"../data/json_outputs/{file_name}"
            result = func(*args, **kwargs)
            json_string = result.to_json()
            json_decoded = json_string.encode().decode("unicode_escape")
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(json_decoded, f, ensure_ascii=False, indent=4)
            return result

        return wrapper

    return my_decorator


# spending_by_category = my_decorator_with_param('spending_by_category_new')(spending_by_category)
# spending_by_category(pd.read_excel('../data/operations.xlsx'), 'Фастфуд', '2021-11-25')

# print(spending_by_category(pd.read_excel('../data/operations.xlsx'), 'Супермаркеты', '2021-11-25'))
