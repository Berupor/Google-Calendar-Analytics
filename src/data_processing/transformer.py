import datetime


class DataTransformer:
    def get_events_duration(self, events):
        event_durations = {}

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))

            start_time = datetime.datetime.fromisoformat(start)
            end_time = datetime.datetime.fromisoformat(end)

            duration = end_time - start_time
            duration_in_hours = round(duration.total_seconds() / 3600, 2)

            if event["summary"] in event_durations:
                event_durations[event["summary"]] += duration_in_hours
            else:
                event_durations[event["summary"]] = duration_in_hours

        return event_durations
