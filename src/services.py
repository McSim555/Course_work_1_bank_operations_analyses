import json
from collections import Counter
from src.utils import data_from_excel


def cashback_categories(paths_to_data: str, target_year: str, target_month: str) -> dict:
    """Функция выводит информацию о кэшбэке по категориям в JSON формате"""

    data_raw = data_from_excel(paths_to_data)
    data = []
    for item in data_raw:
        if item["Дата платежа"] != "":
            day, month, year = item["Дата платежа"].split(".")
            if year == target_year and month == target_month:
                data.append(item)

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

    return cashback


# print(cashback_categories('../data/operations.xlsx', '2021', '12'))
