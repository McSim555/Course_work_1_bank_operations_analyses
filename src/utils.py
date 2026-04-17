import json
import os
import re

import pandas as pd
import requests
from dotenv import load_dotenv


def greetings(date_time: str) -> str:
    """Функция для выбора приветствия"""

    try:
        time_value = re.findall(r"\d{2}:\d{2}:\d{2}", date_time)
        time_str = time_value[0]
    except Exception:
        print("Время введено некорректно")

    if int(time_str[:2]) < 5:
        greeting = "Доброй ночи!"
    elif 5 <= int(time_str[:2]) < 11:
        greeting = "Доброе утро!"
    elif 11 <= int(time_str[:2]) < 18:
        greeting = "Добрый день!"
    else:
        greeting = "Добрый вечер!"

    return greeting


def data_from_excel(path_to_excel: str) -> list[dict]:
    """Функция для считывания финансовых операций из Excel выдает список словарей с данными
    :rtype: list[dict]
    """

    try:
        excel_data = pd.read_excel(path_to_excel)

        excel_data_filled = excel_data.fillna("")

        excel_transactions_list = excel_data_filled.to_dict(orient="records")

        return excel_transactions_list

    except Exception:
        print("Файл не найден или ошибка чтения файла")
        return []


# print(data_from_excel('../data/operations.xlsx'))


def cards_data(excel_file: list[dict], date_time: str) -> list[dict]:
    """Функция для подготовки данных по картам в заданном формате"""

    year = date_time.split("-")[0]
    month = date_time.split("-")[1]
    day = date_time.split("-")[2][:2]

    categories_no_cashback = (
        "Бонусы",
        "Госуслуги",
        "Другое",
        "Зарплата",
        "Наличные",
        "НКО",
        "Переводы",
        "Пополнения",
        "Услуги банка",
        "Финансы",
        "",
    )
    cards_list = []

    for operation in excel_file:
        if (
            operation["Дата операции"][6:10] == year
            and operation["Дата операции"][3:5] == month
            and 0 < int(operation["Дата операции"][:2]) <= int(day)
            and operation["Номер карты"] != ""
        ):

            if operation["Категория"] in categories_no_cashback:
                cash_back = 0.0
            else:
                cash_back = (float(operation["Сумма операции"]) * (-1)) // 100

            single_operation = {
                "last_digits": operation["Номер карты"][1:],
                "total_spent": operation["Сумма операции"],
                "cashback": cash_back,
            }

            cards_list.append(single_operation)

    return cards_list


# date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# date_string = '2026-04-16 01:11:11'
# print(cards_data(data_from_excel('../data/operations.xlsx'), date_string))


def sort_by_payment(excel_file: list[dict], date_time: str) -> list[dict]:
    """Функция определяет ТОП5 транзакций по сумме платежа"""

    year = date_time.split("-")[0]
    month = date_time.split("-")[1]
    day = date_time.split("-")[2][:2]

    excel_file_selected = []

    for operation in excel_file:
        if (
            operation["Дата операции"][6:10] == year
            and operation["Дата операции"][3:5] == month
            and 0 < int(operation["Дата операции"][:2]) <= int(day)
        ):
            excel_file_selected.append(operation)

    sorted_set = sorted(excel_file_selected, key=lambda x: abs(x["Сумма платежа"]), reverse=True)
    top5 = sorted_set[:5]
    top5_selected = []
    for operation in top5:
        selection = {
            "date": operation["Дата платежа"],
            "amount": operation["Сумма платежа"],
            "category": operation["Категория"],
            "description": operation["Описание"],
        }
        top5_selected.append(selection)
    return top5_selected


# print(sort_by_payment(data_from_excel('../data/operations.xlsx'), date_string))


def currency_rates(path_user_settings: str, date: str) -> list[dict]:
    """Функция получает курс валют на заданную дату"""

    with open(path_user_settings, "r", encoding="utf-8") as file:
        settings = json.load(file)
        currencies = settings["user_currencies"]

    currency_rates_list = []

    for item in currencies:
        url = "https://api.apilayer.com/exchangerates_data/convert"
        load_dotenv("../.env")
        API_KEY = os.getenv("API_KEY")
        headers = {"apikey": API_KEY}
        payload = {"amount": 1, "from": item, "to": "RUB"}

        response = requests.get(url, headers=headers, params=payload)
        result = response.json()["result"]
        currency_rate = {"currency": item, "rate": result}
        currency_rates_list.append(currency_rate)

    return currency_rates_list


# print(currency_rates('../user_settings.json', date=date_string))


def stock_information(path_user_settings: str) -> list[dict]:
    """Функция возвращает информацию по выбранным акциям"""

    try:
        with open(path_user_settings, "r", encoding="utf-8") as file:
            settings = json.load(file)
            stock_data = settings["user_stocks"]

        stock_prices_list = []
        url = "https://financialmodelingprep.com/stable/quote"
        load_dotenv("../.env")
        API_KEY = os.getenv("API_KEY_STOCK")
        headers = {"apikey": API_KEY}

        for item in stock_data:
            payload = {"symbol": item}

            response = requests.get(url, headers=headers, params=payload)
            result = response.json()[0]["price"]
            stock_data = {"stock": item, "price": result}
            stock_prices_list.append(stock_data)

        return stock_prices_list

    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return []


# print(stock_information('../user_settings.json'))
