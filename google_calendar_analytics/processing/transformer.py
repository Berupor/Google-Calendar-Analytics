import datetime
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from google_calendar_analytics.core import exceptions


class EventDurationStrategy(ABC):
    """
    Abstract base class for event duration strategies.
    """

    @abstractmethod
    async def calculate_duration(
            self, events: list[dict], *args, **kwargs
    ) -> pd.DataFrame:
        """
        Calculate event durations.

        Args:
            events (list[dict]): List of event dictionaries.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            pandas.DataFrame: Dataframe containing event durations.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """

        pass

    async def _get_duration(self, start, end) -> float:
        """
        Calculate the duration between two dates in hours.

        Args:
            start (str): ISO-formatted start date.
            end (str): ISO-formatted end date.

        Returns:
            float: Duration between start and end dates in hours.
        """
        start_time = datetime.datetime.fromisoformat(start)
        end_time = datetime.datetime.fromisoformat(end)
        duration = end_time - start_time
        return np.round(duration.total_seconds() / 3600, 2)


class ManyEventsDurationStrategy(EventDurationStrategy):
    """
    A strategy for calculating the duration of many events.

    Args:
        EventDurationStrategy (ABC): Abstract base class for event duration strategies.
    """

    async def calculate_duration(  # type: ignore
            self, events: list[dict], max_events: int = 5, ascending=False
    ) -> pd.DataFrame:
        event_durations = {}  # type: ignore

        for event in events:
            start, end = event.get("start", {}).get("dateTime"), event.get(
                "end", {}
            ).get("dateTime")

            if start and end:
                summary = event["summary"]
                duration = await self._get_duration(start, end)
                event_durations[summary] = event_durations.get(summary, 0) + duration

        events_series = pd.Series(event_durations)
        sorted_events = events_series.sort_values(ascending=ascending)
        top_events = sorted_events.iloc[:max_events]

        return pd.DataFrame({"Event": top_events.index, "Duration": top_events.values})


class OneEventDurationStrategy(EventDurationStrategy):
    """
    A strategy for calculating the duration of a single event.

    Args:
        EventDurationStrategy (ABC): Abstract base class for event duration strategies.
    """

    async def calculate_duration(self, events: list[dict], event_name: str) -> pd.DataFrame:  # type: ignore
        one_event: dict[str, float] = {}
        for event in events:
            if event["summary"] == event_name:
                start, end = event["start"]["dateTime"], event["end"]["dateTime"]
                duration = await self._get_duration(start, end)
                date = datetime.datetime.fromisoformat(start).strftime("%m.%d")
                one_event[date] = one_event.get(date, 0) + duration

        return pd.DataFrame(one_event.items(), columns=["Date", "Duration"])


class EventDurationPeriodsStrategy(EventDurationStrategy):
    """
    A strategy for calculating the duration of events in periods.

    Args:
        EventDurationStrategy (ABC): Abstract base class for event duration strategies.
    """

    async def calculate_duration(  # type: ignore
            self,
            events: list[dict],
            event_name: str,
            period_days: int,
            num_periods: int,
    ) -> pd.DataFrame:
        period_duration = datetime.timedelta(days=period_days)
        periods = []

        for i in range(num_periods):
            period_end = (
                    datetime.datetime.now().date()
                    - datetime.timedelta(days=datetime.datetime.now().weekday())
                    - period_duration * i
            )
            period_start = period_end - period_duration + datetime.timedelta(days=1)
            periods.append((period_start, period_end))

        event_duration = {}  # type: ignore
        for event in events:
            if event["summary"] == event_name:
                start, end = event["start"]["dateTime"], event["end"]["dateTime"]
                duration = await self._get_duration(start, end)
                date = datetime.datetime.fromisoformat(start).date()

                for period_index, (period_start, period_end) in enumerate(periods):
                    if period_start <= date <= period_end:
                        day_number = (date - period_start).days + 1
                        date_str = date
                        if date_str in event_duration:
                            event_duration[date_str]["Duration"] += duration
                        else:
                            event_duration[date_str] = {
                                "Date": date_str,
                                "Day": day_number,
                                "Duration": duration,
                                "Period": period_index,
                            }
        expected_data_points = num_periods * period_days
        available_data_points = len(event_duration)

        if available_data_points < expected_data_points:
            raise exceptions.NotEnoughDataError(
                expected_data_points, available_data_points
            )

        return pd.DataFrame(list(event_duration.values()))


class AsyncDataTransformer:
    def __init__(self):
        self.strategy: EventDurationStrategy = None  # type: ignore

    def set_strategy(self, strategy: EventDurationStrategy) -> None:
        self.strategy = strategy

    async def calculate_duration(
            self, events: list[dict], *args, **kwargs
    ) -> pd.DataFrame:
        if not self.strategy:
            raise ValueError("Strategy is not set")

        return await self.strategy.calculate_duration(events, *args, **kwargs)
