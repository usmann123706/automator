import requests

from config import (
    SERVICENOW_CLIENT_ID,
    SERVICENOW_CLIENT_SECRET,
    SERVICENOW_PASSWORD,
    SERVICENOW_TOKEN_URL,
    SERVICENOW_USERNAME,
)


def get_servicenow_access_token():
    payload = {
        "username": SERVICENOW_USERNAME,
        "password": SERVICENOW_PASSWORD,
        "client_id": SERVICENOW_CLIENT_ID,
        "client_secret": SERVICENOW_CLIENT_SECRET,
        "grant_type": "password",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
        SERVICENOW_TOKEN_URL,
        headers=headers,
        data=payload,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            "ServiceNow authentication failed. "
            f"Status: {response.status_code}, "
            f"Response: {response.text}"
        )

    response_data = response.json()
    access_token = response_data.get("access_token")

    if not access_token:
        raise RuntimeError(
            "ServiceNow access token not found."
        )

    return access_token

# if __name__ == "__main__":
# #     token = get_servicenow_access_token()
# #
# #     print("ServiceNow authentication successful.")
# #     print(f"Token received: {bool(token)}")