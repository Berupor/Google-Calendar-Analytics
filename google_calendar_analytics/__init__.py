"""
:authors: Berupor
:license: MIT

:copyright: (c) 2023 Berupor
"""

from ._version import __version__ as version
from .analytics import AnalyzerFacade
from .authentication.auth import CalendarAuth
from .collecting.collector import AsyncCalendarDataCollector
from .processing.transformer import (AsyncDataTransformer,
                                     EventDurationPeriodsStrategy,
                                     ManyEventsDurationStrategy,
                                     OneEventDurationStrategy)
from .visualization.visual_design import (VisualDesign, base_plot_design,
                                          pastel_palette)
from .visualization.visualizer_factory import (BarPlot, LinePlot,
                                               MultyLinePlot, PiePlot,
                                               PlotFactory)

__all__ = [
    "AnalyzerFacade",
    "AsyncCalendarDataCollector",
    "AsyncDataTransformer",
    "BarPlot",
    "CalendarAuth",
    "EventDurationPeriodsStrategy",
    "LinePlot",
    "ManyEventsDurationStrategy",
    "MultyLinePlot",
    "OneEventDurationStrategy",
    "PiePlot",
    "PlotFactory",
    "VisualDesign",
    "base_plot_design",
    "pastel_palette",
]

__author__ = "Berupor"
__version__ = version
__email__ = "evgeniy.zelenoff@gmail.com"
