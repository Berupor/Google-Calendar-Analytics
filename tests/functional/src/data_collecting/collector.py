import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from google_calendar_analytics.collecting.collector import CalendarDataCollector


class CalendarDataCollectorTest(unittest.TestCase):
    def setUp(self):
        self.creds = MagicMock()
        self.collector = CalendarDataCollector(self.creds)

    @patch.object(CalendarDataCollector, "_get_events_by_time_range")
    def test_collect_data(self, mock_get_events):
        # Arrange
        start_time = datetime(2023, 3, 1, 0, 0, 0)
        end_time = datetime(2023, 3, 2, 0, 0, 0)
        expected_events = [{"id": "event1"}, {"id": "event2"}]
        mock_get_events.return_value = expected_events

        # Act
        actual_events = self.collector.collect_data(start_time, end_time)

        # Assert
        self.assertEqual(actual_events, expected_events)
        mock_get_events.assert_called_once_with(
            calendar_id="primary",
            time_min=start_time.isoformat() + "Z",
            time_max=end_time.isoformat() + "Z",
        )
