import datetime
import operator


class DataTransformer:
    @staticmethod
    def _get_duration(start, end):
        start_time = datetime.datetime.fromisoformat(start)
        end_time = datetime.datetime.fromisoformat(end)

        duration = end_time - start_time
        duration_in_hours = round(duration.total_seconds() / 3600, 2)
        return duration_in_hours

    @staticmethod
    def _update_event_durations(event, event_durations):
        duration = DataTransformer._get_duration(
            event["start"]["dateTime"], event["end"]["dateTime"]
        )
        if event["summary"] in event_durations:
            event_durations[event["summary"]] += duration
        else:
            event_durations[event["summary"]] = duration

    @staticmethod
    def many_events_duration(events, max_events=5, order=True) -> dict:
        event_durations = {}

        for event in events:
            if "dateTime" in event["start"] and "dateTime" in event["end"]:
                DataTransformer._update_event_durations(event, event_durations)

        sorted_events = dict(
            sorted(event_durations.items(), key=operator.itemgetter(1), reverse=order)
        )
        top_events = dict(list(sorted_events.items())[:max_events])

        return top_events

    @staticmethod
    def one_event_duration(events, event_name):
        one_event = {}

        for event in events:
            if event["summary"] == event_name:
                duration = DataTransformer._get_duration(
                    event["start"]["dateTime"], event["end"]["dateTime"]
                )
                date = datetime.datetime.fromisoformat(event["start"]["dateTime"])
                one_event[date.date().strftime("%m-%d")] = duration

        return one_event
