from incident_monitor import (
    get_pending_incident_notifications,
)
from state_manager import (
    load_processed_incidents,
    mark_as_notified,
    cleanup_old_processed_incidents,
)
from teams_webhook_notifier import send_notification
from user_mapping import USERS


def main():
    pending_incidents = get_pending_incident_notifications()
    processed_incidents = load_processed_incidents()
    processed_incidents = cleanup_old_processed_incidents(
        processed_incidents
    )

    print(f"Pending notifications: {len(pending_incidents)}")

    for incident in pending_incidents:
        incident_number = incident["incident_number"]
        assigned_to = incident["assigned_to"]

        print(
            f"Processing incident {incident_number} "
            f"assigned to {assigned_to}"
        )

        if assigned_to not in USERS:
            print(
                f"Skipping incident {incident_number}. "
                f"No Teams user mapping found for: {assigned_to}"
            )
            continue

        teams_user_id = USERS[assigned_to]

        send_notification(
            incident_number=incident_number,
            assigned_to=assigned_to,
            teams_user_id=teams_user_id,
        )

        mark_as_notified(
            incident=incident,
            processed_incidents=processed_incidents,
        )

        print(
            f"Marked as notified: "
            f"{incident_number} -> {assigned_to}"
        )


if __name__ == "__main__":
    main()