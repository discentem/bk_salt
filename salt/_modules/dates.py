from enum import Enum
import datetime

def __virtual__():
    return 'dates'

class WeekdayEnum(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

def Weekday(name: str) -> WeekdayEnum:
    try:
        return WeekdayEnum[name.upper()]  # Convert string to uppercase and get enum
    except KeyError:
        raise ValueError(f"Invalid weekday name: {name}")

def today_is(weekday: str) -> bool:
    weekday = Weekday(weekday)
    return datetime.datetime.now().weekday() == weekday.value

if __name__ == '__main__':
    print(today_is('monday'))  # True if today is Monday
    print(today_is('sunday'))  # False if today is not Sunday