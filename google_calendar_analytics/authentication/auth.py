import os.path

from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore


class CalendarAuth:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self, token_path: str, credentials_path: str):
        self.token_path = token_path
        self.credentials_path = credentials_path

    def get_credentials(self) -> Credentials | None:
        """
        Get the user's calendar credentials.

        Returns:
            Credentials: Google calendar credentials.
        """
        creds = None

        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)

        if not creds or not creds.valid:
            # Try to refresh the credentials
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # If the credentials are not valid, try to get new credentials
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                except FileNotFoundError:
                    print(
                        f"Error: The credentials file {self.credentials_path} was not found."
                    )
                    return None

            # Save the credentials to the token file
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return creds
