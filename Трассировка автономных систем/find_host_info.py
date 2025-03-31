import re
import requests


def info_seeker(host: str) -> dict:
    try:
        response = requests.get(f"http://ip-api.com/json/{host}").json()
        result = {
            "query": response.get("query", "Нет данных"),
            "as": response.get("as", "Нет данных"),
            "country": response.get("country", "Нет данных"),
            "isp": response.get("isp", "Нет данных"),
        }
        return result
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
