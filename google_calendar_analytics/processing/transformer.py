import datetime

import pandas as pd


class AsyncDataTransformer:
    async def _get_duration(self, start, end) -> float:
        """
        A method to calculate the duration of an event
        """

        start_time = datetime.datetime.fromisoformat(start)
        end_time = datetime.datetime.fromisoformat(end)
        duration = end_time - start_time
        return round(duration.total_seconds() / 3600, 2)

    async def many_events_duration(
        self, events: list[dict], max_events: int = 5, ascending=False
    ) -> pd.DataFrame:
        """
        A method to calculate the duration of multiple events and return
        a DataFrame with the top events

        Args:
            events (list[dict]): A list of events
            max_events (int): The maximum number of events to be analyzed.
            ascending (bool): If True, sort the events in ascending order of duration
        """
        event_durations: dict[str, float] = {}

        for event in events:
            # Get the start and end times in ISO format
            start, end = event.get("start", {}).get("dateTime"), event.get(
                "end", {}
            ).get("dateTime")

            # If start and end times exist, calculate the duration and update the event durations dictionary
            if start and end:
                summary = event["summary"]
                duration = await self._get_duration(start, end)
                event_durations[summary] = event_durations.get(summary, 0) + duration

        events_series = pd.Series(event_durations)
        sorted_events = events_series.sort_values(ascending=ascending)
        top_events = sorted_events.iloc[:max_events]

        return pd.DataFrame({"Event": top_events.index, "Duration": top_events.values})

    async def one_event_duration(
        self, events: list[dict], event_name: str
    ) -> pd.DataFrame:
        """
        A method to calculate the duration of one event and return
        a DataFrame with the durations for each day

        Args:
            events (list[dict]): A list of events
            event_name (str): The name of the event to be analyzed
        """
        one_event: dict[str, float] = {}
        for event in events:
            if event["summary"] == event_name:
                start, end = event["start"]["dateTime"], event["end"]["dateTime"]
                duration = await self._get_duration(start, end)
                date = datetime.datetime.fromisoformat(start).strftime("%m.%d")
                one_event[date] = one_event.get(date, 0) + duration

        return pd.DataFrame(one_event.items(), columns=["Date", "Duration"])

    async def event_duration_periods(
        self,
        events: list[dict],
        event_name: str,
        period_days: int,
        num_periods: int,
    ) -> pd.DataFrame:
        """
        A method to calculate the duration of one event
        in multiple periods and return a DataFrame with the durations for each day

        Args:
            events (list[dict]): A list of events
            event_name (str): The name of the event to be analyzed
            period_days (int): The number of days in each period
            num_periods (int): The number of periods to be analyzed
        """
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
                            return pd.DataFrame(list(event_duration.values()))
