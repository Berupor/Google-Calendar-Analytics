"""
:authors: Berupor
:license: MIT

:copyright: (c) 2023 Berupor
"""

from ._version import __version__
from .analytics import AnalyzerFacade
from .authentication.auth import CalendarAuth
from .collecting.collector import AsyncCalendarDataCollector
from .processing.transformer import AsyncDataTransformer
from .visualization.visualizer_factory import (BarPlot, LinePlot, PiePlot,
                                               PlotFactory, MultyLinePlot)

__all__ = [
    "AsyncDataTransformer",
    "PlotFactory",
    "PiePlot",
    "BarPlot",
    "CalendarAuth",
    "LinePlot",
    "MultyLinePlot",
    "AsyncCalendarDataCollector",
    "AnalyzerFacade",
]

__author__ = "Berupor"
__version__ = __version__
__email__ = "evgeniy.zelenoff@gmail.com"
