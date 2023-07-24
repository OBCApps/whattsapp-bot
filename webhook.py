
from fastapi import FastAPI, Request
from twilio.rest import Client
from dotenv import load_dotenv
import os
import openai

load_dotenv()
twilio_acount_id = os.getenv("twilio_acount_id")
twilio_token = os.getenv("twilio_token")
twilio_number = os.getenv("twilio_number")
openai.api_key = os.getenv("openia_key")
client = Client(twilio_acount_id, twilio_token)


def obtener_respuesta(pregunta):
    # Parámetros para la solicitud de la API
    completar = openai.Completion.create(
        engine="text-davinci-003",  # Motor GPT-3 utilizado (puedes usar otros si estás suscrito)
        prompt=pregunta,  # Pregunta o inicio del diálogo
        max_tokens=150,  # Máximo número de tokens en la respuesta
        temperature=0.7,  # Controla la creatividad de las respuestas (0.0 es más determinista, 1.0 más creativo)
    )

    # Obtener la respuesta generada por GPT-3
    respuesta = completar.choices[0].text
    return respuesta


def sendMessagge( message , number):    
    print("message" , message)
    print("number" , number)
    message = client.messages.create(
            from_ = twilio_number ,
            body= message ,
            to= number
        )

app = FastAPI()

@app.post("/whattsapp-bot")
async def whattsapp_bot(request: Request):
    message_body = await request.form()    
    print(message_body)
    user_number = message_body['From']
    msg_user = message_body['Body']
    
    response = obtener_respuesta(msg_user)
    sendMessagge(response , user_number)

    return {"status": "success"}
