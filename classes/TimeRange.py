from .Time import Time


class TimeRange:
    def __init__(self, time_range):
        self.time_start = Time(hours_and_minutes=time_range.split("-")[0])
        self.time_end = Time(hours_and_minutes=time_range.split("-")[1])

    def __contains__(self, time: Time):
        compare_start_time = (time.time_start.hours >= self.time_start.hours) or (
            time.time_start.hours == self.time_start.hours
            and time.time_start.minutes >= self.time_start.minutes
        )
        compare_end_time = (time.time_end.hours <= self.time_end.hours) or (
            time.time_end.hours == self.time_end.hours
            and time.time_end.minutes <= self.time_end.minutes
        )
        return compare_start_time and compare_end_time

    def __str__(self):
        return f"{self.time_start}-{self.time_end}"
