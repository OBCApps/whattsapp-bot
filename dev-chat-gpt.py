import openai
#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
openai.api_key = "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"


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


while True:
    prompt = input ("\nPregunta: ")
    if prompt == "exit": break
    
    respuesta_del_chatbot = obtener_respuesta(prompt)
    print("Chatbot: ", respuesta_del_chatbot)
