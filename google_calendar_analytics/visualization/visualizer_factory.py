"""
# **VisualizerFactory**

This module provides classes for generating visualizations of event data
using Pandas and Plotly libraries. It includes classes for bar charts,
pie charts, and line charts of event durations, as well as multiple line charts
for events over multiple periods. The Plot class defines some common properties
for all visualization classes, while the ManyEventPlot and OneEventPlot classes
define required abstract methods. The factory method PlotFactory returns an object
of the specified visualization class based on input parameters.
"""
from abc import ABC, abstractmethod

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


class Plot(ABC):
    FIG_SIZE = {"width": 800, "height": 400}
    COLORS = px.colors.qualitative.Pastel

    def __init__(self, dark_theme=False, transparency=1.0, **kwargs):
        self.dark_theme = dark_theme
        self.transparency = transparency

        if self.dark_theme:
            self.font_color = "white"
            self.plot_bgcolor = f"rgba(34, 34, 34, {self.transparency})"
            self.paper_bgcolor = f"rgba(34, 34, 34, {self.transparency})"
        else:
            self.font_color = "black"
            self.plot_bgcolor = f"rgba(247, 247, 247, {self.transparency})"
            self.paper_bgcolor = f"rgba(255, 255, 255, {self.transparency})"


class ManyEventPlot(Plot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    async def plot(
        self,
        events: pd.DataFrame,
        title: str = "Title",
    ):
        """
        Analyze one event for a certain period of time.
        """


class OneEventPlot(Plot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    async def plot(
        self,
        events: pd.DataFrame,
        event_name: str,
    ):
        """
        Analyze one event for a certain period of time.
        """


class PiePlot(ManyEventPlot):
    async def plot(
        self,
        events: pd.DataFrame,
        title: str = "Top events with the Longest Duration",
        **kwargs,
    ) -> go.Figure:
        """
        Plot a pie chart of the event durations.

        Args:
            events (pd.DataFrame): A DataFrame containing the event names as the index and the event durations as the values.
            title (str): The title of the chart.
        """
        fig = go.Figure(
            go.Pie(
                labels=events.Event,
                values=events.Duration,
                textposition="auto",
                name="Duration",
                marker=dict(colors=self.COLORS),
                textinfo="label+percent",
            )
        )
        fig.update_layout(
            title=title,
            title_font=dict(size=18, color=self.font_color),
            width=self.FIG_SIZE["width"],
            height=self.FIG_SIZE["height"],
            plot_bgcolor=self.plot_bgcolor,
            paper_bgcolor=self.paper_bgcolor,
            font=dict(color=self.font_color),
        )
        fig.update_traces(
            hovertemplate="<b>Event:</b> %{label} <br><b>Duration:</b> \
                           %{value:.2f} hours<br><b>Percentage:</b> %{percent}",
        )
        return fig


class BarPlot(ManyEventPlot):
    async def plot(
        self,
        events: pd.DataFrame,
        title: str = "Top events with the Longest Duration",
        **kwargs,
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
            title_font=dict(size=18, color=self.font_color),
            xaxis=dict(title="Event", title_font=dict(size=14, color=self.font_color)),
            yaxis=dict(
                title="Duration (Hours)",
                title_font=dict(size=14, color=self.font_color),
            ),
            width=self.FIG_SIZE["width"],
            height=self.FIG_SIZE["height"],
            plot_bgcolor=self.plot_bgcolor,
            paper_bgcolor=self.paper_bgcolor,
            font=dict(color=self.font_color),
        )
        fig.update_traces(
            hovertemplate="<b>Event:</b> %{x} <br><b>Duration:</b> %{y:.2f} hours",
        )

        return fig


class LinePlot(OneEventPlot):
    async def plot(
        self,
        events: pd.DataFrame,
        event_name: str,
        **kwargs,
    ) -> go.Figure:
        """
        Plot a line chart of the event durations.

        Args:
            events (pd.DataFrame): A DataFrame containing the event dates as the index and the event durations as the values.
            event_name (str): The name of the event.
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

        fig.update_layout(
            title=dict(
                text=f"Time spent on {event_name}",
                font=dict(size=16, color=self.font_color),
            ),
            xaxis=dict(
                title="Date",
                showgrid=True,
                nticks=10,
                dtick="D5",
                gridwidth=0.2,
                titlefont=dict(size=14, color=self.font_color),
                tickfont=dict(size=12, color=self.font_color),
                tickcolor=self.font_color,
            ),
            yaxis=dict(
                title="Duration (hours)",
                showgrid=True,
                gridwidth=0.2,
                titlefont=dict(size=14, color=self.font_color),
                tickfont=dict(size=12, color=self.font_color),
                tickcolor=self.font_color,
            ),
            margin=dict(l=50, r=50, t=80, b=50),
            width=self.FIG_SIZE["width"],
            height=self.FIG_SIZE["height"],
            plot_bgcolor=self.plot_bgcolor,
            paper_bgcolor=self.paper_bgcolor,
        )

        fig.update_traces(
            hovertemplate="<b>Date:</b> %{x} <br><b>Duration:</b> %{y:.2f} hours"
        )

        return fig


class MultyLinePlot(OneEventPlot):
    async def plot(self, events: pd.DataFrame, event_name: str, **kwargs) -> go.Figure:
        """
        Plot a line chart of the event durations.

        Args:
            events (pd.DataFrame): A DataFrame containing the event dates as the index and the event durations as the values.
            event_name (str): The name of the event.
        """
        fig = go.Figure()

        # Create a separate line for each period
        for period in events.Period.unique():
            period_events = events[events.Period == period]
            period_start = period_events.Date.min().strftime("%m-%d")
            period_end = period_events.Date.max().strftime("%m-%d")
            period_label = f"{period_start} to {period_end}"
            fig.add_trace(
                go.Scatter(
                    x=period_events.Day,
                    y=period_events.Duration,
                    mode="lines+markers",
                    line=dict(width=2),
                    marker=dict(size=6),
                    name=period_label,
                    text=period_events.Date,
                    hovertemplate="<b>Date:</b> %{text} <br><b>Duration:</b> %{y:.2f} hours",
                )
            )
            fig.update_layout(hovermode="x")

        # Update the color scheme and set the title of the figure
        fig.update_layout(
            title=dict(
                text=f"Time spent on the {event_name} in periods of {events.Day.max()} days",
                font=dict(size=16, color=self.font_color),
            ),
            xaxis=dict(
                title="Day",
                showgrid=True,
                gridwidth=0.2,
                dtick="D5",
                titlefont=dict(size=14, color=self.font_color),
                tickfont=dict(size=12, color=self.font_color),
                tickcolor=self.font_color,
            ),
            yaxis=dict(
                title="Duration (hours)",
                showgrid=True,
                gridwidth=0.2,
                titlefont=dict(size=14, color=self.font_color),
                tickfont=dict(size=12, color=self.font_color),
            ),
            margin=dict(l=50, r=50, t=80, b=50),
            width=self.FIG_SIZE["width"],
            height=self.FIG_SIZE["height"],
            plot_bgcolor=self.plot_bgcolor,
            paper_bgcolor=self.paper_bgcolor,
        )
        return fig


async def PlotFactory(
    plot_type="Pie", dark_theme=False, transparency=1, event_name="Event"
) -> Plot:
    """
    Factory method to create a plot object.

    Args:
        plot_type (str): The type of plot to create.
        dark_theme (bool): Whether to use a dark theme or not.
        transparency (float): The transparency of the chart.
        event_name (str): The name of the event.
    """

    plots = {
        "Pie": PiePlot,
        "Bar": BarPlot,
        "Line": LinePlot,
        "MultyLine": MultyLinePlot,
    }

    if plot_type not in plots:
        raise ValueError(
            f"Invalid plot type: '{plot_type}'.\n"
            f"Available options are: {', '.join(plots.keys())}."
        )

    return plots[plot_type](
        dark_theme=dark_theme, transparency=transparency, event_name=event_name
    )
