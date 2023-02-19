import unittest

import pandas as pd

from google_calendar_analytics.processing.transformer import DataTransformer


class DataTransformerTest(unittest.TestCase):
    def setUp(self):
        self.transformer = DataTransformer()

    def test__get_duration(self):
        start_time = "2022-02-18T09:00:00+00:00"
        end_time = "2022-02-18T10:30:00+00:00"
        expected_duration = 1.5
        duration = self.transformer._get_duration(start_time, end_time)

        self.assertAlmostEqual(duration, expected_duration, delta=0.01)

    def test_many_events_duration(self):
        events = [
            {"start": {"dateTime": "2022-02-18T09:00:00+00:00"}, "end": {"dateTime": "2022-02-18T10:30:00+00:00"},
             "summary": "Meeting 1"},
            {"start": {"dateTime": "2022-02-18T11:00:00+00:00"}, "end": {"dateTime": "2022-02-18T12:30:00+00:00"},
             "summary": "Meeting 2"},
            {"start": {"dateTime": "2022-02-18T13:00:00+00:00"}, "end": {"dateTime": "2022-02-18T14:30:00+00:00"},
             "summary": "Meeting 3"},
        ]
        expected_output = pd.DataFrame({"Event": ["Meeting 1", "Meeting 2", "Meeting 3"], "Duration": [1.5, 1.5, 1.5]})
        output = self.transformer.many_events_duration(events, max_events=3, ascending=False)

        pd.testing.assert_frame_equal(output, expected_output)

    def test_one_event_duration(self):
        events = [
            {"start": {"dateTime": "2022-02-18T09:00:00+00:00"}, "end": {"dateTime": "2022-02-18T10:30:00+00:00"},
             "summary": "Meeting 1"},
            {"start": {"dateTime": "2022-02-18T11:00:00+00:00"}, "end": {"dateTime": "2022-02-18T12:30:00+00:00"},
             "summary": "Meeting 1"},
            {"start": {"dateTime": "2022-02-18T13:00:00+00:00"}, "end": {"dateTime": "2022-02-18T14:30:00+00:00"},
             "summary": "Meeting 2"},
        ]
        expected_output = pd.DataFrame({"Date": ["02.18"], "Duration": [3.0]})
        output = self.transformer.one_event_duration(events, "Meeting 1")
        pd.testing.assert_frame_equal(output, expected_output)
