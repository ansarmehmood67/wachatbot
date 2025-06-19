import os
import django
import pandas as pd
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inplacecore.settings')
django.setup()

from chatbot.models import Candidate

META_ACCESS_TOKEN = "EAA5J7BOmHM4BOZBv8oRDHzp5CVmCnhMV6zACVX2tV5kWzmvHaZBle808vBtelZCdU8UnyN9AuZBR4zPKS6glhFXOWmCQYUlCbopD5ZBggmZBKFkdA0qEM2eSrxmwt9BS0Wp1jJ3jnswAAdIuIgt8LZCzgPpd5P9RIbwgyLsQP9eNjnshhNEc6VcxDcxdVzgAnToy5ozALpfXFACFdUReCv3x1NVlKYvy4PTnZCBAmUsg"
META_PHONE_NUMBER_ID = "689775147550787"

HEADERS = {
    "Authorization": f"Bearer {META_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def send_onboarding_template(phone_number):
    url = f"https://graph.facebook.com/v15.0/{META_PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "onboarding",
            "language": {
                "code": "it"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "document",
                            "document": {
                                "link": "https://instant-avatar.com/document/Privacy%20whatsapp.pdf",
                                "filename": "Informativa_InPlace.pdf"
                            }
                        }
                    ]
                }
            ]
        }
    }

    print(f"Sending onboarding template to {phone_number}")
    print("Payload:", json.dumps(payload, indent=2))

    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()




def main():
    df = pd.read_excel("clean_sample_contacts.xlsx")

    for _, row in df.iterrows():
        phone_number = str(row.get('Phone')).replace("+", "").replace(" ", "")

        if not phone_number or phone_number.lower() == 'nan':
            print(f"⚠️ Skipping invalid phone number: {phone_number}")
            continue

        candidate, created = Candidate.objects.get_or_create(
            phone_number=phone_number,
            defaults={'status': 'sent'}
        )

        if not created:
            print(f"⏭️ Candidate exists, skipping: {phone_number}")
            continue

        try:
            response = send_onboarding_template(phone_number)
            print(f"✅ Onboarding template sent to {phone_number}: {response}")
        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed to send to {phone_number}")
            print(f"Status: {e.response.status_code}")
            print(f"Response: {e.response.text}")

if __name__ == "__main__":
    main()
