from owm_key import owm_api_key
import json
import requests

def get_weather_data(place, api_key=None):
    try:
        # Отправляем запрос к API OpenWeatherMap
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather',
            params={"q": place, "appid": api_key}
        )
        response.raise_for_status()  # Проверяем, успешен ли запрос (HTTP 200)
        
        # Разбираем JSON-ответ
        res_obj = response.json()
        
        # Форматируем данные
        formatted_data = {
            "name": res_obj.get("name"),
            "coord": {
                "lon": res_obj.get("coord", {}).get("lon"),
                "lat": res_obj.get("coord", {}).get("lat")
            },
            "country": res_obj.get("sys", {}).get("country"),
            "feels_like": round(res_obj.get("main", {}).get("feels_like", 0) - 273.15, 2),  # Перевод в Цельсии
            "timezone": f"UTC{res_obj.get('timezone', 0) // 3600:+d}"  # Рассчитываем смещение
        }

        # Выводим данные
        print(json.dumps(formatted_data, indent=4))

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except (KeyError, TypeError) as e:
        print(f"Ошибка обработки данных: {e}")


if __name__ == '__main__':
    # Вызываем функцию для нескольких городов
    get_weather_data('Moscow', api_key=owm_api_key)
    get_weather_data('Chicago', api_key=owm_api_key)
    get_weather_data('Dhaka', api_key=owm_api_key)
