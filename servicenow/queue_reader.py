import requests

from config import (
    SERVICENOW_BASE_URL,
    SERVICENOW_ASSIGNMENT_GROUP_ID,
)
from servicenow.auth import get_servicenow_access_token


def fetch_incident_queue(access_token):

    url = f"{SERVICENOW_BASE_URL}/api/tracy/v2/table/incident"

    query = (
        f"assignment_group={SERVICENOW_ASSIGNMENT_GROUP_ID}"
        "^sys_created_onBETWEENjavascript:gs.beginningOfLastMonth()"
        "@javascript:gs.endOfToday()"
        "^stateIN1,2,3"
    )

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    params = {
        "query": query,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    if response.status_code == 404 and "No records found" in response.text:
        return {
            "result": {
                "status": "Success",
                "data": [],
            }
        }

    if not response.ok:
        raise RuntimeError(
            "Unable to fetch ServiceNow incident queue. "
            f"Status: {response.status_code}, "
            f"Response: {response.text}"
        )

    return response.json()

# if __name__ == "__main__":
#     access_token = get_servicenow_access_token()
#
#     queue_response = fetch_incident_queue(
#         access_token=access_token,
#     )
#
#     print("Incident queue fetch successful.")
#     print(queue_response)