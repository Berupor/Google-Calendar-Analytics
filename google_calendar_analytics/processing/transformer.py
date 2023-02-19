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

        event_durations = {}

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

        one_event = {}
        for event in events:
            if event["summary"] == event_name:
                start, end = event["start"]["dateTime"], event["end"]["dateTime"]
                duration = self._get_duration(start, end)
                date = datetime.datetime.fromisoformat(start).strftime("%m.%d")
                one_event[date] = one_event.get(date, 0) + duration

        return pd.DataFrame(one_event.items(), columns=["Date", "Duration"])
