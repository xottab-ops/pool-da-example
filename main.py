import json
import regex


class Time:
    def __init__(self, hours=0, minutes=0, hours_and_minutes=None):
        if hours_and_minutes is not None:
            if not regex.match("[0-2]\d:[0-5]\d", hours_and_minutes):
                raise ValueError
            self.hours = int(hours_and_minutes.split(":")[0])
            self.minutes = int(hours_and_minutes.split(":")[1])
        else:
            self.hours = hours
            self.minutes = minutes

    def __str__(self):
        return f"{str(self.hours).zfill(2)}:{str(self.minutes).zfill(2)}"


class TimeRange:
    def __init__(self, time_range):
        self.time_start = Time(hours_and_minutes=time_range.split("-")[0])
        self.time_end = Time(hours_and_minutes=time_range.split("-")[1])

    def inner(self, time):
        compare_start_time = (self.time_start.hours > time.time_start.hours) or (
            self.time_start.hours == time.time_start.hours
            and self.time_start.minutes >= time.time_start.minutes
        )
        compare_end_time = (self.time_end.hours < time.time_end.hours) or (
            self.time_end.hours == time.time_end.hours
            and self.time_end.minutes <= time.time_end.minutes
        )
        return compare_start_time and compare_end_time

    def __str__(self):
        return f"{self.time_start}-{self.time_end}"


class WorkingDays:
    def __init__(self, work_days_list):
        self.working_days = {}
        for day in work_days_list:
            if day["Hours"] == "закрыто":
                self.working_days[day["DayOfWeek"]] = None
                continue
            self.working_days[day["DayOfWeek"]] = TimeRange(day["Hours"])


class Address:
    def __init__(self, admin_area, district, address):
        self.admin_area = admin_area
        self.district = district
        self.address = address

    def __str__(self):
        return f"{self.admin_area}, {self.district}, {self.address}"


class Pool:
    def __init__(self, json):
        self.name = json.get("ObjectName", None)
        self.address = Address(
            json.get("AdmArea", None),
            json.get("District", None),
            json.get("Address", None),
        )
        self.phone = json.get("HelpPhone", None)
        self.paid = json.get("paid", None)
        self.website = json.get("WebSite", None)
        if json.get("WorkingHoursSummer", None) is not None:
            self.work_hours = WorkingDays(json.get("WorkingHoursSummer", None))
        self.length = json.get("DimensionsSummer", None)[0]["Length"]
        self.width = json.get("DimensionsSummer", None)[0]["Width"]
        self.depth = json.get("DimensionsSummer", None)[0]["Depth"]

    def __str__(self):
        return self.name

    def __get_work_time(self, day_of_week):
        return self.work_hours.working_days[day_of_week]

    def __print_working_hours(self):
        for day in self.work_hours.working_days:
            print(f"{day} - {self.__get_work_time(day)}")

    def print(self):
        print(
            f"""Название: {self.name}\

            \rДлина х Ширина х Высота: {self.length} x {self.width} x {self.depth}

            \rАдрес: {self.address}
            \rТелефон: {self.phone}

            \rПлатный: {self.paid}
            """
        )
        self.__print_working_hours()

    def compare(self, pool):
        return (
            self.length > pool.length
            or self.length == pool.length
            and self.width > pool.width
            or self.length == pool.length
            and self.width == pool.width
            and (self.depth is not None and self.depth > pool.depth)
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
        if regex.match("^[0-2]\d:[0-5]\d-[0-2]\d:[0-5]\d$", time_request):
            time_request = TimeRange(time_request)
            break
        print("Введите правильно")

    with open(filename, "r", encoding="UTF-8") as file:
        records = json.load(file)

    return day_of_week_request, time_request, records


def get_max_pool(max_pool, day_of_week_request, time_request, records):
    for record in records:
        pool = Pool(record)
        if pool.work_hours.working_days[day_of_week_request] is None:
            continue
        if not time_request.inner(pool.work_hours.working_days[day_of_week_request]):
            continue
        if not pool.compare(max_pool):
            continue
        max_pool = pool

    return max_pool if max_pool.depth != -1 else None


def main():
    day_of_week_request, time_request, records = init("data2.json")
    max_pool_json = {"DimensionsSummer": [
        {"Length": -1,
         "Width": -1,
         "Depth": -1}
         ]
         }
    max_pool = Pool(max_pool_json)

    max_pool = get_max_pool(max_pool,
                            day_of_week_request,
                            time_request,
                            records
                            )

    if max_pool is None:
        print("Подходящих бассейнов нет")
        return
    max_pool.print()


if __name__ == "__main__":
    main()
