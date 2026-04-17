import json
import logging

from utils import greetings, data_from_excel, cards_data, sort_by_payment, currency_rates, stock_information


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='../logs/views.log',
                    filemode='w',
                    encoding='utf-8')

main_logger = logging.getLogger('views')


def main_page(date: str)-> dict:
    """Функция принимает дату в формате YYYY-MM-DD HH:MM:SS и возвращает JSON файл после обработки входных данных во вспомогательных функциях"""

    final_data = {}
    try:
        final_data["greeting"] = greetings(date)
        main_logger.info(f'Сформировано приветствие: {final_data["greeting"]}')
    except Exception as e:
        main_logger.error('Функция greeting сработала с ошибкой')

    try:
        final_data["cards"] = cards_data(data_from_excel('../data/operations.xlsx'), date)
        main_logger.info(f'Сформирован список транзакций. Пример формата вывода: {final_data["cards"][0]}')
    except Exception as e:
        main_logger.error('Функция cards_data сработала с ошибкой')

    try:
        final_data["top_transactions"] = sort_by_payment(data_from_excel('../data/operations.xlsx'), date)
        main_logger.info(f'Сформирован список топ5 транзакций. Пример формата вывода: {final_data["top_transactions"][0]}')
    except Exception as e:
        main_logger.error('Функция sort_by_payment сработала с ошибкой')

    try:
        final_data["currency_rates"] = currency_rates('../user_settings.json', date)
        main_logger.info(f'Получены курсы валют: {final_data["currency_rates"]}')
    except Exception as e:
        main_logger.error('Функция currency_rates сработала с ошибкой')

    try:
        final_data["stock_prices"] = stock_information('../user_settings.json')
        main_logger.info(f'Получены биржевые данные. Пример: {final_data["stock_prices"][0]}')
    except Exception as e:
        main_logger.error('Функция stock_information сработала с ошибкой')

    with open('../data/json_outputs/main_output.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)



    return final_data



# print(main_page('2021-05-02 07:11:11'))









# Топ-5 транзакций по сумме платежа.
# Курс валют.
# Стоимость акций из S&P500.
# Пример структуры JSON-ответа
# {
#   "greeting": "Добрый день",
#   "cards": [
#     {
#       "last_digits": "5814",
#       "total_spent": 1262.00,
#       "cashback": 12.62
#     },
#     {
#       "last_digits": "7512",
#       "total_spent": 7.94,
#       "cashback": 0.08
#     }
#   ],
#   "top_transactions": [
#     {
#       "date": "21.12.2021",
#       "amount": 1198.23,
#       "category": "Переводы",
#       "description": "Перевод Кредитная карта. ТП 10.2 RUR"
#     },
#     {
#       "date": "20.12.2021",
#       "amount": 829.00,
#       "category": "Супермаркеты",
#       "description": "Лента"
#     },
#     {
#       "date": "20.12.2021",
#       "amount": 421.00,
#       "category": "Различные товары",
#       "description": "Ozon.ru"
#     },
#     {
#       "date": "16.12.2021",
#       "amount": -14216.42,
#       "category": "ЖКХ",
#       "description": "ЖКУ Квартира"
#     },
#     {
#       "date": "16.12.2021",
#       "amount": 453.00,
#       "category": "Бонусы",
#       "description": "Кешбэк за обычные покупки"
#     }
#   ],
#   "currency_rates": [
#     {
#       "currency": "USD",
#       "rate": 73.21
#     },
#     {
#       "currency": "EUR",
#       "rate": 87.08
#     }
#   ],
#   "stock_prices": [
#     {
#       "stock": "AAPL",
#       "price": 150.12
#     },
#     {
#       "stock": "AMZN",
#       "price": 3173.18
#     },
#     {
#       "stock": "GOOGL",
#       "price": 2742.39
#     },
#     {
#       "stock": "MSFT",
#       "price": 296.71
#     },
#     {
#       "stock": "TSLA",
#       "price": 1007.08
#     }
#   ]
# }