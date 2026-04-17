import json
import logging
from src.utils import cards_data, currency_rates, data_from_excel, greetings, sort_by_payment, stock_information

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="../logs/views.log",
    filemode="w",
    encoding="utf-8",
)

main_logger = logging.getLogger("views")


def main_page(date: str) -> dict:
    """Функция принимает дату в формате YYYY-MM-DD HH:MM:SS и возвращает JSON файл
    после обработки входных данных во вспомогательных функциях"""

    final_data = {}
    try:
        final_data["greeting"] = greetings(date)
        main_logger.info(f'Сформировано приветствие: {final_data["greeting"]}')
    except Exception as e:
        main_logger.error(f"Функция greeting сработала с ошибкой: {e}")

    try:
        final_data["cards"] = cards_data(data_from_excel("../data/operations.xlsx"), date)
        main_logger.info(f'Сформирован список транзакций. Пример формата вывода: {final_data["cards"][0]}')
    except Exception as e:
        main_logger.error(f"Функция cards_data сработала с ошибкой: {e}")

    try:
        final_data["top_transactions"] = sort_by_payment(data_from_excel("../data/operations.xlsx"), date)
        main_logger.info(
            f'Сформирован список топ5 транзакций. Пример формата вывода: {final_data["top_transactions"][0]}'
        )
    except Exception as e:
        main_logger.error(f"Функция sort_by_payment сработала с ошибкой: {e}")

    try:
        final_data["currency_rates"] = currency_rates("../user_settings.json", date)
        main_logger.info(f'Получены курсы валют: {final_data["currency_rates"]}')
    except Exception as e:
        main_logger.error(f"Функция currency_rates сработала с ошибкой: {e}")

    try:
        final_data["stock_prices"] = stock_information("../user_settings.json")
        main_logger.info(f'Получены биржевые данные. Пример: {final_data["stock_prices"][0]}')
    except Exception as e:
        main_logger.error(f"Функция stock_information сработала с ошибкой: {e}")

    with open("../data/json_outputs/main_output.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

    return final_data

# print(main_page('2021-05-02 07:11:11'))
