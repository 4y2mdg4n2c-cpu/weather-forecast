import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KEY')
def get_unique_dates(data):
    unique_dates = []
    for item in data['list']:
        date = item['dt_txt'].split(' ')[0]
        if date not in unique_dates:
            unique_dates.append(date)
    return unique_dates[:3]
def get_weather_for_day(data, date):
    night_temp = []
    morning_temp = []
    days_temp = []
    evening_temp = []
    for item in data['list']:
        dt_date, dt_time = item['dt_txt'].split(' ')
        if dt_date != date:
            continue
        hour = int(dt_time.split(':')[0])
        if 0 <= hour < 6:
            night_temp.append(item['main']['temp'])
        elif hour >= 6 and hour < 12:
            morning_temp.append(item['main']['temp'])
        elif hour >= 12 and hour < 18:
            days_temp.append(item['main']['temp'])
        elif hour >= 18 and hour < 24:
            evening_temp.append(item['main']['temp'])
    return night_temp, morning_temp, days_temp, evening_temp
def calc_avg(values):
    if values:
        return round(sum(values) / len(values), 2)
    return None 
def get_print_weather(data, city):
    dates = get_unique_dates(data)
    print(f'\nПогода в городе {city}\n')
    for date in dates:
        night_temp, morning_temp, days_temp, evening_temp = get_weather_for_day(data, date)
        avg_night_temp = calc_avg(night_temp)
        avg_morning_temp = calc_avg(morning_temp)
        avg_days_temp = calc_avg(days_temp)
        avg_evening_temp = calc_avg(evening_temp)
        print(f"Дата: {date}")
        print(f"Ночь: {avg_night_temp if avg_night_temp is not None else 'Нет данных'}°C")
        print(f"Утро: {avg_morning_temp if avg_morning_temp is not None else 'Нет данных'}°C")
        print(f"День: {avg_days_temp if avg_days_temp is not None else 'Нет данных'}°C")
        print(f"Вечер: {avg_evening_temp if avg_evening_temp is not None else 'Нет данных'}°C")
        print("-" * 30)
def main():
    while True:
        city = input("Введите название города (или 'exit' для выхода): ")
        if city.lower() == 'exit':
            print("Выход из программы.")
            break
        if city.strip() == "":
            print("Название города не может быть пустым.")
            continue
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                get_print_weather(data, city)
            else:
                print('Ошибка: Город не найден или API недоступен.')
        except requests.RequestException:
            print(f"Ошибка: нет соединения с интернетом")
if __name__ == "__main__":
        main()