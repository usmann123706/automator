from servicenow.auth import get_servicenow_access_token
from servicenow.queue_reader import fetch_incident_queue
from state_manager import (
    load_processed_incidents,
    is_already_notified,
)

def get_pending_incident_notifications():
    assigned_incidents = get_assigned_incidents()
    processed_incidents = load_processed_incidents()

    pending_incidents = []

    for incident in assigned_incidents:
        if is_already_notified(
            incident=incident,
            processed_incidents=processed_incidents,
        ):
            continue

        pending_incidents.append(incident)

    return pending_incidents

def get_assigned_incidents():
    access_token = get_servicenow_access_token()

    queue_response = fetch_incident_queue(
        access_token=access_token,
    )

    incidents = (
        queue_response
        .get("result", {})
        .get("data", [])
    )

    assigned_incidents = []

    for incident in incidents:
        assigned_to = (
            incident.get("assigned_to", {})
            .get("displayValue", "")
            .strip()
        )

        if not assigned_to:
            continue

        assigned_incidents.append(
            {
                "incident_number": incident.get("number"),
                "assigned_to": assigned_to,
                "state": incident.get("state", {}).get("displayValue", ""),
                "sys_id": incident.get("sys_id"),
            }
        )

    return assigned_incidents

if __name__ == "__main__":
    incidents = get_assigned_incidents()

    print(f"Assigned incidents found: {len(incidents)}")

    for incident in incidents:
        print(incident)