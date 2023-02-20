# Google Calendar Analytics

![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/Logo.png?raw=true)
This Python program allows you to perform analytics on your Google Calendar events. With this program, you can visualize
the total duration of your events, compare the length of events across different time periods, and gain insights into
which events take up the most time.

## Features

- Extract events from your Google Calendar
- Compute the total duration of events in a specified time range
- Visualize the duration of events in a pie chart, bar chart, or line chart
- Limit the number of events displayed in the charts
- Wide chart customization. For example, dark mode and transparent background

## Usage
To use the Google Calendar Analytics program, first install the dependencies by running the following command:

```bash
pip install google-calendar-analytics
```

You can then import the AnalyzerFacade class and create an instance with your Google Calendar credentials:

```python
from datetime import datetime
from google.oauth2.credentials import Credentials

from google_calendar_analytics import AnalyzerFacade

# Example of creds dictionary. (You can get it from Google OAuth2 in you web app)
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
analyzer = AnalyzerFacade(creds=creds)
```

Once you have an AnalyzerFacade instance, you can use its analyze_one and analyze_many methods to generate charts. For example, to analyze a single event and generate a chart, you can use the following code:

```python
start_time = datetime(2023, 2, 1)
end_time = datetime(2023, 2, 15)

event_name = "Meeting"
plot_type = "Line"
fig = analyzer.analyze_one(start_time, end_time, event_name, plot_type)
fig.show()
```
To analyze multiple events and generate a chart, you can use the following code:

```python
start_time = datetime(2023, 2, 1)
end_time = datetime(2023, 2, 15)

max_events = 5
plot_type = "Pie"
fig = analyzer.analyze_many(start_time, end_time, plot_type, max_events)
fig.show()
```

## Contribution

If you would like to contribute to this project, please feel free to submit a pull request. Some areas where
contributions are particularly welcome include:

- Adding new features
- Improving existing features
- Debugging and fixing bugs
- Adding tests to ensure the program is working as expected

## Weekly analytics example:

|              Pie plot               |              Bar plot               |
|:-----------------------------------:|:-----------------------------------:|
| ![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Pie_ploty.png?raw=true) | ![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Bar_ploty.png?raw=true) |

|              Line plot               |                        
|:------------------------------------:|
| ![img](https://github.com/Berupor/Calendar-Analytics/blob/master/examples/plot_Line_ploty.png?raw=true) | 
 
