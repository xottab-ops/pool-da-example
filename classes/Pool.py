from .Address import Address
from .WorkingDays import WorkingDays


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

    def __lt__(self, other):
        return (
            self.length < other.length
            or self.length == other.length
            and self.width < other.width
            or self.length == other.length
            and self.width == other.width
            and (self.depth is not None and self.depth < other.depth)
        )
