from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def autenticar_calendar():
    creds = Credentials.from_authorized_user_info(json.loads(os.environ["GOOGLE_TOKEN_CALENDAR"]), SCOPES)
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
