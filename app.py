from flask import Flask, render_template, request, redirect, url_for
from calendar_reader import obtener_eventos_semana

app = Flask(__name__)

@app.route("/")
def index():
    eventos = obtener_eventos_semana()
    return render_template("index.html", eventos=eventos)

if __name__ == "__main__":
    app.run()