from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC1c2d4e4246bce38f509b8a241d618b85"
# Your Auth Token from twilio.com/console
auth_token  = "93fd3d2a14defb5427d3fd89afbea18a"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+61432160253", 
    from_="+61481072801",
    body="My name is Ron Burgandy?")

print(message.sid)