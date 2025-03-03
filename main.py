import json
import regex


def get_time(time: str):
    time_start = time.split("-")[0]
    time_end = time.split("-")[1]
    return (
        int(time_start.split(":")[0]),
        int(time_start.split(":")[1]),
        int(time_end.split(":")[0]),
        int(time_end.split(":")[1]),
    )


day_of_week_request = input("Введите день недели, в который хотите покупаться: ")

while True:
    time_request = input("Введите часы в формате XX:XX-XX:XX. Нули тоже вводить ")
    if regex.match("^[0-2]\d:[0-2]\d-[0-2]\d:[0-2]\d$", time_request):
        time_request = get_time(time_request)
        break
    print("Введите правильно")


with open("data2.json", "r", encoding="UTF-8") as file:
    records = json.load(file)

pools_accepted = []

for pool in records:
    for day in pool["WorkingHoursSummer"]:
        if day["DayOfWeek"] != day_of_week_request:
            continue
        work_time = get_time(day["Hours"])
        if (
            (time_request[0] > work_time[0])
            or (time_request[0] == work_time[0] and time_request[1] >= work_time[1])
        ) and (
            (time_request[2] < work_time[3])
            or (time_request[2] == work_time[3] and time_request[2] <= work_time[3])
        ):

            pools_accepted.append(
                {
                    "length": pool["DimensionsSummer"][0]["Length"],
                    "width": pool["DimensionsSummer"][0]["Width"],
                    "depth": pool["DimensionsSummer"][0]["Depth"],
                    "pool_name": pool["ObjectName"],
                    "address": f"{pool["AdmArea"]}, {pool["District"]}, {pool["Address"]}",
                    "phone": pool["HelpPhone"],
                    "paid": pool["Paid"],
                    "work_hours": day["Hours"],
                }
            )

max_pool = {"length": -1, "width": -1, "depth": -1}

for pool in pools_accepted:
    length = pool["length"]
    width = pool["width"]
    depth = pool["depth"]
    if (
        length > max_pool["length"]
        or length == max_pool["length"]
        and width > max_pool["width"]
        or length == max_pool["length"]
        and width == max_pool["width"]
        and (depth is not None and depth > max_pool["depth"])
    ):
        max_pool = pool

print(
    f"""Вам подходит следующий бассейн: 
Название: {max_pool["pool_name"]}\

Длина х Ширина х Высота: {max_pool["length"]} x {max_pool["width"]} x {max_pool["depth"]}

Адрес: {max_pool["address"]}
Телефон: {max_pool["phone"]}

Платный: {max_pool["paid"]}
Часы работы в {day_of_week_request}: {max_pool["work_hours"]}
"""
)
