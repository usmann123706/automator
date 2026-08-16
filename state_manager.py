import json
from pathlib import Path
from datetime import datetime, timedelta


STATE_FILE = Path("processed_incidents.json")
RETENTION_DAYS = 45


def load_processed_incidents():
    if not STATE_FILE.exists():
        return {}

    with STATE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_processed_incidents(processed_incidents):
    with STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(processed_incidents, file, indent=4)


def build_incident_assignment_key(incident):
    incident_number = incident["incident_number"]
    assigned_to = incident["assigned_to"]

    return f"{incident_number}|{assigned_to}"


def is_already_notified(incident, processed_incidents):
    assignment_key = build_incident_assignment_key(incident)

    return assignment_key in processed_incidents


def mark_as_notified(incident, processed_incidents):
    assignment_key = build_incident_assignment_key(incident)

    processed_incidents[assignment_key] = {
        "incident_number": incident["incident_number"],
        "assigned_to": incident["assigned_to"],
        "state": incident["state"],
        "sys_id": incident["sys_id"],
        "notified_at": datetime.now().isoformat(timespec="seconds"),
    }

    save_processed_incidents(processed_incidents)


def cleanup_old_processed_incidents(processed_incidents):
    cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)

    cleaned_incidents = {}

    for assignment_key, details in processed_incidents.items():
        notified_at_text = details.get("notified_at")

        if not notified_at_text:
            cleaned_incidents[assignment_key] = details
            continue

        try:
            notified_at = datetime.fromisoformat(notified_at_text)
        except ValueError:
            cleaned_incidents[assignment_key] = details
            continue

        if notified_at >= cutoff_date:
            cleaned_incidents[assignment_key] = details

    save_processed_incidents(cleaned_incidents)

    return cleaned_incidents