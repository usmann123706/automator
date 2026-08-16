import requests

from config import (
    SERVICENOW_BASE_URL,
    SERVICENOW_INCIDENT_API_PATH,
)

from servicenow.auth import get_servicenow_access_token


def fetch_single_incident(access_token, incident_number):
    url = (
        f"{SERVICENOW_BASE_URL}"
        f"{SERVICENOW_INCIDENT_API_PATH}"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    params = {
        "query": f"number={incident_number}",
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            "Single incident fetch failed. "
            f"Incident: {incident_number}, "
            f"Status: {response.status_code}, "
            f"Response: {response.text}"
        )

    return response.json()

# if __name__ == "__main__":
#     token = get_servicenow_access_token()
#
#     incident_number = "INC9523238"
#
#     incident_response = fetch_single_incident(
#         access_token=token,
#         incident_number=incident_number,
#     )
#
#     print("Single incident fetch successful.")
#     print(incident_response)