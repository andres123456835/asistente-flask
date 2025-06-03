from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

# Alcance mínimo necesario para leer eventos
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def autenticar_calendar():
    creds = None

    # Intenta usar el token ya guardado
    if os.path.exists('token_calendar.json'):
        creds = Credentials.from_authorized_user_file('token_calendar.json', SCOPES)
    else:
        # Si no existe, abre flujo de autorización
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Guarda token para futuros usos
        with open('token_calendar.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def obtener_eventos_semana():
    service = autenticar_calendar()

    hoy = datetime.utcnow()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de esta semana
    fin_semana = inicio_semana + timedelta(days=7)       # Domingo

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
