import sqlite3
import datetime


def inicializar_base():
    conn = sqlite3.connect("experiencias.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS decisiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            estado TEXT,
            accion TEXT,
            recompensa INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def guardar_experiencia(estado, accion, recompensa):
    conn = sqlite3.connect("experiencias.db")
    c = conn.cursor()
    c.execute('INSERT INTO decisiones (timestamp, estado, accion, recompensa) VALUES (?, ?, ?, ?)', (
        datetime.datetime.now().isoformat(),
        str(estado),
        str(accion),
        recompensa
    ))
    conn.commit()
    conn.close()
