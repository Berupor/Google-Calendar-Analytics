from authentication.auth import CalendarAuth
from data_collecting.collector import CalendarDataCollector
from data_processing.transformer import DataTransformer
from visualization.image_saver import ImageSaver
from visualization.visualizer_factory import (ManyEventPlot, OneEventPlot,
                                              PlotFactory)


class AnalyzerFacade:
    def __init__(self):
        self.calendar_auth = CalendarAuth(
            "authentication/token.json", "authentication/credentials.json"
        )
        self.data_collector = CalendarDataCollector(
            self.calendar_auth.get_credentials()
        )
        self.data_transformer = DataTransformer()
        self.image_saver = ImageSaver(route="visualization/charts/", dpi=300)

    def analyze_one(self, event_name: str, plot_type: str = "Line", time_range="week"):
        """
        Analyze the duration of one event and generate a chart.

        Args:
            plot_type (str): The type of chart to be generated.
            event_name (str): The name of the event to be analyzed.
            time_range (str): The time range to analyze the events (week, month, or year).
        """

        plot: OneEventPlot = PlotFactory(plot_type)

        # Collect data for a specific event and calculate its duration
        events = self.data_transformer.one_event_duration(
            events=self.data_collector.collect_data(time_range=time_range),
            event_name=event_name,
        )
        self.image_saver.save_plot(
            plot=plot.plot(events=events, event_name=event_name),
            filename=f"plot_{plot_type}",
        )

    def analyze_many(
        self, plot_type: str = "Pie", max_events: int = 5, time_range="week", order=True
    ):
        """
        Analyze the durations of multiple events and generate a chart.

        Args:
            plot_type (str): The type of chart to be generated (Pie or Bar).
            max_events (int): The maximum number of events to be analyzed.
            time_range (str): The time range to analyze the events (week, month, or year).
            order (bool): If True, then there will be events with the longest duration, otherwise with the shortest
        """

        plot: ManyEventPlot = PlotFactory(plot_type)

        # Collect data for the top events and calculate their durations
        events = self.data_transformer.many_events_duration(
            events=self.data_collector.collect_data(time_range=time_range),
            max_events=max_events,
            order=order,
        )
        self.image_saver.save_plot(
            plot=plot.plot(events=events), filename=f"plot_{plot_type}"
        )


def main():
    """
    Entrypoint with using examples.
    """
    event_visualizer = AnalyzerFacade()

    event_visualizer.analyze_one(
        plot_type="Line", time_range="week", event_name="Programming"
    )
    event_visualizer.analyze_many(plot_type="Bar", time_range="week", max_events=5)


if __name__ == "__main__":
    main()
