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
from typing import Type

import pandas as pd
import plotly.graph_objs as go

from .visual_design import base_plot_design  # type: ignore


class Plot(ABC):
    def __init__(self, style_class: base_plot_design, **kwargs):
        self.style_class = style_class
        self.transparency = style_class.transparency

        if self.style_class.dark_theme:
            self.font_color = style_class.font_color or "white"
            self.plot_bgcolor = f"rgba(34, 34, 34, {self.transparency})"
            self.paper_bgcolor = f"rgba(34, 34, 34, {self.transparency})"
            self.grid_color = style_class.grid_color or "white"
        else:
            self.font_color = style_class.font_color or "black"
            self.plot_bgcolor = f"rgba(247, 247, 247, {self.transparency})"
            self.paper_bgcolor = f"rgba(255, 255, 255, {self.transparency})"
            self.grid_color = style_class.grid_color or "black"


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
                marker=dict(colors=self.style_class.rgb_colors),
                textinfo="label+percent",
                showlegend=self.style_class.show_legend,
            )
        )

        if self.style_class.show_title:
            fig.update_layout(
                title=title,
                title_font=dict(size=18, color=self.font_color),
            )

        fig.update_layout(
            width=self.style_class.width,
            height=self.style_class.height,
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
                marker=dict(color=self.style_class.rgb_colors, colorscale="Blues"),
            )
        )
        if self.style_class.show_xaxis_title:
            fig.update_xaxes(title_text="Event")

        if self.style_class.show_yaxis_title:
            fig.update_yaxes(title_text="Duration (Hours)")

        if self.style_class.show_title:
            fig.update_layout(
                title=title,
                title_font=dict(size=18, color=self.font_color),
            )

        fig.update_layout(
            width=self.style_class.width,
            height=self.style_class.height,
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
                line=dict(
                    color=self.style_class.rgb_line_color,
                    width=self.style_class.line_width,
                    shape=self.style_class.line_shape,
                ),
                marker=dict(size=6, color=self.style_class.rgb_line_color),
                name="Duration",
            )
        )

        if self.style_class.show_title:
            fig.update_layout(
                title=dict(
                    text=f"Time spent on {event_name}",
                    font=dict(size=16, color=self.font_color),
                )
            )

        if self.style_class.show_xaxis_title:
            fig.update_xaxes(title_text="Date")

        if self.style_class.show_yaxis_title:
            fig.update_yaxes(title_text="Duration (hours)")

        fig.update_layout(
            xaxis=dict(
                showgrid=self.style_class.show_grid,
                nticks=10,
                dtick="D5",
                gridcolor=self.grid_color,
                gridwidth=self.style_class.grid_width,
                titlefont=dict(size=14, color=self.font_color),
                tickfont=dict(size=12, color=self.font_color),
                tickcolor=self.font_color,
            ),
            yaxis=dict(
                showgrid=self.style_class.show_grid,
                gridwidth=self.style_class.grid_width,
                gridcolor=self.grid_color,
                titlefont=dict(size=14, color=self.font_color),
                tickfont=dict(size=12, color=self.font_color),
                tickcolor=self.font_color,
            ),
            margin=dict(l=50, r=50, t=80, b=50),
            width=self.style_class.width,
            height=self.style_class.height,
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
                    showlegend=self.style_class.show_legend,
                )
            )
            fig.update_layout(hovermode="x")

        if self.style_class.show_title:
            fig.update_layout(
                title=dict(
                    text=f"Time spent on {event_name}",
                    font=dict(size=16, color=self.font_color),
                )
            )

        if self.style_class.show_xaxis_title:
            fig.update_xaxes(title_text="Day")

        if self.style_class.show_yaxis_title:
            fig.update_yaxes(title_text="Duration (hours)")
        # Update the color scheme and set the title of the figure
        fig.update_layout(
            xaxis=dict(
                showgrid=self.style_class.show_grid,
                gridwidth=self.style_class.grid_width,
                dtick="D5",
                gridcolor=self.grid_color,
                titlefont=dict(size=14, color=self.font_color),
                tickfont=dict(size=12, color=self.font_color),
                tickcolor=self.font_color,
            ),
            yaxis=dict(
                showgrid=self.style_class.show_grid,
                gridwidth=self.style_class.grid_width,
                gridcolor=self.grid_color,
                titlefont=dict(size=14, color=self.font_color),
                tickfont=dict(size=12, color=self.font_color),
            ),
            margin=dict(l=50, r=50, t=80, b=50),
            width=self.style_class.width,
            height=self.style_class.height,
            plot_bgcolor=self.plot_bgcolor,
            paper_bgcolor=self.paper_bgcolor,
        )
        return fig


async def PlotFactory(
    style_class: Type[base_plot_design], plot_type="Pie", event_name="Event"
) -> Plot:
    """
    Factory method to create a plot object.

    Args:
        plot_type (str): The type of plot to create.
        event_name (str): The name of the event.
        style_class (Type[base_plot_design]): The style class to use for the plot.
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

    return plots[plot_type](style_class=style_class, event_name=event_name)
