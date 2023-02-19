import unittest

import pandas as pd
import plotly.graph_objs as go

from google_calendar_analytics.visualization.visualizer_factory import BarPlot, LinePlot, PiePlot, PlotFactory


class TestPlots(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({"Event": ["A", "B", "C", "D"],
                                "Duration": [10, 20, 30, 40]})

    def test_pie_plot(self):
        plot = PiePlot()
        fig = plot.plot(self.df, "Pie Chart Title")
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, "Pie Chart Title")
        self.assertEqual(fig.layout.width, 800)
        self.assertEqual(fig.layout.height, 400)

    def test_bar_plot(self):
        plot = BarPlot()
        fig = plot.plot(self.df, "Bar Chart Title")
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, "Bar Chart Title")
        self.assertEqual(fig.layout.width, 800)
        self.assertEqual(fig.layout.height, 400)

    def test_line_plot(self):
        df = pd.DataFrame({"Date": pd.date_range(start="2022-01-01", periods=10, freq="D"),
                           "Duration": [10, 20, 30, 40, 50, 40, 30, 20, 10, 5]})
        plot = LinePlot()
        fig = plot.plot(df, "Event A")
        self.assertIsInstance(fig, go.Figure)
        self.assertEqual(fig.layout.title.text, "Time spent on Event A")
        self.assertEqual(fig.layout.width, 800)
        self.assertEqual(fig.layout.height, 400)

    def test_plot_factory(self):
        plot1 = PlotFactory("Pie")
        plot2 = PlotFactory("Bar")
        plot3 = PlotFactory("Line")
        self.assertIsInstance(plot1, PiePlot)
        self.assertIsInstance(plot2, BarPlot)
        self.assertIsInstance(plot3, LinePlot)

    def test_invalid_plot_type(self):
        with self.assertRaises(ValueError):
            plot = PlotFactory("invalid_type")
