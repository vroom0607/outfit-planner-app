from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_next_event():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("calendar", "v3", credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=1,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    if not events:
        return None
    return events[0]['summary']