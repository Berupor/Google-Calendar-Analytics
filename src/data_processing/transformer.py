import datetime


class DataTransformer:
    def _get_duration(self, start, end) -> float:
        """
        A method to calculate the duration of an event
        """

        start_time = datetime.datetime.fromisoformat(start)
        end_time = datetime.datetime.fromisoformat(end)
        duration = end_time - start_time
        return round(duration.total_seconds() / 3600, 2)

    def many_events_duration(self, events, max_events=5, order=True) -> dict:
        """
        A method to calculate the total duration of many events
        """

        event_durations: dict[str, float] = {}

        for event in events:
            start, end = event.get("start", {}).get("dateTime"), event.get(
                "end", {}
            ).get("dateTime")
            if start and end:
                summary = event["summary"]
                duration = self._get_duration(start, end)
                event_durations[summary] = event_durations.get(summary, 0) + duration

        # Sort the events by duration (descending or ascending based on the value of `order`)
        sorted_events = dict(sorted(event_durations.items(), key=lambda x: x[1], reverse=order))  # type: ignore
        top_events = dict(list(sorted_events.items())[:max_events])
        return top_events

    def one_event_duration(self, events, event_name) -> dict:
        """
        A method to calculate the total duration of a single event
        """

        one_event: dict[str, float] = {}
        for event in events:
            if event["summary"] == event_name:
                start, end = event["start"]["dateTime"], event["end"]["dateTime"]
                duration = self._get_duration(start, end)
                date = datetime.datetime.fromisoformat(start)
                date_str = date.date().strftime("%m-%d")
                # Add the duration to the existing value for the date (if it exists)
                # or add a new key-value pair for the date
                if date_str in one_event:
                    one_event[date_str] += duration
                else:
                    one_event[date_str] = duration

        return one_event
