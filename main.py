import json
import regex


DAY_POSITION = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "четверг": 3,
    "пятница": 4,
    "суббота": 5,
    "воскресенье": 6,
}


def get_time(time: str) -> tuple[int, int, int, int]:
    """
    Функция преобразует время в формате ММ1:ЧЧ1-ММ2:ЧЧ2
    в кортеж (ММ1, ЧЧ1, ММ2, ЧЧ2)
    """
    time_start = time.split("-")[0]
    time_end = time.split("-")[1]
    return (
        int(time_start.split(":")[0]),
        int(time_start.split(":")[1]),
        int(time_end.split(":")[0]),
        int(time_end.split(":")[1]),
    )


def init(filename: str) -> tuple[str, str, list]:
    """
    Функция запрашивает у пользователя день недели и время, в которое
    удобно пользователю купаться. Также, предзагружает список бассейнов.
    Возвращает кортеж (день недели, время, список бассейнов)
    """
    day_of_week_request = input("Введите день недели, в который хотите покупаться: ")

    while True:
        time_request = input("Введите часы в формате XX:XX-XX:XX. Нули тоже вводить ")
        if regex.match("^[0-2]\d:[0-2]\d-[0-2]\d:[0-2]\d$", time_request):
            time_request = get_time(time_request)
            break
        print("Введите правильно")

    with open(filename, "r", encoding="UTF-8") as file:
        records = json.load(file)

    return day_of_week_request, time_request, records


def compare_time(
    time_request: tuple[int, int, int, int], work_time: tuple[int, int, int, int]
):
    """
    Функция сравнивает кортежи 2-х времен. Возвращает True, когда
    time_request находится во внутреннем промежутке work_time, иначе False
    """
    compare_start_time = (time_request[0] > work_time[0]) or (
        time_request[0] == work_time[0] and time_request[1] >= work_time[1]
    )
    compare_end_time = (time_request[2] < work_time[2]) or (
        time_request[2] == work_time[2] and time_request[3] <= work_time[3]
    )
    if compare_start_time and compare_end_time:
        return True
    return False


def filter_pool(pool, day_of_week_request, time_request):
    for day in pool["WorkingHoursSummer"]:
        if day["DayOfWeek"] != day_of_week_request:
            continue
        work_time = get_time(day["Hours"])
        if compare_time(time_request, work_time):
            return True
    return False


def filter_pools(
    records: list[dict],
    day_of_week_request: str,
    time_request: tuple[int, int, int, int],
) -> list[dict]:
    """
    Функция фильтрует бассейны, подходящие пользователю по
    дню недели и времени
    """
    return [
        {
            "length": pool["DimensionsSummer"][0]["Length"],
            "width": pool["DimensionsSummer"][0]["Width"],
            "depth": pool["DimensionsSummer"][0]["Depth"],
            "pool_name": pool["ObjectName"],
            "address": f"{pool["AdmArea"]}, {pool["District"]}, {pool["Address"]}",
            "phone": pool["HelpPhone"],
            "paid": pool["Paid"],
            "work_hours": pool["WorkingHoursSummer"][DAY_POSITION
                                                     [day_of_week_request]
                                                     ][
                "Hours"
            ],
        }
        for pool in filter(
            lambda pool: filter_pool(pool, day_of_week_request, time_request),
            records
        )
    ]


def compare_max_pool(max_pool, **kwargs):
    length = kwargs.get("length", 30)
    width = kwargs.get("width", 50)
    depth = kwargs.get("depth", 80)
    return (
        length > max_pool["length"]
        or length == max_pool["length"]
        and width > max_pool["width"]
        or length == max_pool["length"]
        and width == max_pool["width"]
        and (depth is not None and depth > max_pool["depth"])
    )


def get_max_pool(pools_accepted: list[dict]):
    max_pool = {"length": -1, "width": -1, "depth": -1}

    for pool in pools_accepted:
        length = pool["length"]
        width = pool["width"]
        depth = pool["depth"]
        if compare_max_pool(max_pool, length=length, width=width, depth=depth):
            max_pool = pool
    return max_pool


def print_max_pool(max_pool: dict, day_of_week_request: str) -> None:
    print(
        f"""Вам подходит следующий бассейн:
        \rНазвание: {max_pool["pool_name"]}\

        \rДлина х Ширина х Высота: {max_pool["length"]} x {max_pool["width"]} x {max_pool["depth"]}

        \rАдрес: {max_pool["address"]}
        \rТелефон: {max_pool["phone"]}

        \rПлатный: {max_pool["paid"]}
        \rЧасы работы в {day_of_week_request}: {max_pool["work_hours"]}
        """
    )


def main():
    day_of_week_request, time_request, records = init("data2.json")
    filtered_pools = filter_pools(records, day_of_week_request, time_request)
    pool = get_max_pool(filtered_pools)
    print_max_pool(pool, day_of_week_request)


if __name__ == "__main__":
    main()
