from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import os
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def autenticar_gmail():
    creds = None
    token_path = os.path.abspath("token_gmail.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    else:
        creds_data = json.loads(os.environ["GOOGLE_CREDS_GMAIL"])
        flow = InstalledAppFlow.from_client_config(creds_data, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def leer_ultimos_correos(n=5):
    service = autenticar_gmail()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=n).execute()
    mensajes = results.get('messages', [])

    correos = []
    for msg in mensajes:
        data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = data['payload']['headers']
        asunto = next((h['value'] for h in headers if h['name'] == 'Subject'), '(sin asunto)')
        remitente = next((h['value'] for h in headers if h['name'] == 'From'), '(desconocido)')
        correos.append((remitente, asunto))
    
    return correos
