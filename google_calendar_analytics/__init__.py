"""
:authors: Berupor
:license: MIT

:copyright: (c) 2023 Berupor
"""

from ._version import __version__ as version
from .analytics import AnalyzerBuilder, AnalyzerFacade
from .authentication.auth import CalendarAuth
from .collecting.collector import AsyncCalendarDataCollector
from .processing.transformer import (AsyncDataTransformer,
                                     EventDurationPeriodsStrategy,
                                     ManyEventsDurationStrategy,
                                     OneEventDurationStrategy)
from .visualization.visualizer_factory import (BarPlot, LinePlot,
                                               MultyLinePlot, PiePlot,
                                               PlotFactory)

__all__ = [
    "AnalyzerBuilder",
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
]

__author__ = "Berupor"
__version__ = version
__email__ = "evgeniy.zelenoff@gmail.com"
