import operator

import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:
    SAVING_ROUTE = "visualization/charts"
    DPI = 250

    def plot_pie_chart(self, data: dict, max_events: int = 5):
        """
        Plot a pie chart of the event durations.

        Args:
            data (dict): A dictionary containing the event names as keys and the event durations as values.
            max_events (int, optional): The maximum number of events to display in the pie chart. Defaults to 5.
        """
        sorted_events = dict(
            sorted(data.items(), key=operator.itemgetter(1), reverse=True)
        )
        top_events = dict(list(sorted_events.items())[:max_events])

        plt.pie(
            top_events.values(),
            labels=top_events.keys(),
            autopct="%.0f %%",
            pctdistance=0.7,
            colors=sns.color_palette("pastel"),
            shadow=True,
        )
        plt.title(
            f"Top {max_events} events with Longest Duratioin",
            weight="bold",
            fontsize=14,
        )
        plt.savefig(self.SAVING_ROUTE + "/pie_plot.png", dpi=self.DPI)

    def plot_bar_chart(self, data: dict, max_events=5):
        """
        Plot a bar chart of the event durations.

        Args:
            data (dict): A dictionary containing the event names as keys and the event durations as values.
            max_events (int, optional): The maximum number of events to display in the bar chart. Defaults to 5.
        """
        sorted_events = dict(
            sorted(data.items(), key=operator.itemgetter(1), reverse=True)
        )
        top_events = dict(list(sorted_events.items())[:max_events])

        plt.figure(figsize=(8, 4))
        ax = sns.barplot(
            x=list(top_events.keys()), y=list(top_events.values()), palette="pastel"
        )
        ax.set(
            title=f"Top {max_events} Events with the Longest Duration",
            ylabel="Duration (Hours)",
        )
        ax.set_title(ax.get_title(), fontweight="bold", fontsize=14)

        plt.savefig(self.SAVING_ROUTE + "/bar_plot.png", dpi=self.DPI)
