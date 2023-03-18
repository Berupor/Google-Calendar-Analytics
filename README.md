[![PyPi Package Version](https://img.shields.io/pypi/v/google-calendar-analytics.svg)](https://pypi.org/project/google-calendar-analytics/)
[![PyPi status](https://img.shields.io/pypi/status/google-calendar-analytics.svg?style=flat-square)](https://pypi.python.org/pypi/google-calendar-analytics)
[![PyPi downloads](https://img.shields.io/pypi/dm/google-calendar-analytics.svg)](https://pypi.org/project/google-calendar-analytics/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/google-calendar-analytics.svg)](https://pypi.python.org/pypi/google-calendar-analytics)

# Google Calendar Analytics

![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/Logo.png?raw=true)

---

- ### [Documentation](https://berupor.github.io/Calendar-Analytics/)
- ### [Source code](https://github.com/Berupor/Calendar-Analytics)

---
This Python program allows you to perform analytics on your Google Calendar events. With this program, you can visualize
the total duration of your events, compare the length of events across different time periods, and gain insights into
which events take up the most time.

## Features

- Async support for faster data retrieval and chart generation
- Extract events from your Google Calendar
- Compute the total duration of events in a specified time range
- Visualize the duration of events in a pie chart, bar chart, line chart and more
- Limit the number of events displayed in the charts
- Wide chart customization. For example, dark mode and transparent background

## Quick Start
To use the Google Calendar Analytics program, first install the dependencies by running the following command:

```bash
pip install google-calendar-analytics
```

You can then import the AnalyzerFacade and Analyzer builder classs and create an instances with your Google Calendar
credentials:


### How to get credentials from Google?
1. [Google documentation](https://developers.google.com/calendar/api/quickstart/python)

```python
import asyncio
from datetime import datetime

from google.oauth2.credentials import Credentials
from google_calendar_analytics import AnalyzerFacade, AnalyzerBuilder

# (You can get it from Google OAuth2 in you web app or from link above)
# Example of creds dictionary. (You can get it from Google OAuth2 in your web app)
creds = {
    "token": "ya29.a0AVvZVsoH4qZcrGK25VwsXspJv-r9K-",
    "refresh_token": "1//0hwlhrtalKgeRCgYIARAAGBESNwF-",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "395np.apps.googleusercontent.com",
    "client_secret": "GOCSPXFqoucE03VRVz",
    "scopes": ["https://www.googleapis.com/auth/calendar"],
    "expiry": "2023-02-18T15:30:15.674219Z"
}
creds = Credentials.from_authorized_user_info(creds)
```

Once you have created the credentials, you can create an instance of the AnalyzerFacade with AnalyzerBuilder class and
use it to analyze your calendar:

```python
analyzer = (
    AnalyzerBuilder()
    .with_credentials(creds)
    .with_plot_type("Bar")
    .build()
)

# Choose time range for analysis
start_time = datetime(2023, 3, 1)
end_time = datetime(2023, 3, 18)

plot = await analyzer.analyze_one(start_time, end_time, event_name="Programming")
plot.show()
```


## Contribution

If you would like to contribute to this project, please feel free to submit a pull request. Some areas where
contributions are particularly welcome include:

- Adding new features
- Improving existing features
- Debugging and fixing bugs
- Adding tests to ensure the program is working as expected

## Analytics example:

|              Pie plot               |              Bar plot               |
|:-----------------------------------:|:-----------------------------------:|
| ![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Pie_ploty.png?raw=true) | ![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Bar_ploty.png?raw=true) |

|              Line plot               |                                          Multy line plot                                           |          
|:------------------------------------:|:--------------------------------------------------------------------------------------------------:|
| ![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Line_ploty.png?raw=true) | ![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Multy.png?raw=true) |
 
