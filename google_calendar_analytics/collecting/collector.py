from datetime import datetime

from googleapiclient.discovery import build  # type: ignore


class CalendarDataCollector:
    """A class to collect data from a Google Calendar."""

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
        self, start_time: datetime, end_time: datetime, calendar_id: str = "primary"
    ) -> list:
        """Collect data from the calendar for the specified time range."""

        events = self._get_events_by_time_range(
            calendar_id=calendar_id,
            time_min=start_time.isoformat() + "Z",
            time_max=end_time.isoformat() + "Z",
        )
        return events
