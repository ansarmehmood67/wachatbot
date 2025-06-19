import os
import django
from dotenv import load_dotenv
from twilio.rest import Client

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inplacecore.settings')
django.setup()

# Load env
load_dotenv()

from chatbot.models import Candidate

# Twilio setup
client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Reminder text
reminder_text = (
    "Ciao! Hai completato la registrazione su https://www.inplace.it?\n"
    "Se hai bisogno di aiuto, scrivi pure qui 🙂"
)

# Fetch candidates to remind
candidates = Candidate.objects.filter(status='sent')

for candidate in candidates:
    try:
        msg = client.messages.create(
            from_=twilio_number,
            to=f"whatsapp:{candidate.phone}",
            body=reminder_text
        )
        candidate.status = 'reminded'
        candidate.save()
        print(f"✅ Reminder sent to {candidate.name} ({candidate.phone})")
    except Exception as e:
        print(f"❌ Failed to send to {candidate.phone}: {e}")
