# from servicenow.auth import get_servicenow_access_token
# from servicenow.incident_reader import fetch_single_incident


def extract_incident_details(response_data, expected_incident_number):
    result = response_data.get("result", {})
    incidents = result.get("data", [])

    if not incidents:
        raise RuntimeError(
            f"Incident {expected_incident_number} not found in response."
        )

    incident = incidents[0]

    actual_incident_number = incident.get("number")
    incident_sys_id = incident.get("sys_id")

    if actual_incident_number != expected_incident_number:
        raise RuntimeError(
            "Incident number mismatch. "
            f"Requested: {expected_incident_number}, "
            f"Received: {actual_incident_number}"
        )

    if not incident_sys_id:
        raise RuntimeError(
            f"Sys Id not found of Incident {expected_incident_number}."
        )

    return {
        "incident_number": actual_incident_number,
        "sys_id": incident_sys_id,
        "state": incident.get("state", {}).get("displayValue", ""),
        "assignment_group": incident.get(
            "assignment_group", {}
        ).get("displayValue", ""),
        "assigned_to": incident.get(
            "assigned_to", {}
        ).get("displayValue", ""),
        "priority": incident.get("priority", ""),
    }

# if __name__ == "__main__":
#     incident_number = "INC9523238"
#
#     access_token = get_servicenow_access_token()
#
#     response_data = fetch_single_incident(
#         access_token=access_token,
#         incident_number=incident_number,
#     )
#
#     incident_details = extract_incident_details(
#         response_data=response_data,
#         expected_incident_number=incident_number,
#     )
#
#     print("Incident parsing successful.")
#     print(incident_details)