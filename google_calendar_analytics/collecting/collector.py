import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from googleapiclient.discovery import build  # type: ignore


class AsyncCalendarDataCollector:
    """A class to collect data from a Google Calendar."""

    def __init__(self, creds):
        self.service = build("calendar", "v3", credentials=creds, cache_discovery=True)

    async def _get_events_by_time_range(
        self,
        time_min: str,
        time_max: str,
        calendar_id: str,
        thread_pool: ThreadPoolExecutor,
    ) -> list:
        """Helper function to retrieve events in a specific time range."""
        request = self.service.events().list(
            calendarId=calendar_id,

            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
        )

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(thread_pool, request.execute)
        events = response.get("items", [])
        return events

    async def collect_data(
        self,
        start_time: datetime,
        end_time: datetime,
        calendar_id: str = "primary",
        thread_pool: ThreadPoolExecutor = None,  # type: ignore
    ) -> list:
        """Collect data from the calendar for the specified time range."""
        if not thread_pool:
            thread_pool = ThreadPoolExecutor()

        try:
            events = await self._get_events_by_time_range(
                calendar_id=calendar_id,
                time_min=start_time.isoformat() + "Z",
                time_max=end_time.isoformat() + "Z",
                thread_pool=thread_pool,
            )
        except Exception as e:
            print(f"Error: {e}")
            events = []

        return events
