from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from datetime import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = '/Users/Melik/Desktop/client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

# title = "Google I/O 2015"
# desc = "A chance to hear more about Google\'s developer products."
# dateStart = '2017-09-18' YYYY-mon-day date i.e. '2017-09-18'
# timeStart = '06:00:00' hr:min:sec time i.e. '06:00:00'
# dateEnd = '2017-09-18'
# timeEnd = '10:00:00'
# isDefaultReminder = False
# emailHours = 48 #48 hours
# popupMinutes = 30 #30 minutes
# appendEvent("Google I/O 2015","A chance to hear more about Google\'s developer products.",'2017-09-18','06:00:00','2017-09-18','10:00:00',False,48,30)
def appendEvent(title,desc,dateStart,timeStart,dateEnd,timeEnd,isDefaultReminder,emailHours,popupMinutes):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = {
        'summary': title,
        'description': desc,
        'start': {
            'dateTime': dateStart+'T'+timeStart,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': dateEnd+'T'+timeEnd,
            'timeZone': 'America/New_York',
        },
        'reminders': {
        'useDefault': isDefaultReminder,
        'overrides': [
            {'method': 'email', 'minutes': emailHours * 60},
            {'method': 'popup', 'minutes': popupMinutes},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
