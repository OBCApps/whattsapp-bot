import openai

# Configura tu API key
openai.api_key = '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'

# Función para obtener el uso actual de tu cuenta
def obtener_uso_cuenta():
    cuenta = openai.organization.usage()
    return cuenta

# Obtén el uso actual de tu cuenta
uso_cuenta = obtener_uso_cuenta()
print("Solicitudes realizadas: ", uso_cuenta['data'][0]['attributes']['usage']['total'])
print("Límite de solicitudes: ", uso_cuenta['data'][0]['attributes']['usage']['limit'])
