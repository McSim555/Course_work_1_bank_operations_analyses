from utils import data_from_excel
import json
from collections import Counter


def cashback_categories(paths_to_data: str, year: str, month: str) -> dict:
    """Функция выводит информацию о кэшбэке по категориям в JSON формате"""

    data = data_from_excel(paths_to_data)

    categories_list = [operation["Категория"] for operation in data if "Категория" in operation]

    operations_count = Counter(categories_list)

    create_zero_dict = lambda cats: {cat: 0 for cat in cats}
    cashback = create_zero_dict(operations_count.keys())

    for key in operations_count.keys():
        for item in data:
            if key in item['Категория']:
                if item['Кэшбэк'] != '':
                    cashback[key] = cashback[key] + int(item['Кэшбэк'])

    with open('../data/json_outputs/cashback_by_categories.json', 'w', encoding='utf-8') as f:
        json.dump(cashback, f, ensure_ascii=False, indent=4)

    return cashback

print(cashback_categories('../data/operations.xlsx', '2021', '04'))

    # for operation in data:
    #     if operation['Дата операции'][6:10] == year and operation['Дата операции'][3:5] == month:


    # {
    #     "Категория 1": 1000,
    #     "Категория 2": 2000,
    #     "Категория 3": 500
    # }