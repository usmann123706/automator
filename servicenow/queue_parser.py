from servicenow.auth import get_servicenow_access_token
from servicenow.queue_reader import fetch_incident_queue

ALLOWED_INCIDENT_STATES = {
    "assigned",
    "in progress",
}


def extract_relevant_incidents(queue_response):
    result = queue_response.get("result", {})
    incidents = result.get("data", [])

    relevant_incidents = []

    for incident in incidents:
        state_data = incident.get("state", {})
        state_name = state_data.get("displayValue", "").strip()

        if state_name.lower() not in ALLOWED_INCIDENT_STATES:
            continue

        assigned_to_data = incident.get("assigned_to", {})

        relevant_incidents.append(
            {
                "incident_number": incident.get("number", ""),
                "sys_id": incident.get("sys_id", ""),
                "state": state_name,
                "state_value": state_data.get("value", ""),
                "assigned_to": assigned_to_data.get(
                    "displayValue",
                    "",
                ),
                "assigned_to_id": assigned_to_data.get(
                    "value",
                    "",
                ),
            }
        )

    return relevant_incidents

# if __name__ == "__main__":
#     access_token = get_servicenow_access_token()
#
#     queue_response = fetch_incident_queue(
#         access_token=access_token,
#     )
#
#     relevant_incidents = extract_relevant_incidents(
#         queue_response=queue_response,
#     )
#
#     print(f"Relevant incidents found: {len(relevant_incidents)}")
#
#     for incident in relevant_incidents:
#         print(incident)