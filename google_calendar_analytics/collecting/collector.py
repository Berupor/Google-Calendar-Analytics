from datetime import datetime

import aiohttp
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class AsyncCalendarDataCollector:
    """A class to collect data from a Google Calendar."""

    def __init__(self, creds: Credentials, session: aiohttp.ClientSession):
        self.service = build("calendar", "v3", credentials=creds)
        self.session = session
        self.creds = creds

    async def _make_request(self, request):
        """Make an API request using aiohttp.ClientSession."""
        try:
            url = request.uri
            headers = request.headers.copy()
            headers["Authorization"] = f"Bearer {self.creds.token}"

            async with self.session.get(url, headers=headers) as resp:
                return await resp.json()
        except aiohttp.ClientError as e:
            print(f"Error: {e}")
            return None

    async def _get_events_by_time_range(
            self,
            time_min: str,
            time_max: str,
            calendar_id: str,
    ) -> list:
        """Helper function to retrieve events in a specific time range."""
        events = []
        page_token = None

        while True:
            request = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
                pageToken=page_token,
            )

            response = await self._make_request(request)

            if response is None:
                break

            events.extend(response.get("items", []))
            page_token = response.get("nextPageToken")
            if not page_token:
                break

        return events

    async def collect_data(
            self,
            start_time: datetime,
            end_time: datetime,
            calendar_id: str = "primary",
    ) -> list:
        """Collect data from the calendar for the specified time range."""

        return await self._get_events_by_time_range(
            calendar_id=calendar_id,
            time_min=start_time.isoformat() + "Z",
            time_max=end_time.isoformat() + "Z",
        )
