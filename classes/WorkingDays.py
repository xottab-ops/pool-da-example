from .TimeRange import TimeRange


class WorkingDays:
    def __init__(self, work_days_list):
        self.working_days = {}
        for day in work_days_list:
            if day["Hours"] == "закрыто":
                self.working_days[day["DayOfWeek"]] = None
                continue
            self.working_days[day["DayOfWeek"]] = TimeRange(day["Hours"])
