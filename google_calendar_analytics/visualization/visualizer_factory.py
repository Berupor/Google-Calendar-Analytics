from abc import ABC, abstractmethod

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


class Plot(ABC):
    FIG_SIZE = {"width": 800, "height": 400}
    COLORS = px.colors.qualitative.Pastel


class ManyEventPlot(Plot):
    @abstractmethod
    def plot(
        self, events: pd.DataFrame, title: str = "Title", dark_theme: bool = False
    ):
        """
        To analyze one event for a certain period of time.
        """


class OneEventPlot(Plot):
    @abstractmethod
    def plot(
        self,
        events: pd.DataFrame,
        event_name: str,
        transparent: int,
        dark_theme: bool = False,
    ):
        """
        To analyze one event for a certain period of time.
        """


class PiePlot(ManyEventPlot):
    def plot(
        self,
        events: pd.DataFrame,
        dark_theme: bool = False,
        title: str = "Top events with the Longest Duration",
    ) -> go.Figure:
        """
        Plot a pie chart of the event durations.

        Args:
            events (pd.DataFrame): A DataFrame containing the event names as the index and the event durations as the values.
            title (str): The title of the chart.
        """
        if dark_theme:
            color_palette = px.colors.sequential.Blugrn
        else:
            color_palette = self.COLORS

        fig = go.Figure(
            go.Pie(
                labels=events.Event,
                values=events.Duration,
                textposition="auto",
                name="Duration",
                marker=dict(colors=color_palette),
                textinfo="label+percent",
            )
        )
        fig.update_layout(
            title=title,
            title_font=dict(size=18),
            width=self.FIG_SIZE["width"],
            height=self.FIG_SIZE["height"],
        )
        fig.update_traces(
            hovertemplate="<b>Event:</b> %{label} <br><b>Duration:</b> \
                           %{value:.2f} hours<br><b>Percentage:</b> %{percent}",
        )
        return fig


class BarPlot(ManyEventPlot):
    def plot(
        self,
        events: pd.DataFrame,
        title: str = "Top events with the Longest Duration",
        dark_theme: bool = False,
    ) -> go.Figure:
        """
        Plot a bar chart of the event durations.

        Args:
            events (pd.DataFrame): A DataFrame containing the event names as the index and the event durations as values.
            title (str): The title of the chart.
        """

        fig = go.Figure(
            go.Bar(
                x=events.Event,
                y=events.Duration,
                name="Duration",
                marker=dict(color=self.COLORS, colorscale="Blues"),
            )
        )

        fig.update_layout(
            title=title,
            title_font=dict(size=18),
            xaxis=dict(title="Event", title_font=dict(size=14)),
            yaxis=dict(title="Duration (Hours)", title_font=dict(size=14)),
            width=self.FIG_SIZE["width"],
            height=self.FIG_SIZE["height"],
        )
        fig.update_traces(
            hovertemplate="<b>Event:</b> %{x} <br><b>Duration:</b> %{y:.2f} hours",
        )

        return fig


class LinePlot(OneEventPlot):
    def plot(
        self,
        events: pd.DataFrame,
        event_name: str,
        transparent: int = 1,
        dark_theme: bool = False,
    ) -> go.Figure:
        """
        Plot a line chart of the event durations.

        Args:
            events (pd.DataFrame): A DataFrame containing the event dates as the index and the event durations as the values.
            event_name (str): The name of the event.
            transparent (int): The transparency of the background. If 0, the background is transparent.
            dark_theme (bool): Whether to use a dark theme or not.
        """
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=events.Date,
                y=events.Duration,
                mode="lines+markers",
                line=dict(color="red", width=2),
                marker=dict(size=6, color="red"),
                name="Duration",
            )
        )

        if dark_theme:
            # Update the color scheme for a dark theme
            fig.update_layout(
                title=dict(
                    text=f"Time spent on {event_name}",
                    font=dict(size=16, color="white"),
                ),
                xaxis=dict(
                    title="Date",
                    showgrid=True,
                    nticks=10,
                    dtick="D5",
                    gridwidth=0.2,
                    titlefont=dict(size=14, color="white"),
                    tickfont=dict(size=12, color="white"),
                    tickcolor="white",
                ),
                yaxis=dict(
                    title="Duration (hours)",
                    showgrid=True,
                    gridwidth=0.2,
                    titlefont=dict(size=14, color="white"),
                    tickfont=dict(size=12, color="white"),
                    tickcolor="white",
                ),
                margin=dict(l=50, r=50, t=80, b=50),
                plot_bgcolor=f"rgba(34, 34, 34, {transparent})",
                paper_bgcolor=f"rgba(34, 34, 34, {transparent})",
            )
        else:
            # Use the default color scheme
            fig.update_layout(
                title=dict(
                    text=f"Time spent on {event_name}",
                    font=dict(size=16, color="darkblue"),
                ),
                xaxis=dict(
                    title="Date",
                    showgrid=True,
                    gridwidth=0.2,
                    gridcolor="lightgray",
                    dtick="D5",
                    tickfont=dict(size=10),
                ),
                yaxis=dict(
                    title="Duration (hours)",
                    showgrid=True,
                    gridwidth=0.2,
                    gridcolor="lightgray",
                    tickfont=dict(size=10),
                ),
                margin=dict(l=50, r=50, t=80, b=50),
                template="plotly_white",
                plot_bgcolor=f"rgba(255, 255, 255, {transparent})",
                paper_bgcolor=f"rgba(255, 255, 255, {transparent})",
            )

        fig.update_traces(
            hovertemplate="<b>Date:</b> %{x} <br><b>Duration:</b> %{y:.2f} hours"
        )

        return fig


def PlotFactory(plot_type="Pie"):
    """Factory Method"""
    plots = {"Pie": PiePlot, "Bar": BarPlot, "Line": LinePlot}

    if plot_type not in plots:
        raise ValueError(
            f"Invalid plot type: '{plot_type}'.\n"
            f"Available options are: {', '.join(plots.keys())}."
        )

    return plots[plot_type]()
