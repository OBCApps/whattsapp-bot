
from fastapi import FastAPI, Request
from twilio.rest import Client
from dotenv import load_dotenv
import src.scripts_media.audio_transcription as audio
#import src.commands_bot.objectives as objectives
import os
import openai

load_dotenv()
twilio_acount_id = os.getenv("twilio_acount_id")
twilio_token = os.getenv("twilio_token")
twilio_number = os.getenv("twilio_number")
openai.api_key = os.getenv("openia_key")
print()
client = Client(twilio_acount_id, twilio_token)
users_info = {}

def obtener_respuesta(pregunta):
    completar = openai.Completion.create(
        engine = "text-davinci-002", 
        prompt = pregunta, 
        max_tokens = 150, 
        temperature = 0, 
    )
    respuesta = completar.choices[0].text
    return respuesta

def get_instruction(message):
    #prompt = f"Clasifica este mensaje: {message} si se relaciona a las siguientes categorias,  Buscar un producto [Un usuario quiere saber si el producto que desea existe y precios etc..] si se relaciona solo retorne Buscar un producto, Saludo[Si el usuario esta escribiendo un mensaje de saludo] si se relaciona solo retorne Saludo, Buscar un producto detalle[el usuario da detalles acerca de lo qeu quiere buscar] si se relaciona solo retorne Buscar un producto detalle, Pagar[El usuario sabe acerca del producto por ello quiere realizar la compra del producto] si se relaciona solo retorne Pagar, Acepto pagar[El cliente menciono que comprara el producto y esta seguro que va a comprar] si se relaciona solo retorne Acepto Pagar,Envio de datos[El usuario esta enviando sus datos personales, por ejmplo nombre y numero si se relaciona solo retorna Envio de datos, Pago realizado[El cliente esta afirmando que ah echo el deposito] si se relaciona solo retorna Pago realizado]  " 
    prompt = f"Clasifica este mensaje: {message} si se relaciona a las siguientes categorias, Categoria 1: si se relaciona a buscar un producto, solo dame como respuesta Buscar un producto ; Categoria 2: Si se relaciona a que se esta haciendo un saludo, solo dame como respuesta Saludo . Por ejemplo, user: Hola , respuesta:Saludo ; user:quiero un producto, respuesta: Buscar un producto"
    response = obtener_respuesta(prompt)    
    return response

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
    user = users_info.get(user_number, {'state': 'initial'})
    print("user" , user)

    if 'MediaContentType0' in message_body:
        type_media = message_body['MediaContentType0'].split("/")[0]
        if type_media == 'audio':
            msg_user = audio.get_transcription(type_media)
    

    if user['state'] == 'initial':
        # Bienvenida, busqueda , solicitud de datos
        objetivo = get_instruction(msg_user)
        print(f"objetivo {objetivo} 1")
        if objetivo == "Buscar un producto":
            user['state'] = 'search_product'
            prompt = "Solicita los detalles para la busqueda del producto"
            response = obtener_respuesta(prompt)
            sendMessagge(response , user_number)        

        elif objetivo == "Saludo":
            prompt = "Eres un profesional en venta de productos saludables, y debes darle la bienvenida a la plataforma de forma amigable y debes mencionarle que le enviaras un video explicando detalladamente de lo que puedes hacer"
            response = obtener_respuesta(prompt)
            sendMessagge(response , user_number)
        else:
            prompt = "No entendiste lo que el usuario dijo, por ello le mencionas que repita las frases "
            response = obtener_respuesta(prompt)
            sendMessagge(response , user_number)

    elif user['state'] == 'search_product':
        objetivo = get_instruction(msg_user)
        if objetivo == "Buscar un producto detalle":
            prompt = "Menciona 2 productos(colageno y CAmu CAmu) en forma de lista, mencionando que encontraste los siguientes productos"
            response = obtener_respuesta(prompt)
            sendMessagge(response , user_number)
        elif objetivo == "Pagar":
            user['state'] = 'pay_product'
            prompt = "Menciona que la unica forma de pago integrado es metodo Yape dale mas explicaciones y menciona si esta seguro de realizar el pago."
            response = obtener_respuesta(prompt)
            sendMessagge(response , user_number)

    elif user['state'] == 'pay_product':
        objetivo = get_instruction(msg_user)
        if objetivo == "Acepto pagar":
            prompt = "Solicita sus datos, Nombre, numero con el cual va a realizar el Yape."
            response = obtener_respuesta(prompt)
            sendMessagge(response , user_number)
        elif objetivo == "Envio de datos":
            user['state'] = 'paid_product'
            prompt = "Menciona que se ha obtenido los datos correctamente, y mencionale que debe realizar el Yapeo y debe mandar la imagen de la operacion realizada"
            response = obtener_respuesta(prompt)
            sendMessagge(response , user_number)
    
    elif user['state'] == 'paid_product':
        objetivo = get_instruction(msg_user)
        
        if objetivo == "Pago realizado":
            prompt = "Dile que espere a que su Yapeo aya sido confirmado, se le comunicara que el pago ah sido realizado exitosamentem en caso de error se le comunicaria en un plazo maximo de 24 horas, le das el numero 930544749 haya ocurrido un error."
            response = obtener_respuesta(prompt)
            sendMessagge(response , user_number)
    
    
    #response = obtener_respuesta(msg_user)
    #sendMessagge(response , user_number)

    return {"status": "success"}
