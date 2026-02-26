from datetime import datetime, date, time
import calendar
from typing import List, Tuple, Optional
from dataclasses import dataclass
from logger import logger
from zoneinfo import ZoneInfo


@dataclass
class DateRange:
    start_date: date
    end_date: date

    def contained(self, current_date: date) -> bool:
        return self.start_date <= current_date <= self.end_date

    def is_invalid(self) -> bool:
        return self.start_date > self.end_date


class ScheduleConfig:
    def __init__(
        self,
        timezone: str,
        send_day: str,
        send_time: str,
        operation_range: Tuple[str, str],
        message: str,
        break_ranges: Optional[List[Tuple[str, str]]] = None,
    ):
        self.message = message
        self.timezone = timezone
        self.send_day = self._parse_day(send_day)
        self.send_time = self._parse_time(send_time)
        self.operation_range = self._parse_range(operation_range)
        self.break_ranges = self._parse_break_ranges(break_ranges or [])

    def _parse_day(self, day_str: str) -> int:
        try:
            return list(calendar.day_name).index(day_str.capitalize())
        except ValueError:
            raise ValueError(f"Invalid weekday: {day_str}")

    def _parse_time(self, time_str: str) -> time:
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError(f"Invalid time format (expected HH:MM): {time_str}")

    def _parse_date(self, date_str: str) -> date:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format (expected YYYY-MM-DD): {date_str}")

    def _parse_range(self, range_str: Tuple[str, str]) -> DateRange:
        start, end = range_str
        return DateRange(
            start_date=self._parse_date(start), end_date=self._parse_date(end)
        )

    def _parse_break_ranges(self, ranges: List[Tuple[str, str]]) -> List[DateRange]:
        parsed = []
        for date_range in ranges:
            date_range = self._parse_range(date_range)
            if date_range.is_invalid():
                raise ValueError(
                    f"Break start date {date_range.start_date} is after end date {date_range.end_date}"
                )
            parsed.append(date_range)
        return parsed

    def is_in_break(self, check_date: date) -> bool:
        for date_range in self.break_ranges:
            if date_range.contained(check_date):
                return True
        return False

    def should_send(self, now: Optional[datetime] = None) -> bool:
        """
        Returns True if message should be sent at this datetime.
        """
        now = now or datetime.now(ZoneInfo(self.timezone))
        today = now.date()

        if now.weekday() != self.send_day:
            return False

        if (
            now.time().hour != self.send_time.hour
            or now.time().minute != self.send_time.minute
        ):
            logger.info(
                "Current hour and minute don't match the specified hour and minute. Message will not be sent."
            )
            return False

        if not self.operation_range.contained(today):
            logger.info(
                "Current day is outside of the operation range. Message will not be sent."
            )
            return False

        if self.is_in_break(today):
            logger.info("Current day is within break period. Message will not be sent.")
            return False

        return True
