import json
import logging
from collections import Counter
from datetime import datetime

from src.utils import data_from_excel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="../logs/services.log",
    filemode="w",
    encoding="utf-8",
)

main_logger = logging.getLogger("services")


def cashback_categories(paths_to_data: str, target_year: str, target_month: str) -> dict:
    """Функция выводит информацию о кэшбэке по категориям в JSON формате"""

    data_raw = data_from_excel(paths_to_data)
    data = []
    # for item in data_raw:
    #     if item["Дата платежа"] != "":
    #         day, month, year = item["Дата платежа"].split(".")
    #         if year == target_year and month == target_month:
    #             data.append(item)

    for item in data_raw:
        payment_date_str = item["Дата платежа"]

        if payment_date_str or payment_date_str != "":

            try:
                payment_date = datetime.strptime(payment_date_str, "%d.%m.%Y")

                if payment_date.year == int(target_year) and payment_date.month == int(target_month):
                    data.append(item)
            except ValueError as e:
                main_logger.info(f"Ошибка преобразования даты '{payment_date_str}': {e}")
                print(f"Ошибка преобразования даты '{payment_date_str}': {e}")

    main_logger.info("Сформирован файл для заданного месяца и года")

    categories_list = [operation["Категория"] for operation in data if "Категория" in operation]

    operations_count = Counter(categories_list)

    create_zero_dict = lambda cats: {cat: 0 for cat in cats}
    cashback = create_zero_dict(operations_count.keys())

    for key in operations_count.keys():
        for item in data:
            if key in item["Категория"]:
                if item["Кэшбэк"] != "":
                    cashback[key] = cashback[key] + int(item["Кэшбэк"])

    with open("../data/json_outputs/cashback_by_categories.json", "w", encoding="utf-8") as f:
        json.dump(cashback, f, ensure_ascii=False, indent=4)

    main_logger.info("Данные работы функции записаны в файл JSON")

    return cashback


# print(cashback_categories('../data/operations.xlsx', '2021', '07'))
