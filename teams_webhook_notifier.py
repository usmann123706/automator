import requests

from config import TEAMS_WEBHOOK_URL


def send_notification(
    incident_number,
    assigned_to,
    teams_user_id,
):
    adaptive_card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "TextBlock",
                "text": "New Incident Assignment",
                "weight": "Bolder",
                "size": "Large",
            },
            {
                "type": "TextBlock",
                "text": (
                    f"Incident {incident_number} "
                    f"has been assigned to <at>{assigned_to}</at>."
                ),
                "wrap": True,
            },
        ],
        "msteams": {
            "entities": [
                {
                    "type": "mention",
                    "text": f"<at>{assigned_to}</at>",
                    "mentioned": {
                        "id": teams_user_id,
                        "name": assigned_to,
                    },
                }
            ]
        },
    }

    response = requests.post(
        TEAMS_WEBHOOK_URL,
        json=adaptive_card,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    response.raise_for_status()

    print(f"Notification sent for incident {incident_number}")
    print(f"Status code: {response.status_code}")


