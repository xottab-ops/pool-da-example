import regex


class Time:
    def __init__(self, hours=0, minutes=0, hours_and_minutes=None):
        if hours_and_minutes is not None:
            if not regex.match("[0-2]\\d:[0-5]\\d", hours_and_minutes):
                raise ValueError
            self.hours = int(hours_and_minutes.split(":")[0])
            self.minutes = int(hours_and_minutes.split(":")[1])
        else:
            self.hours = hours
            self.minutes = minutes

    def __str__(self):
        return f"{str(self.hours).zfill(2)}:{str(self.minutes).zfill(2)}"
