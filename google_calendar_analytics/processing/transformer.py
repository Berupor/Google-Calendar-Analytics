import datetime

import pandas as pd


class DataTransformer:
    def _get_duration(self, start, end) -> float:
        """
        A method to calculate the duration of an event
        """

        start_time = datetime.datetime.fromisoformat(start)
        end_time = datetime.datetime.fromisoformat(end)
        duration = end_time - start_time
        return round(duration.total_seconds() / 3600, 2)

    def many_events_duration(
            self, events: list[dict], max_events: int = 5, ascending=False
    ) -> pd.DataFrame:
        """
        A method to calculate the total duration of many events

        Args:
            events (list): A list of event objects with 'start' and 'end' times in ISO format and a 'summary' field.
            max_events (int): The maximum number of events to include in the output dataframe.
            ascending (bool): If True, sort the events in ascending order of duration.

        Returns:
            A pandas dataframe with columns 'Event' and 'Duration' for the top events by duration.
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
                duration = self._get_duration(start, end)
                event_durations[summary] = event_durations.get(summary, 0) + duration

        events_series = pd.Series(event_durations)
        sorted_events = events_series.sort_values(ascending=ascending)
        top_events = sorted_events.iloc[:max_events]

        return pd.DataFrame({"Event": top_events.index, "Duration": top_events.values})

    def one_event_duration(self, events: list[dict], event_name: str) -> pd.DataFrame:
        """
        A method to calculate the total duration of a single event

        Args:
            events: A list of events represented as dictionaries with start and end times.
            event_name: The name of the event to calculate the duration for.

        Returns:
            Returns a pandas DataFrame with the event's total duration for each date in the format 'MM.DD'.
            Columns 'Date' and 'Duration' display the date and the event's duration in hours, respectively.
        """

        one_event: dict[str, float] = {}
        for event in events:
            if event["summary"] == event_name:
                start, end = event["start"]["dateTime"], event["end"]["dateTime"]
                duration = self._get_duration(start, end)
                date = datetime.datetime.fromisoformat(start).strftime("%m.%d")
                one_event[date] = one_event.get(date, 0) + duration

        return pd.DataFrame(one_event.items(), columns=["Date", "Duration"])

    def event_duration_periods(
            self,
            events: list[dict],
            event_name: str,
            period_days: int,
            num_periods: int,
    ) -> pd.DataFrame:
        """
        A method to calculate the total duration of a single event for the current and previous periods.

        Args:
            events: A list of events represented as dictionaries with start and end times.
            event_name: The name of the event to calculate the duration for.
            period_days: The number of days in each period.
            num_periods: The number of periods to calculate.

        Returns:
            Returns a pandas DataFrame with the event's total duration for each day in the format 'YYYY-MM-DD'.
            Columns 'Date', 'Day', and 'Duration' display the date, the day number within each period, and the event's duration in hours, respectively.
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
                duration = self._get_duration(start, end)
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
