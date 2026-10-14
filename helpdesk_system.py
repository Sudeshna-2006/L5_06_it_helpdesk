"""Helpdesk ticketing system ."""

import json
import os
import re
import subprocess
from datetime import datetime

tickets = {}
ticket_state = {"counter": 100}
ADMIN_PASSWORD = os.getenv("HELPDESK_ADMIN_PASSWORD", "")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket and optionally record its creation in an audit trail."""
    try:
        priority = int(urgency)
    except (TypeError, ValueError) as error:
        raise ValueError("Urgency must be an integer from 1 to 5.") from error

    if not 1 <= priority <= 5:
        raise ValueError("Urgency must be between 1 and 5.")

    ticket_state["counter"] += 1
    ticket_id = ticket_state["counter"]
    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }

    if audit_trail is not None:
        audit_trail.append(
            f"{user} raised #{ticket_id} at {datetime.now()}"
        )

    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign an existing ticket to a technician."""
    if ticket_id not in tickets:
        raise KeyError(f"Ticket {ticket_id} does not exist.")
    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to an existing ticket."""
    if ticket_id not in tickets:
        raise KeyError(f"Ticket {ticket_id} does not exist.")
    tickets[ticket_id]["notes"].append(note)


def close_ticket(ticket_id, password):
    """Close a ticket if the configured administrator password matches."""
    if not ADMIN_PASSWORD:
        raise RuntimeError(
            "Set the HELPDESK_ADMIN_PASSWORD environment variable first."
        )
    if password != ADMIN_PASSWORD:
        raise PermissionError("Invalid administrator password.")
    if ticket_id not in tickets:
        raise KeyError(f"Ticket {ticket_id} does not exist.")
    del tickets[ticket_id]


def unresolved_high_priority():
    """Return IDs of unassigned tickets with priority 4 or 5."""
    return [
        ticket_id
        for ticket_id, ticket in tickets.items()
        if ticket["priority"] >= 4 and ticket["tech"] is None
    ]


def ping_user_machine(hostname):
    """Ping a valid hostname without invoking a shell."""
    if not re.fullmatch(r"[A-Za-z0-9.-]+", hostname):
        raise ValueError("Invalid hostname.")

    return subprocess.run(
        ["ping", "-n", "1", hostname] if os.name == "nt"
        else ["ping", "-c", "1", hostname],
        check=False,
        shell=False,
        capture_output=True,
        text=True,
        timeout=5,
    )


def save_tickets(file="tickets.json"):
    """Save all open tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(tickets, output_file, indent=2)


def main():
    """Run a demonstration of the helpdesk ticketing system."""
    first_ticket = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    third_ticket = raise_ticket("joe", "vpn", "2")

    assign_ticket(first_ticket, "Tech-Kiran")
    add_note(first_ticket, "Printer troubleshooting started")

    print("Unassigned high priority:", unresolved_high_priority())

    while True:
        level = input(
            "Urgency for a new laptop ticket (1-5, Enter for 3): "
        ).strip() or "3"

        try:
            raise_ticket("sana", "laptop", level)
            break
        except ValueError as error:
            print(error)

    if ADMIN_PASSWORD:
        close_ticket(third_ticket, ADMIN_PASSWORD)
    else:
        print(
            "Ticket remains open: set HELPDESK_ADMIN_PASSWORD "
            "to enable administrator actions."
        )

    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()
