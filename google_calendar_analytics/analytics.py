"""
# **Analytics**

The analytics module provides a facade class for analyzing calendar events and
generating charts. The module uses a CalendarDataCollector to retrieve events from
the Google Calendar API and a DataTransformer to transform the data into the format
required by the plotting functions. The plotting is done by creating instances of PlotFactory.

The AnalyzerFacade class provides three methods for analyzing events: `analyze_one`,
`analyze_many`, and `analyze_one_with_periods`. The `analyze_one` method analyzes a single
event, the analyze_many method analyzes multiple events, and the analyze_one_with_periods
method analyzes a single event over a period of time.

The AnalyzerBuilder class is a builder class that allows for creating instances of the
AnalyzerFacade class with different options.

"""

from datetime import datetime

import plotly.graph_objs as go
from google.oauth2.credentials import Credentials  # type: ignore

from .collecting.collector import AsyncCalendarDataCollector
from .processing.transformer import (AsyncDataTransformer,
                                     EventDurationPeriodsStrategy,
                                     ManyEventsDurationStrategy,
                                     OneEventDurationStrategy)
from .visualization.visualizer_factory import PlotFactory
from .core import exceptions


class AnalyzerFacade:
    """
    Facade class for analyzing calendar events and generating charts.

    The class provides three methods for analyzing events:
    `analyze_one`, 'analyze_many', and 'analyze_one_with_periods'.
    It uses a CalendarDataCollector to retrieve events from Google Calendar API and a DataTransformer
    to transform the data into the format required by the plotting functions. The plotting is done by
    creating instances of PlotFactory.

    Args:
        creds (Credentials): Google credentials class instance.

    Attributes:
        creds (Credentials): An instance of the Credentials class.
        plot_type (str): The type of chart to be generated.
        transparency (float): The transparency of the chart.
        dark_theme (bool): If True, the chart will be generated with a dark theme.
        max_events (int): The maximum number of events to be analyzed.
        ascending (bool): If True, sort the events in ascending order of duration.
        data_collector (AsyncCalendarDataCollector): An instance of the CalendarDataCollector class.
        data_transformer (DataTransformer): An instance of the DataTransformer class.

    Examples:
        ```python
        # Initialize AnalyzerFacade and analyze a single event
        analyzer = AnalyzerBuilder().with_credentials(creds).build()
        start_time = datetime(2023, 3, 1, tzinfo=pytz.UTC)
        end_time = datetime(2023, 3, 18, tzinfo=pytz.UTC)
        event_name = "Meeting"
        plot = await analyzer.analyze_one(start_time, end_time, event_name)

        # Initialize AnalyzerFacade and analyze multiple events
        analyzer = AnalyzerBuilder().with_credentials(creds).build()
        start_time = datetime(2023, 3, 1, 0, 0, 0)
        end_time = datetime(2023, 3, 31, 23, 59, 59)
        fig = await analyzer.analyze_many(start_time=start_time, end_time=end_time)
        fig.show()

        # Initialize AnalyzerFacade and analyze a single event over a period of time
        analyzer = AnalyzerBuilder().with_credentials(creds).build()
        start_time = datetime(2023, 3, 1, tzinfo=pytz.UTC)
        end_time = datetime(2023, 3, 31, tzinfo=pytz.UTC)
        event_name = "Meeting"
        period_days = 7
        num_periods = 2
        plot = await analyzer.analyze_one_with_periods(
        start_time=start_time,
        end_time=end_time,
        event_name=event_name,
        period_days=period_days,
        num_periods=num_periods,
        )
        ```
    """

    def __init__(self, creds: Credentials):
        self.creds = creds
        self.plot_type = "Line"
        self.transparency = 1.0
        self.dark_theme = False
        self.max_events = 5
        self.ascending = False

        self.data_collector = AsyncCalendarDataCollector(creds)
        self.data_transformer = AsyncDataTransformer()

    async def analyze_one(
            self, start_time: datetime, end_time: datetime, event_name: str, **kwargs
    ) -> go.Figure:
        """
        Analyze a single event and generate a plot.

        This method analyzes a single event from the specified start time to end time and generates a plot using the OneEventDurationStrategy. The method uses a CalendarDataCollector to retrieve events from the Google Calendar API, a DataTransformer to transform the data into the required format, and a PlotFactory to generate the plot.

        Args:
            start_time (datetime): The start time for the analysis.
            end_time (datetime): The end time for the analysis.
            event_name (str): The name of the event to analyze.
            **kwargs: Additional keyword arguments for the plot creation.

        Returns:
            go.Figure: The plot generated by the PlotFactory.

        Raises:
            None

        Examples:
            To analyze a single event from March 1, 2023 to March 18, 2023 with the name "Meeting" and generate a plot, use:

            ```
            analyzer = AnalyzerBuilder().with_credentials(creds).build()
            start_time = datetime(2023, 3, 1, tzinfo=pytz.UTC)
            end_time = datetime(2023, 3, 18, tzinfo=pytz.UTC)
            event_name = "Meeting"
            plot = await analyzer.analyze_one(start_time, end_time, event_name)
            ```
        """
        if self.plot_type not in ("Line", ):
            raise exceptions.InvalidPlotTypeError(self.plot_type, method="analyze_one")

        self.data_transformer.set_strategy(OneEventDurationStrategy())
        return await self._analyze(
            start_time=start_time,
            end_time=end_time,
            event_name=event_name,
            method="one",
        )

    async def analyze_many(
            self, start_time: datetime, end_time: datetime, **kwargs
    ) -> go.Figure:
        """
        Analyze multiple calendar events and generate a plot of their durations.

        Args:
            start_time (datetime): The start time for the analysis.
            end_time (datetime): The end time for the analysis.
            **kwargs: Additional keyword arguments for the plot creation.

        Returns:
            go.Figure: The plot generated by the PlotFactory.

        Raises:
            None

        Examples:
            ```
            analyzer = AnalyzerBuilder().with_credentials(creds).build()
            start_time = datetime(2023, 3, 1, 0, 0, 0)
            end_time = datetime(2023, 3, 31, 23, 59, 59)
            fig = await analyzer.analyze_many(start_time=start_time, end_time=end_time)
            fig.show()
            ```
        """
        if self.plot_type not in ("Bar", "Pie"):
            raise exceptions.InvalidPlotTypeError(self.plot_type, method="analyze_many")

        self.data_transformer.set_strategy(ManyEventsDurationStrategy())
        return await self._analyze(
            start_time=start_time,
            end_time=end_time,
            method="many",
        )

    async def analyze_one_with_periods(
            self,
            start_time: datetime,
            end_time: datetime,
            event_name: str,
            period_days: int = 7,
            num_periods: int = 2,
            **kwargs
    ) -> go.Figure:
        """
        Analyze a single event over multiple periods of time and generate a plot.

        This method analyzes a single event from the specified start time to end time over multiple periods of time using the EventDurationPeriodsStrategy. The method uses a CalendarDataCollector to retrieve events from the Google Calendar API, a DataTransformer to transform the data into the required format, and a PlotFactory to generate the plot.

        Args:
            start_time (datetime): The start time for the analysis.
            end_time (datetime): The end time for the analysis.
            event_name (str): The name of the event to analyze.
            period_days (int, optional): The number of days in each period. Defaults to 7.
            num_periods (int, optional): The number of periods to analyze. Defaults to 2.
            **kwargs: Additional keyword arguments for the plot creation.

        Returns:
            go.Figure: The plot generated by the PlotFactory.

        Raises:
            None

        Examples:
            To analyze a single event named "Meeting" from March 1, 2023 to March 31, 2023 over two periods of 7 days and generate a plot, use:

            ```
            analyzer = AnalyzerBuilder().with_credentials(creds).build()
            start_time = datetime(2023, 3, 1, tzinfo=pytz.UTC)
            end_time = datetime(2023, 3, 31, tzinfo=pytz.UTC)
            event_name = "Meeting"
            period_days = 7
            num_periods = 2
            plot = await analyzer.analyze_one_with_periods(start_time, end_time, event_name, period_days, num_periods)
            ```
        """
        if self.plot_type not in ("MultyLine", ):
            raise exceptions.InvalidPlotTypeError(self.plot_type, method="analyze_one_with_periods")

        self.data_transformer.set_strategy(EventDurationPeriodsStrategy())
        return await self._analyze(
            start_time=start_time,
            end_time=end_time,
            event_name=event_name,
            method="one_with_periods",
            period_days=period_days,
            num_periods=num_periods,
        )

    async def _analyze(
            self,
            start_time: datetime,
            end_time: datetime,
            event_name: str = None,
            method: str = "one",
            period_days: int = 7,
            num_periods: int = 2,
            **kwargs
    ) -> go.Figure:
        """
        Analyzes calendar events data and creates a plot using the specified method.

        Args:
            start_time (datetime): The start time for the analysis.
            end_time (datetime): The end time for the analysis.
            event_name (str, optional): The name of the event to analyze. Required for the 'one' and 'one_with_periods' methods. Defaults to None.
            method (str, optional): The method to use for analysis. Must be one of 'one', 'many', or 'one_with_periods'. Defaults to 'one'.
            period_days (int, optional): The number of days in each period. Required for the 'one_with_periods' method. Defaults to 7.
            num_periods (int, optional): The number of periods to analyze. Required for the 'one_with_periods' method. Defaults to 2.
            **kwargs: Additional keyword arguments for the plot creation.

        Returns:
            go.Figure: The plot generated by the PlotFactory.

        Raises:
            ValueError: If an invalid method is specified.
        """
        plot_creator = await PlotFactory(
            plot_type=self.plot_type,
            dark_theme=self.dark_theme,
            transparency=self.transparency,
        )

        calendar_events = await self.data_collector.collect_data(
            start_time=start_time,
            end_time=end_time,
        )

        if method == "one":
            event_durations = await self.data_transformer.calculate_duration(
                events=calendar_events, event_name=event_name
            )
            return await plot_creator.plot(
                events=event_durations, event_name=event_name
            )
        elif method == "many":
            event_durations = await self.data_transformer.calculate_duration(
                events=calendar_events,
                max_events=self.max_events,
                ascending=self.ascending,
            )
            return await plot_creator.plot(events=event_durations)
        elif method == "one_with_periods":
            event_durations = await self.data_transformer.calculate_duration(
                events=calendar_events,
                event_name=event_name,
                period_days=period_days,
                num_periods=num_periods,
            )

            return await plot_creator.plot(
                events=event_durations, event_name=event_name
            )
        else:
            raise ValueError("Invalid method specified")


class AnalyzerBuilder:
    """
    Builder class to create instances of the AnalyzerFacade.

    This class allows you to set different options for the AnalyzerFacade
    and then build the final instance using the `build` method.

    Examples:
        ```
        analyzer = (
            AnalyzerBuilder()
            .with_credentials(creds)
            .with_plot_type("Line")
            .with_dark_theme(True)
            .build()
        )
        ```
    """

    def __init__(self):
        self._creds = None
        self._plot_type = "Line"
        self._transparency = 1.0
        self._dark_theme = False
        self._max_events = 5
        self._ascending = False

    def with_credentials(self, creds: Credentials):
        self._creds = creds
        return self

    def with_plot_type(self, plot_type: str):
        self._plot_type = plot_type
        return self

    def with_transparency(self, transparency: float):
        self._transparency = transparency
        return self

    def with_dark_theme(self, dark_theme: bool):
        self._dark_theme = dark_theme
        return self

    def with_max_events(self, max_events: int):
        self._max_events = max_events
        return self

    def with_ascending(self, ascending: bool):
        self._ascending = ascending
        return self

    def build(self) -> AnalyzerFacade:
        analyzer = AnalyzerFacade(self._creds)
        analyzer.plot_type = self._plot_type
        analyzer.transparency = self._transparency
        analyzer.dark_theme = self._dark_theme
        analyzer.max_events = self._max_events
        analyzer.ascending = self._ascending
        return analyzer
