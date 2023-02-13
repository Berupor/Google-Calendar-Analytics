import unittest

from src.data_processing.transformer import DataTransformer


class TestDataTransformer(unittest.TestCase):
    def setUp(self):
        self.events = [
            {
                "summary": "Meeting 1",
                "start": {
                    "dateTime": "2022-01-01T10:00:00+00:00",
                },
                "end": {
                    "dateTime": "2022-01-01T11:30:00+00:00",
                },
            },
            {
                "summary": "Meeting 2",
                "start": {
                    "dateTime": "2022-01-02T09:00:00+00:00",
                },
                "end": {
                    "dateTime": "2022-01-02T10:00:00+00:00",
                },
            },
            {
                "summary": "Meeting 1",
                "start": {
                    "dateTime": "2022-01-03T10:00:00+00:00",
                },
                "end": {
                    "dateTime": "2022-01-03T11:30:00+00:00",
                },
            },
        ]

    def test_get_duration(self):
        start = "2022-01-01T10:00:00+00:00"
        end = "2022-01-01T11:30:00+00:00"
        expected = 1.5
        result = DataTransformer._get_duration(start, end)
        self.assertEqual(result, expected)

    def test_many_events_duration(self):
        expected = {
            "Meeting 1": 3.0,
            "Meeting 2": 1.0,
        }
        result = DataTransformer.many_events_duration(self.events)
        self.assertEqual(result, expected)

    def test_one_event_duration(self):
        event_name = "Meeting 1"
        expected_result = {
            "01-01": 1.5,
            "01-03": 1.5,
        }

        result = DataTransformer.one_event_duration(self.events, event_name)
        self.assertDictEqual(result, expected_result)

        event_name = "Non-existent Event"
        expected_result = {}
        result = DataTransformer.one_event_duration(self.events, event_name)
        self.assertDictEqual(result, expected_result)

        event_name = "Meeting 2"
        expected_result = {"01-02": 1.0}
        result = DataTransformer.one_event_duration(self.events, event_name)
        self.assertDictEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
