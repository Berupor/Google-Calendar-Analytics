Getting Google API Credentials

To use the Google Calendar API, you will need to obtain API credentials from the Google Cloud Console. Follow these steps to get the credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Navigate to the "APIs & Services" tab and click on "Credentials".
4. Click on the "Create credentials" button and select "OAuth client ID".
5. Select "Desktop app" as the application type.
6. Enter a name for the client ID and click "Create".
7. Download the client ID and client secret to your computer.
8. Store the client ID and secret securely in your application's configuration file or environment variables.
9. When you run your application, it will prompt you to authenticate with your Google account and grant access to the Google Calendar API.
10. Note that depending on the Google Cloud Console dashboard, some of these steps may differ slightly, but the general process is the same. Once you have obtained the credentials, you will be able to use them to authenticate your application and access the Google Calendar API.

## After you have obtained the credentials.json
You can use it to authenticate your application and access the Google Calendar Analytics.

Move `credentials.json` file to your project folder and write:
```python
from google_calendar_analytics.authentication.auth import CalendarAuth

creds = CalendarAuth(token_path="your_folder/token.json",
                     credentials_path="your_folder/credentials.json").get_credentials()
```

Congratulations! You have successfully obtained the credentials and can now use them to authenticate your application and access the Google Calendar Analytics.
