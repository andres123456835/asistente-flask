from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import os
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def autenticar_gmail(usuario="nina"):
    creds = None
    token_file = f'token_gmail_{usuario}.json'

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        # Si no existe el token, se espera que haya una variable de entorno GOOGLE_CREDS_GMAIL_NINA o ANDY
        creds_env_var = f"GOOGLE_CREDS_GMAIL_{usuario.upper()}"
        creds_data = json.loads(os.environ[creds_env_var])
        flow = InstalledAppFlow.from_client_config(creds_data, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def leer_ultimos_correos(n=5, usuario="nina"):
    service = autenticar_gmail(usuario)
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
