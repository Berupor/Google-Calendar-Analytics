import unittest

import matplotlib.pyplot as plt

from src.visualization.visualizer_factory import PlotFactory


class TestPlot(unittest.TestCase):
    def setUp(self):
        self.events = {
            "Event 1": 10,
            "Event 2": 5,
            "Event 3": 15,
        }
        self.title = "Test Title"
        self.event_name = "Event 1"

    def test_pie_plot(self):
        plot = PlotFactory("Pie")
        result = plot.plot(self.events)
        self.assertEqual(result, plt)

    def test_bar_plot(self):
        plot = PlotFactory("Bar")
        result = plot.plot(self.events)
        self.assertEqual(result, plt)

    def test_line_plot(self):
        plot = PlotFactory("Line")
        result = plot.plot(self.events, event_name="Event 1")
        self.assertEqual(result, plt)

    def test_invalid_plot_type(self):
        with self.assertRaises(ValueError):
            PlotFactory("Invalid")


if __name__ == "__main__":
    unittest.main()
