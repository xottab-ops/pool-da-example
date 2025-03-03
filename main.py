import json
import regex
from classes import TimeRange, Pool


def init(filename: str) -> tuple[str, str, list]:
    """
    Функция запрашивает у пользователя день недели и время, в которое
    удобно пользователю купаться. Также, предзагружает список бассейнов.
    Возвращает кортеж (день недели, время, список бассейнов)
    """
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            records = json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError("Не удалось найти файл с данными. Файл должен лежать по пути data/data.json",
            e)

    day_of_week_request = input("Введите день недели, в который хотите покупаться: ")
    while True:
        time_request = input("Введите часы в формате XX:XX-XX:XX. Нули тоже вводить ")
        if regex.match("^[0-2]\\d:[0-5]\\d-[0-2]\\d:[0-5]\\d$", time_request):
            time_request = TimeRange(time_request)
            break
        print("Введите правильно")

    return day_of_week_request, time_request, records


def get_max_pool(max_pool, day_of_week_request, time_request, records):
    for record in records:
        pool = Pool(record)
        if pool.work_hours.working_days[day_of_week_request] is None:
            continue

        if (
            time_request in pool.work_hours.working_days[day_of_week_request]
            and max_pool < pool
        ):
            max_pool = pool

    return max_pool if max_pool.depth != -1 else None


def main():
    try:
        day_of_week_request, time_request, records = init("data/data2.json")
        max_pool_json = {"DimensionsSummer": [{"Length": -1, "Width": -1, "Depth": -1}]}
        max_pool = Pool(max_pool_json)

        max_pool = get_max_pool(max_pool, day_of_week_request, time_request, records)

        if max_pool is None:
            print("Подходящих бассейнов нет")
            return
        max_pool.print()
    except Exception as e:
        print("Непредвиденная ошибка:", e)


if __name__ == "__main__":
    main()
