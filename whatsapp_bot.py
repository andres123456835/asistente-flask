from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body")
    from_number = request.form.get("From")
    
    print(f"Mensaje recibido de {from_number}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # Aquí decides cómo responder
    msg.body(f"🧠 Hola, recibí tu mensaje: {incoming_msg}")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5001)
