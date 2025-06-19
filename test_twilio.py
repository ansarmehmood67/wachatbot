import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Connect to Twilio
client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

# Send a WhatsApp message
message = client.messages.create(
    body="Ciao! Ti stiamo cercando da InPlace. Registrati su https://www.inplace.it",
    from_=os.getenv("TWILIO_SANDBOX_NUMBER"),
    to=os.getenv("MY_TEST_NUMBER")
)

print(f"Message SID: {message.sid}")
