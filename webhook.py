import json
from fastapi import FastAPI, Request
from twilio.rest import Client
from dotenv import load_dotenv
#import src.scripts_media.audio_transcription as audio
#import src.commands_bot.objectives as objectives
import os
import openai

load_dotenv()
twilio_acount_id = os.getenv("twilio_acount_id")
twilio_token = os.getenv("twilio_token")
twilio_number = os.getenv("twilio_number")
openai.api_key = os.getenv("openia_key")

client = Client(twilio_acount_id, twilio_token)
users_info = {}

def obtener_respuesta(pregunta):
    completar = openai.Completion.create(
        engine = "text-davinci-002", 
        prompt = pregunta, 
        max_tokens = 150, 
        temperature = 0.5, 
    )
    respuesta = completar.choices[0].text
    return respuesta

""" def get_instruction(message):
    #prompt = f"Clasifica este mensaje: {message} en una de las siguientes categorías:\n\n- Buscar un producto\n- Saludo\n- Buscar un producto detalle\n- Pagar\n- Acepto pagar\n- Envio de datos\n- Pago realizado\n\nPor favor, proporciona la categoría adecuada."
    prompt = segmentador(message)
    response = obtener_respuesta(prompt)    
    return response """

def get_instruction(message):
    plantilla="No me interesa tu opinion, solo clasifica el texto. Usuario: "

    completion = openai.ChatCompletion.create(
        
        model="gpt-3.5-turbo",
        messages=[
            
            {"role": "system","content": "Clasifica el siguiente texto en 5 categorias. Busqueda Producto (Cuando el usuario quiere buscar precios y descripciones sobre productos), Comprar Producto (Cuando el usuario esta decidido a comprar 1 o mas productos), Saludo (Cuando inicialmente esta saludando), Consejo nutricional (Cuando el usuario busca un consejo) y Otros (Cuando es ninguno de las anteriores)"""},
            
            {"role": "system", "name":"example_user", "content":plantilla+"Hola, buenos días"},
            {"role": "system", "name": "example_assistant", "content": "Saludo"},

            {"role": "system", "name":"example_user", "content":plantilla+"Quiero buscar un producto que me ayude con mi salud"},
            {"role": "system", "name": "example_assistant", "content": "Busqueda Producto"},

            {"role": "system", "name":"example_user", "content":plantilla+"Busco un producto saludable tenga proteinas"},
            {"role": "system", "name": "example_assistant", "content": "Busqueda Producto"},

            {"role": "system", "name":"example_user", "content":plantilla+"Creo que cenare una salchipapa que me recomiendas?"},
            {"role": "system", "name": "example_assistant", "content": "Consejo nutricional"},

            {"role": "system", "name":"example_user", "content":plantilla+"Cuanto cuesta el colageno o el acai?"},
            {"role": "system", "name": "example_assistant", "content":"Busqueda Producto"},

            {"role": "system", "name":"example_user", "content":plantilla+"Que tan saludable es tomar gaseosa?"},
            {"role": "system", "name": "example_assistant", "content": "Consejo nutricional"},

            {"role": "system", "name":"example_user", "content":plantilla+"Hola, puedes recomendarme un producto para mejorar mi sistema inmunologico "},
            {"role": "system", "name": "example_assistant", "content": "Busqueda Producto"},

            {"role": "system", "name":"example_user", "content":plantilla+"Quiero un producto que contenga vitamina C, que proteja mis celulas"},
            {"role": "system", "name": "example_assistant", "content": "Busqueda Producto"},

            {"role": "system", "name":"example_user", "content":plantilla+"Es sano comer mayonesa?"},
            {"role": "system", "name": "example_assistant", "content": "Consejo nutricional"},

            {"role": "system", "name":"example_user", "content":plantilla+"Quiero comprar Acai y Colageno"},
            {"role": "system", "name": "example_assistant", "content": "Comprar Producto"},

            {"role":"user","content":plantilla+str(message)}
        ],
        temperature=0,
        max_tokens=300,
    )


    result = completion.choices[0].message["content"]

    print("resultado: " , result)
        
    #print(ans)
    return result


def search_product(message):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role":"system", "content":"""Tu principal funcion es brindarle información al usuario como si tu fueras un experto en nutrición, ventas, es decir, el usuario te brindara un producto que busca para una compra y tu debes de darle una perspectiva clara, como un vendedor experto, mencionando las ventajas de comprar el producto. Los productos son los siguientes: Acaí, Colageno, quinua saludable y espirulina."""},
            
            {"role":"system", "name":"example_user", "content":"""Quiero comprar Acaí"""},
            {"role":"system", "name":"example_assistant", "content":"El acai es una fruta antioxidante rica en nutrientes y beneficios para la salud, como mejorar la digestión, fortalecer el sistema inmunológico y promover la salud cardiovascular.\nPrecio del acai: $10."},

            {"role":"system", "name":"example_user", "content":"""Quiero comprar colageno"""},
            {"role":"system", "name":"example_assistant", "content":"¿Qué contiene nuestro Acti Colágeno + Camu Camu? : El colágeno hidrolizado es un suplemento alimenticio de origen bovino. La misión principal del colágeno es formar fibras, a partir de las cuales se crearán las estructuras de nuestro organismo, tales como tendones, cartílagos, huesos y ligamentos. Su componente de Camu Camu, fruto de la selva amazónica, es muy alto en Vitamina C y potencia la absorción del colágeno para que el cuerpo aproveche al máximo los beneficios de este. Además contiene una gran cantidad de bioflavonoides y de aminoácidos esenciales. Beneficios: Aporta firmeza y elasticidad a nuestros tejidos y nuestra piel, mejorando su elasticidad y textura.Ayuda a mantener nuestro sistema oseo y muscular en buenas condiciones.¿Para quiénes está indicado?:Es altamente recomendado para personas mayores de 40 años y personas con problemas osteoarticulares.¿Cuál es la dosis recomendada?:3 cucharaditas, equivalentes a 15 ml., aportarán la dosis diaria necesaria.Precauciones:Elevadas dosis de colágeno, mayores a la indicada, podrían provocar problemas digestivos..\nPrecio del colágeno: $30."},

            {"role":"system", "name":"example_user", "content":"""Quiero comprar Quinua pop"""},
            {"role":"system", "name":"example_assistant", "content":"La quinua pop es una mezcla deliciosa y saludable que contiene pasas, arándanos y quinua. Esta combinación proporciona una buena dosis de fibra, antioxidantes y nutrientes esenciales para una alimentación equilibrada.\nPrecio de la quinua pop: $15."},
          
            {"role":"user", "content":str(message)}
        ],
        temperature=0,
        max_tokens=300,
    )

    result = completion.choices[0].message["content"]

    print(result)

    return result

def get_search_product(message):
    prompt = """
            Tu unica funcion es generar una lista diccionario de productos saludables con sus cantidades segun mencione el usuario donde la clave es el producto y el valor es la cantidad que desea(por defecto es 1). Los productos son: Acaí, colageno, Quinua pop , Espirulina y Camu Camu.
            En caso no se relacione genera un diccionario vacio.

            Usuario: Quiero comprar Acai y Colageno
            Respuesta: {"Acai":1,"Colageno":1} 
            Usuario: Tambien Quiero comprar 4 Acais 
            Respuesta: {"Acai":4} 
            Usuario: Quiero comprar Quinua Pop y quiero saber el precio
            Respuesta: {"Quinua Pop":1} 
            Usuario: Quiero llevar 2 Acais, Colageno e Espirulina
            Respuesta: {"Acai":2,"Colageno":1,"Espirulina":1} 
            Usuario: Quiero comprar Acaí, 2 colageno , 3 Quinua pop, Espirulina y Camu Camu
            Respuesta:  {"Acai":3,"Colageno":3,"Quinua pop":1, "Espirulina":1 , "Camu Camu":1}
            Usuario:%s
            Respuesta : """%message
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    result = response.choices[0].message["content"]
    print("lista productos: " , result)
    return result
    
users_info = [
    {
        "number": "whatsapp:+51930544749",
        "state": "initial",
        "name": "Wanly Obregón",
        "new" : False,
        "data": {            
            "Compras": [
                {"producto": "Producto X", "precio": 10.0 , "cantidad" : 1},
                {"producto": "Producto Y", "precio": 10.0 , "cantidad" : 1},
            ],
            
            "Carrito": [
                {"producto": "Producto Z", "precio": 10.0 , "cantidad" : 1},
                {"producto": "Producto W", "precio": 10.0 , "cantidad" : 1},
            ],
            
            "Buscados": [
                {"producto": "Producto L", "precio": 10.0 , "cantidad" : 1},
                {"producto": "Producto M", "precio": 10.0 , "cantidad" : 1},
            ]
            
        }
    }
]
def get_user_info(number):
    for user in users_info:
        if user["number"] == number:
            return user
    
    return None

""" 
def update_user_info(number, data):
    for user in users_info:
        if user["number"] == number:
            user["state"] = data["state"]  # Modifica el estado con el nuevo valor
            break """

def update_user_info(number, data):
    for user in users_info:
        if user["number"] == number:
            user["state"] = data["state"]  # Modifica el estado con el nuevo valor
            
            # Agregar el nuevo producto al carrito
            user["data"]["Carrito"].extend(data["data"]["Carrito"])

            break


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
    user_number = message_body['From']
    msg_user = message_body['Body']
    user = get_user_info(user_number)
    if user == None:
        print("Agregar nuevo")
        users_info.append({
            "number": user_number,
            "state" : "initial",
            "name": "",
            "new" : True,
            "data": {            
                "Compras": [],                
                "Carrito": [],
                "Buscados": []
                
            }
        })
        print(users_info)
        user = get_user_info(user_number)
        print(user)
    
    #user = users_info.get(user_number, {'state': 'initial'})
    print("user - state" , user)

    if 'MediaContentType0' in message_body:
        type_media = message_body['MediaContentType0'].split("/")[0]
        if type_media == 'audio':
            audio_data = await request.form()
            msg_user = "hols" #audio.to_audio_text(audio_data)
            print(f"En texto: {msg_user}")
    
    



    if user['state'] == 'initial':      
        objetivo = get_instruction(msg_user)

        if objetivo == "Saludo":
            
            if( user['new'] == True):
                prompt = "Olvida todo lo anterior, Eres un profesional en venta de productos saludables, y debes darle la bienvenida a CHATIA  de forma amigable y debes mencionarle que le enviaras un video al whattsapp explicando detalladamente de lo que puedes hacer, para que tengas idea (Eres un chatbot que brindara informacion de productos saludables) "
                response = obtener_respuesta(prompt)
                sendMessagge(response , user_number)
            else:
                prompt = "Olvida todo lo anterior, Eres un profesional en venta de productos saludables, el usuario ah vuelto a contactar contigo por que ya te compro un producto o ya te solicito informacion de un producto. Debes darle la bienvienida y preguntarle sobre que producto esta interesado. Por ejemplo: Bienvenido nuevamente con nosotros, gracias por volver, en que puedo ayudarte?"
                response = obtener_respuesta(prompt)
                sendMessagge(response , user_number)
            
            

               
        elif objetivo == "Busqueda Producto":
            response = search_product(msg_user)
            sendMessagge(response , user_number)
            

        elif objetivo == "Comprar Producto":
            to_search = get_search_product(msg_user) 
            to_search = json.loads(to_search)
            if( to_search == {}):
                response = "Brindame los datos de los productos que deseas Comprar"
                sendMessagge(response , user_number) 
            else :
                
                data = {
                    "number": user_number,
                    "state" : "pay_product",
                    "data": {            
                        "Carrito": [{"producto": producto, "precio": 10, "cantidad": cantidad} for producto, cantidad in to_search.items()],
                        
                    }
                }
                update_user_info(user_number, data)
                print("Actualizado: ", user)
                response = "Se agregaran estos productos a tu carrito de compras, deseas continuar con el pago de los productos?"
                sendMessagge(response , user_number)


        else:
            #print("3")
            prompt = "No entendiste lo que el usuario dijo, por ello le mencionas que repita las frases "
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
