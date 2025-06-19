import os
import django
import pandas as pd
import requests
import json
import math

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inplacecore.settings')
django.setup()

from chatbot.models import Candidate

# Replace with your actual values
META_ACCESS_TOKEN = "EAA5J7BOmHM4BOZBv8oRDHzp5CVmCnhMV6zACVX2tV5kWzmvHaZBle808vBtelZCdU8UnyN9AuZBR4zPKS6glhFXOWmCQYUlCbopD5ZBggmZBKFkdA0qEM2eSrxmwt9BS0Wp1jJ3jnswAAdIuIgt8LZCzgPpd5P9RIbwgyLsQP9eNjnshhNEc6VcxDcxdVzgAnToy5ozALpfXFACFdUReCv3x1NVlKYvy4PTnZCBAmUsg"
META_PHONE_NUMBER_ID = "689775147550787"
PDF_LINK = "https://drive.google.com/uc?export=download&id=1F3KCuErpHRU_IeQ26JgtawL2PJvMDyAo"
PDF_FILENAME = "Informativa_InPlace.pdf"

headers = {
    "Authorization": f"Bearer {META_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

df = pd.read_excel("clean_sample_contacts.xlsx")

def send_whatsapp_template(phone_number, name):
    url = f"https://graph.facebook.com/v15.0/{META_PHONE_NUMBER_ID}/messages"

    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "welcome_onboarding",  # Your approved template name
            "language": {
                "code": "it"  # Adjust if needed
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "document",
                            "document": {
                                "link": PDF_LINK,
                                "filename": PDF_FILENAME
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": name
                        }
                    ]
                }
            ]
        }
    }

    print("Sending payload:", json.dumps(data, indent=2))

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

for _, row in df.iterrows():
    name = row.get('Name')
    surname = row.get('Surname')
    phone_number = str(row.get('Phone')).replace("+", "").replace(" ", "")

    # Validate name
    if name is None or (isinstance(name, float) and math.isnan(name)) or not str(name).strip():
        print(f"⚠️ Skipping {phone_number} because name is missing or empty")
        continue

    name = str(name).strip()

    candidate, created = Candidate.objects.get_or_create(
        phone_number=phone_number,
        defaults={'name': name, 'surname': surname, 'status': 'sent'}
    )

    if not created:
        print(f"⏭️ Already exists, skipping: {name} ({phone_number})")
        continue

    print(f"Preparing message for: {name} ({phone_number})")

    try:
        response = send_whatsapp_template(phone_number, name)
        print(f"✅ Template message sent to {name} ({phone_number}) — Response: {response}")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to send to {name} ({phone_number})")
        print(f"Status code: {e.response.status_code}")
        print(f"Response body: {e.response.text}")
