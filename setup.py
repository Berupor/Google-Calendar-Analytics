#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: Berupor
:license: MIT
:copyright: (c) 2023 Berupor
"""

version = "0.1.1"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="google_calendar_analytics",
    version=version,

    author='Berupor',
    author_email='evgeniy.zelenoff@gmail.com',

    description=(
        u"A Python library for analyzing Google Calendar data."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/Berupor/Calendar-Analytics",
    download_url=f"https://github.com/Berupor/Calendar-Analytics/archive/v{version}.zip",

    license="MIT",

    packages=["google_calendar_analytics"],
    install_requires=[
        "pandas==1.5.3",
        "python-dateutil==2.8.2",
        "google-api-python-client==2.77.0",
        "google-auth-httplib2==0.1.0",
        "google-auth-oauthlib==1.0.0",
        "plotly==5.13.0",
        "kaleido==0.2.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]

)
