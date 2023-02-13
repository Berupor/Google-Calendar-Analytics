from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import seaborn as sns


class Plot(ABC):
    FIG_SIZE = (8, 4)
    COLOR = "pastel"


class ManyEventPlot(Plot):
    @abstractmethod
    def plot(self, events: dict, title: str = None):
        """
        To analyze one event for a certain period of time.
        """


class OneEventPlot(Plot):
    @abstractmethod
    def plot(self, events: dict, event_name: str):
        """
        To analyze one event for a certain period of time.
        """


class PiePlot(ManyEventPlot):
    def plot(
        self, events: dict, title: str = "Top events with the Longest Duration"
    ) -> plt:
        """
        Plot a pie chart of the event durations.

        Args:
            events (dict): A dictionary containing the event names as keys and the event durations as values.
            title (str): The title of the chart.
        """

        plt.figure(figsize=self.FIG_SIZE)
        plt.pie(
            events.values(),
            labels=events.keys(),
            autopct="%.0f %%",
            pctdistance=0.7,
            colors=sns.color_palette(self.COLOR),
            shadow=True,
        )
        plt.title(
            title,
            weight="bold",
            fontsize=14,
        )
        return plt


class BarPlot(ManyEventPlot):
    def plot(
        self, events: dict, title: str = "Top events with the Longest Duration"
    ) -> plt:
        """
        Plot a bar chart of the event durations.

        Args:
            events (dict): A dictionary containing the event names as keys and the event durations as values.
            title (str): The title of the chart.

        """

        plt.figure(figsize=self.FIG_SIZE)
        ax = sns.barplot(
            x=list(events.keys()), y=list(events.values()), palette=self.COLOR
        )
        ax.set(
            title=title,
            ylabel="Duration (Hours)",
        )
        ax.set_title(ax.get_title(), fontweight="bold", fontsize=14)
        # Add the numerical values on top of each bar
        for i, v in enumerate(list(events.values())):
            ax.text(i, 1, str(v), color="black", fontsize=8, ha="center")

        return plt


class LinePlot(OneEventPlot):
    def plot(self, events: dict, event_name: str) -> plt:
        """
        Plot a line chart of the event durations.

        Args:
            events (dict): A dictionary containing the event names as keys and the event durations as values.
            event_name (str): The name of the event.
        """

        plt.figure(figsize=self.FIG_SIZE)
        plt.plot(
            events.keys(),
            events.values(),
            color=sns.color_palette(self.COLOR)[0],
            marker="o",
            markersize=5,
            linestyle="dashed",
        )
        plt.title(
            f"Time spent on {event_name}",
            weight="bold",
            fontsize=14,
        )
        plt.xlabel("Date")
        plt.ylabel("Duration (Hours)")

        # Add gridlines to the plot for improved readability
        plt.grid(True)

        return plt


def PlotFactory(plot_type="Pie"):
    """Factory Method"""
    plots = {"Pie": PiePlot, "Bar": BarPlot, "Line": LinePlot}

    if plot_type not in plots:
        raise ValueError(
            f"Invalid plot type: '{plot_type}'.\n"
            f"Available options are: {', '.join(plots.keys())}."
        )

    return plots[plot_type]()
