import RPi.GPIO as GPIO
from config import *
import httplib2
import os, sys

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'RaspiNotifier'

def get_credentials(createCredential):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'google-api-credentials.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        if createCredential:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        else:
            credentials = None
    return credentials

def googleAuth():
    get_credentials(True)
    print("Authorize")

def getNbrMessagesUnread():
    credentials = get_credentials(False)
    if not credentials:
        return -1

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().get(userId='me', id=config.get("Gmail", "label")).execute()

    return results['messagesUnread']

def checkGmail():
    nbr_mails = int(open(os.path.dirname(__file__)+"/nbr_gmail.txt", "r").read())
    new_nbr_mails = int(getNbrMessagesUnread())

    if new_nbr_mails == -1:
        print("Not authorized")
        sys.exit(1)

    GPIO_PIN = int(config.get("Gmail", "gpioPin"))
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_PIN, GPIO.OUT)

    if new_nbr_mails > nbr_mails:
        GPIO.output(GPIO_PIN, True)
    if new_nbr_mails < nbr_mails:
        GPIO.output(GPIO_PIN, False)

    open(os.path.dirname(__file__)+"/nbr_gmail.txt", "w").write(str(new_nbr_mails))
