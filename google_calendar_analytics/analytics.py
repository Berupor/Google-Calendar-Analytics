from datetime import datetime

import plotly.graph_objs as go
from google.oauth2.credentials import Credentials  # type: ignore

from .collecting.collector import AsyncCalendarDataCollector
from .processing.transformer import AsyncDataTransformer
from .visualization.visualizer_factory import (ManyEventPlot, OneEventPlot,
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
        data_collector (AsyncCalendarDataCollector): An instance of the CalendarDataCollector class.
        data_transformer (DataTransformer): An instance of the DataTransformer class.
    """

    def __init__(self, creds: Credentials):
        self.creds = creds

        self.data_collector = AsyncCalendarDataCollector(creds)
        self.data_transformer = AsyncDataTransformer()

    async def analyze_one(
        self,
        start_time: datetime,
        end_time: datetime,
        event_name: str,
        plot_type: str = "Line",
        transparency: float = 1.0,
        dark_theme: bool = False,
    ) -> go.Figure:
        """
        Analyze the duration of one event and generate a chart.

        Args:
            plot_type (str): The type of chart to be generated.
            event_name (str): The name of the event to be analyzed.
            end_time (datetime): The end time of the time range to analyze.
            start_time (datetime): The start time of the time range to analyze.
            dark_theme (bool): If True, the chart will be generated with a dark theme.
            transparency (float): The transparency of the chart.
        """

        # Create plot object
        plot_creator: OneEventPlot = await PlotFactory(
            plot_type, transparency=transparency, dark_theme=dark_theme
        )

        # Collect data for a specific event and calculate its duration
        calendar_events = await self.data_collector.collect_data(
            start_time=start_time, end_time=end_time
        )
        event_durations = await self.data_transformer.one_event_duration(
            events=calendar_events, event_name=event_name
        )

        return await plot_creator.plot(events=event_durations, event_name=event_name)

    async def analyze_many(
        self,
        start_time: datetime,
        end_time: datetime,
        plot_type: str = "Pie",
        max_events: int = 5,
        transparency: float = 1.0,
        ascending=False,
        dark_theme=False,
    ) -> go.Figure:
        """
        Analyze the durations of multiple events and generate a chart.

        Args:
            plot_type (str): The type of chart to be generated (Pie or Bar).
            max_events (int): The maximum number of events to be analyzed.
            ascending (bool): If True, sort the events in ascending order of duration
            end_time (datetime): The end time of the time range to analyze.
            start_time (datetime): The start time of the time range to analyze.
            dark_theme (bool): If True, the chart will be generated with a dark theme.
            transparency (float): The transparency of the chart.
        """

        plot_creator: ManyEventPlot = await PlotFactory(
            plot_type=plot_type,
            dark_theme=dark_theme,
            transparency=transparency,
        )

        # Collect data for the top events and calculate their durations
        calendar_events = await self.data_collector.collect_data(
            start_time=start_time,
            end_time=end_time,
        )
        event_durations = await self.data_transformer.many_events_duration(
            events=calendar_events,
            max_events=max_events,
            ascending=ascending,
        )

        return await plot_creator.plot(events=event_durations)

    async def analyze_one_with_periods(
        self,
        start_time: datetime,
        end_time: datetime,
        event_name: str,
        period_days: int = 7,
        num_periods: int = 2,
        transparency: float = 1.0,
        dark_theme: bool = False,
    ) -> go.Figure:
        """
        Analyze the duration of one event in multiple periods and generate a chart.

        Args:
            event_name (str): The name of the event to be analyzed.
            end_time (datetime): The end time of the time range to analyze.
            start_time (datetime): The start time of the time range to analyze.
            period_days (int): The number of days in each period.
            num_periods (int): The number of periods to analyze.
            transparency (float): The transparency of the chart.
            dark_theme (bool): If True, the chart will be generated with a dark theme.
        """

        # Create the plot object
        plot_type = "MultyLine"
        plot_creator = await PlotFactory(
            plot_type, transparency=transparency, dark_theme=dark_theme
        )

        # Collect data for the event duration periods
        calendar_events = await self.data_collector.collect_data(
            start_time=start_time, end_time=end_time
        )
        event_durations = await self.data_transformer.event_duration_periods(
            events=calendar_events,
            event_name=event_name,
            period_days=period_days,
            num_periods=num_periods,
        )

        return await plot_creator.plot(events=event_durations, event_name=event_name)
