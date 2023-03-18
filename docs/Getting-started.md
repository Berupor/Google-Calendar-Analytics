To use the Google Calendar Analytics program, first install the dependencies by running the following command:

```bash
pip install google-calendar-analytics
```

You can then import the AnalyzerFacade and Analyzer builder classs and create an instances with your Google Calendar
credentials:


## How to get credentials from Google?
1. [Google documentation](https://developers.google.com/calendar/api/quickstart/python)
2. [Our documentation](Credentials.md)


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

