# hubspot_note_writer.py
import requests
import os
import json
from hubspot.hubspot_oauth_server import get_valid_access_token

def write_note(contact_id: str, note_content: str):
    access_token = get_valid_access_token()

    url = "https://api.hubapi.com/crm/v3/objects/notes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "properties": {
            "hs_note_body": note_content
        },
        "associations": [
            {
                "to": {
                    "id": contact_id
                },
                "types": [
                    {
                        "associationCategory": "HUBSPOT_DEFINED",
                        "associationTypeId": 202
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201:
        raise RuntimeError(f"Note 写入失败: {response.text}")

    return response.json()
