
import src.commands_bot.objectives as objectives
def get_instrucction(message):
    prompt = f"Clasifica este mensaje: {message} si se relaciona a las siguientes categorias Buscar un producto[Un usuario quiere saber si el producto que desea existe y precios etc..],Saludo[Si el usuario esta escribiendo un mensaje de saludo], Buscar un producto detalle[el usuario da detalles acerca de lo qeu quiere buscar], Pagar[El usuario sabe acerca del producto por ello quiere realizar la compra del producto], Acepto pagar[El cliente menciono que comprara el producto y esta seguro que va a comprar],Envio de datos[El usuario esta enviando sus datos personales, por ejmplo nombre y numero, Pago realizado[El cliente esta afirmando que ah echo el deposito]]  " 
   #response = obtener_respuesta(prompt)