from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

# Alcance mínimo necesario para leer eventos
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def autenticar_calendar(usuario="nina"):
    token_file = f'token_calendar_{usuario}.json'
    creds = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    else:
        # Si no existe token, lanza error o inicia flujo si estás en local
        raise FileNotFoundError(f"Token no encontrado para {usuario}: {token_file}")

    return build('calendar', 'v3', credentials=creds)

def obtener_eventos_semana(usuario="nina"):
    service = autenticar_calendar(usuario)

    hoy = datetime.utcnow()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes
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
        eventos.append((inicio, evento.get('summary', '(Sin título)')))

    return eventos
