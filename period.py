"""
Get since and before values for date.
"""
import datetime
from typing import Optional


class Period:

    def get(self, period: str = None) -> Optional[tuple[str, str]]:
        """Available values (day, week, month, year)."""
        if period in dir(self):
            class_method = getattr(self, period)
            return class_method()
        return

    def day(self) -> tuple[str, str]:
        now = datetime.datetime.utcnow()
        since = now - datetime.timedelta(days=1)
        return (str(since), str(now))

    def week(self) -> tuple[str, str]:
        now = datetime.datetime.utcnow()
        since = now - datetime.timedelta(days=7)
        return (str(since), str(now))

    def month(self) -> tuple[str, str]:
        now = datetime.datetime.utcnow()
        since = now - datetime.timedelta(days=30)
        return (str(since), str(now))

    def year(self) -> tuple[str, str]:
        now = datetime.datetime.utcnow()
        since = now - datetime.timedelta(days=365)
        return (str(since), str(now))

    def today(self) -> tuple[str, str]:
        current_day = datetime.date.today()
        next_day = current_day + datetime.timedelta(days=1)
        return (str(current_day), str(next_day))

    def last_day(self) -> tuple[str, str]:
        current_day = datetime.date.today()
        prev_day = current_day - datetime.timedelta(days=1)
        return (str(prev_day), str(current_day))

    def current_month(self) -> tuple[str, str]:
        current_month_date = datetime.date.today().replace(day=1)
        last_day = self.last_day_of_month(
            current_month_date) + datetime.timedelta(days=1)
        return (str(current_month_date), str(last_day))

    def current_year(self) -> tuple[str, str]:
        year = datetime.date.today().year
        return (f'{year}-01-01', f'{year+1}-01-01')

    def last_month(self) -> tuple[str, str]:
        last_month = datetime.date.today().month - 1
        current_year = datetime.date.today().year

        if last_month == 0:
            last_month = 12
            current_year -= 1

        last_month_date = datetime.date.today().replace(
            day=1, month=last_month, year=current_year)
        last_day = self.last_day_of_month(
            last_month_date) + datetime.timedelta(days=1)
        return (str(last_month_date), str(last_day))

    def last_year(self) -> tuple[str, str]:
        year = datetime.date.today().year
        return (f'{year - 1}-01-01', f'{year}-01-01')

    def last_day_of_month(self, day) -> datetime.date:
        # this will never fail
        # get close to the end of the month for any day, and add 4 days 'over'
        next_month = day.replace(day=28) + datetime.timedelta(days=4)
        # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
        return next_month - datetime.timedelta(days=next_month.day)
