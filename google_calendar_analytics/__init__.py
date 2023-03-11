"""
:authors: Berupor
:license: MIT

:copyright: (c) 2023 Berupor
"""

from ._version import __version__
from .analytics import AnalyzerFacade
from .authentication.auth import CalendarAuth
from .collecting.collector import CalendarDataCollector
from .processing.transformer import DataTransformer
from .visualization.visualizer_factory import (BarPlot, LinePlot, PiePlot,
                                               PlotFactory)

__all__ = [
    "DataTransformer",
    "PlotFactory",
    "PiePlot",
    "BarPlot",
    "CalendarAuth",
    "LinePlot",
    "CalendarDataCollector",
    "AnalyzerFacade",
]

__author__ = "Berupor"
__version__ = __version__
__email__ = "evgeniy.zelenoff@gmail.com"
