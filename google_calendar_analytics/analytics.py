from datetime import datetime

from collecting.collector import CalendarDataCollector
from processing.transformer import DataTransformer
from google.oauth2.credentials import Credentials
from visualization.visualizer_factory import (ManyEventPlot, OneEventPlot,
                                              PlotFactory)


class AnalyzerFacade:
    """
    Facade class for analyzing calendar events and generating charts.
    The class provides two methods for analyzing events: 'analyze_one' and 'analyze_many'.
    It uses a CalendarDataCollector to retrieve events from Google Calendar API and a DataTransformer
    to transform the data into the format required by the plotting functions. The plotting is done by
    creating instances of ManyEventPlot and OneEventPlot from the PlotFactory.

    Args:
        creds (Credentials): An instance of the Credentials class.

    Attributes:
        data_collector (CalendarDataCollector): An instance of the CalendarDataCollector class.
        data_transformer (DataTransformer): An instance of the DataTransformer class.
    """

    def __init__(self, creds: Credentials):
        self.creds = creds

        self.data_collector = CalendarDataCollector(creds)
        self.data_transformer = DataTransformer()

    def analyze_one(
        self,
        start_time: datetime,
        end_time: datetime,
        event_name: str,
        plot_type: str = "Line",
        transparent: int = 1,
        dark_theme: bool = False,
    ):
        """
        Analyze the duration of one event and generate a chart.

        Args:
            plot_type (str): The type of chart to be generated.
            event_name (str): The name of the event to be analyzed.
            end_time (datetime): The end time of the time range to analyze.
            start_time (datetime): The start time of the time range to analyze.
            transparent (int): The transparency of the background. If 0, the background is transparent.
            dark_theme (bool): If True, the chart will be generated with a dark theme.
        """

        plot: OneEventPlot = PlotFactory(plot_type)

        # Collect data for a specific event and calculate its duration
        events = self.data_transformer.one_event_duration(
            events=self.data_collector.collect_data(
                start_time=start_time, end_time=end_time
            ),
            event_name=event_name,
        )
        fig = plot.plot(
            events=events,
            event_name=event_name,
            transparent=transparent,
            dark_theme=dark_theme,
        )
        return fig

    def analyze_many(
        self,
        start_time: datetime,
        end_time: datetime,
        plot_type: str = "Pie",
        max_events: int = 5,
        ascending=False,
        dark_theme=False,
    ):
        """
        Analyze the durations of multiple events and generate a chart.

        Args:
            plot_type (str): The type of chart to be generated (Pie or Bar).
            max_events (int): The maximum number of events to be analyzed.
            ascending (bool): If True, sort the events in ascending order of duration
            end_time (datetime): The end time of the time range to analyze.
            start_time (datetime): The start time of the time range to analyze.
            dark_theme (bool): If True, the chart will be generated with a dark theme.
        """

        plot: ManyEventPlot = PlotFactory(plot_type)

        # Collect data for the top events and calculate their durations
        events = self.data_transformer.many_events_duration(
            events=self.data_collector.collect_data(
                start_time=start_time, end_time=end_time
            ),
            max_events=max_events,
            ascending=ascending,
        )
        fig = plot.plot(events=events, dark_theme=dark_theme)
        return fig
