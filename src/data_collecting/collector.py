import datetime
from datetime import timedelta

from googleapiclient.discovery import build

from core.config import settings


class CalendarDataCollector:
    TIME_RANGE_MAP = {"day": 1, "week": 7, "month": 30}

    def __init__(self, creds):
        self.service = build("calendar", "v3", credentials=creds)

    def _get_events_by_time_range(
        self,
        time_min,
        time_max,
        calendar_id: str,
    ) -> list:
        """Helper function to retrieve events in a specific time range."""
        events_result = (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])

    def collect_data(
        self, time_range: str, calendar_id: str = settings.profile.calendar_id
    ) -> list:
        """Collect data from the calendar for the specified time range."""
        now = datetime.datetime.now()

        if time_range not in self.TIME_RANGE_MAP:
            raise ValueError(f"Unsupported range type: {time_range}")

        # Get the start and end times based on the range type
        start_time = now - timedelta(days=self.TIME_RANGE_MAP[time_range])
        start = start_time.replace(hour=0, minute=0, second=0)
        end = now.replace(hour=23, minute=59, second=59)

        events = self._get_events_by_time_range(
            calendar_id=calendar_id,
            time_min=start.isoformat() + "Z",
            time_max=end.isoformat() + "Z",
        )

        return events
