import unittest
from unittest.mock import MagicMock, patch

from src.data_collecting.collector import CalendarDataCollector


class CalendarDataCollectorTest(unittest.TestCase):
    def setUp(self):
        self.creds = MagicMock()
        self.collector = CalendarDataCollector(self.creds)

    @patch("src.data_collecting.collector.build")
    def test_collect_data_unsupported_range(self, build_mock):
        # Arrange
        collector = CalendarDataCollector(self.creds)

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            collector.collect_data("year")
        self.assertEqual(str(context.exception), "Unsupported range type: year")
