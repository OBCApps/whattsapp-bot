

from twilio.rest import Client

account_sid = 'AC5a103564486ae5c551c906b87bdead06'
auth_token = '1850f752340ef0fae1f1f4b604866a98'
client = Client(account_sid, auth_token)


message = client.messages.create(
    from_='whatsapp:+14155238886',
    body= "Prueba otra vez",
    to='whatsapp:+51'+ "930544749"  
  )
