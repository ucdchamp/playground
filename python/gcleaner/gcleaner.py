#pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os.path
import base64
import datetime
from itertools import islice
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
FILTER = []
service = None

def gconn():
    """Authenticates and returns a Gmail API service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def mvtotrash(message_id):
    """Moves a specified Gmail message to the Trash.

    Args:
        message_id: The ID of the message to trash.
    """
    try:
        # The key line: calling the .trash() method
        service.users().messages().trash(userId='me', id=message_id).execute()
        print(f"Message with ID '{message_id}' moved to Trash successfully.")
    except HttpError as error:
        print(f"An error occurred while trashing message '{message_id}': {error}")

def procmsgs(messages):
    """Process inbox list of messages

    Args:
        messages: list of messages to process
    """

    for msg in messages:
        if 'petsmart' in msg['sender']:
            print(f"Processing message from {msg['sender']} with subject: {msg['subject']}")
            mvtotrash(msg['id'])

def logsender(sender):
    """Logs the senders appearing in unread messages

    Args:
        sender: a list of senders to log
    """

    basename='senders'
    date= datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file = f"{basename}_{date}.log"
    with open(file, 'w') as f:
        for s in sender:
            # Write each sender to the file
            f.write(f"{s}\n")
    
    print(f"Logged senders to {os.path.abspath(file)}")

def analyzemsgs(messages):
    """Analyze inbox list of messages

    Args:
        messages: list of messages to analyze
    """

    print(f"Analyzing messages...")
    
    amsgs=set()

    for msg in messages:
        amsgs.add(msg['sender'])

    print(f"Analyzed {len(messages)} messages, found {len(amsgs)} unique senders.")
    
    if amsgs:
        logsender(list(amsgs))
        # for sender in amsgs:
        #     print(f"{sender}")
    else:
        print("No unique senders found.")
        

def get_inbox():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail inbox messages.
    """
    creds = None
    global service
    messages=[]

    try:
        service=gconn()

        # Call the Gmail API to fetch messages
        # 'q': 'in:inbox' filters for inbox messages
        # 'userId': 'me' refers to the authenticated user
        results = service.users().messages().list(userId='me', q='is:unread', maxResults=500).execute()
        messages = results.get('messages', [])

        filtered=[]

        if not messages:
            print('No unread messages found in inbox.')
        else:
            print('working with unread messages in inbox')
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()

                # Extract subject and sender
                headers = msg['payload']['headers']
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')

                # Decode message body (can be complex due to multipart messages)
                # msg_body = ""
                # if 'parts' in msg['payload']:
                #     for part in msg['payload']['parts']:
                #         if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                #             msg_body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                #         elif part['mimeType'] == 'text/html' and 'data' in part['body']:
                #             # For HTML, you might want to use a library like BeautifulSoup to parse
                #             # For simplicity, we'll just decode it here.
                #             msg_body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                # elif 'data' in msg['payload']['body']:
                #      msg_body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')

                # print(f"{msg_body if msg_body else 'No body content'}")

                filtered.append({
                    'sender': sender,
                    'subject': subject,
                    'id': message['id']
                })

                # if 'petsmart.com' in sender:
                #     filtered.append({
                #         'sender': sender,
                #         'subject': subject,
                #         'id': message['id']
                #     })


                # print(f"- From: {sender}")
                # print(f"  Subject: {subject}")
                # Print a snippet of the body, or the full body if you wish
                # print(f"  Body Snippet: {msg_body[:200]}...") # Print first 200 chars
                # print("-" * 30)
        return filtered if filtered else None


    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    inbox=get_inbox()
    #procmsgs(inbox)
    #analyzemsgs(inbox)