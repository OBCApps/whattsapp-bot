import openai

# Reemplaza 'TU_CLAVE_DE_API' con tu clave de API de OpenAI
openai.api_key = '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'

def obtener_respuesta(pregunta):
    respuesta = openai.Completion.create(
        engine="davinci",
        prompt=pregunta,
        max_tokens=50
    )
    return respuesta.choices[0].text.strip()

def main():
    print("¡Hola! Soy un chatbot de servicio al cliente. ¿En qué puedo ayudarte hoy?")
    
    while True:
        entrada_usuario = input("Usuario: ")
        
        if entrada_usuario.lower() == 'salir':
            print("¡Hasta luego! Que tengas un buen día.")
            break
        
        respuesta_chatbot = obtener_respuesta(entrada_usuario)
        print("Chatbot:", respuesta_chatbot)
        
        if "precio" in respuesta_chatbot and "producto" in respuesta_chatbot:
            print("Chatbot: Si deseas comprar este producto, puedes continuar con el proceso de pago.")
            respuesta_pago = input("Usuario: Deseo realizar el pago. ¿Continuar? (sí/no) ")
            
            if respuesta_pago.lower() == 'sí':
                print("Chatbot: Perfecto. Procesando el pago...")
                # Aquí podrías agregar la lógica para simular el proceso de pago
                
                print("Chatbot: ¡El pago se ha realizado exitosamente! ¡Gracias por tu compra!")
            else:
                print("Chatbot: Entiendo. Si tienes más preguntas, no dudes en preguntar.")

if __name__ == "__main__":
    main()
