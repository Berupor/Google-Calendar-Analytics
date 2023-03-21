#!/usr/bin/env python

from io import open

from setuptools import find_packages, setup

"""
:authors: Berupor
:license: MIT
:copyright: (c) 2023 Berupor
"""

version = "0.3.1"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name="google_calendar_analytics",
    version=version,
    author="Berupor",
    author_email="evgeniy.zelenoff@gmail.com",
    description=("A Python library for analyzing Google Calendar data."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Berupor/Calendar-Analytics",
    download_url=f"https://github.com/Berupor/Calendar-Analytics/archive/refs/tags/v{version}-alpha.zip",
    license="MIT",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    setup_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
