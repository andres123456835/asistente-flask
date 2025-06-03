from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
import json

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def autenticar_calendar():
    creds = None
    creds_data = json.loads(os.environ["GOOGLE_CREDS"])
    flow = InstalledAppFlow.from_client_config(creds_data, SCOPES)
    creds = flow.run_console()  # sin navegador, copia/pega código desde consola de Render
    return build('calendar', 'v3', credentials=creds)


def obtener_eventos_semana():
    service = autenticar_calendar()
    hoy = datetime.utcnow()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=7)
    eventos_resultado = service.events().list(
        calendarId='primary',
        timeMin=inicio_semana.isoformat() + 'Z',
        timeMax=fin_semana.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    eventos = []
    for evento in eventos_resultado.get('items', []):
        inicio = evento['start'].get('dateTime', evento['start'].get('date'))
        eventos.append((inicio, evento['summary']))
    return eventos