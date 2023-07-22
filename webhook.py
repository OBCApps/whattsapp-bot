
from fastapi import FastAPI, Request
from twilio.rest import Client
from dotenv import load_dotenv
import os


load_dotenv()
twilio_acount_id = os.getenv("twilio_acount_id")
twilio_token = os.getenv("twilio_token")
twilio_number = os.getenv("twilio_number")

app = FastAPI()

@app.post("/whattsapp-bot")
async def whattsapp_bot(request: Request):
    message_body = await request.form()    
    user_number = message_body['From']
    msg_user = message_body['Body']
    client = Client(twilio_acount_id, twilio_token)

    if "hola" in msg_user:
        message = client.messages.create(
            from_ = twilio_number ,
            body="Hola! ¿Cómo estás?",
            to= user_number
        )
    else:
        message = client.messages.create(
            from_ = twilio_number ,
            body = "No entendí tu mensaje. Por favor, envía 'hola' para recibir una respuesta.",
            to = user_number
        )

    return {"status": "success"}
