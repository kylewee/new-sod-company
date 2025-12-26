#!/usr/bin/env python3
"""
SMS Review Request System
Sends automated review requests at Day 0, Day 3, and Day 7
"""

import json
import os
from datetime import datetime, timedelta
from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    REVIEW_LINKS,
    DATABASE_FILE
)

# Initialize Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# SMS Templates
TEMPLATES = {
    "day0": """Hi {name}! Thanks for choosing Sod.Company today. Quick question - how's your new lawn looking? Reply 1-5 (5 = love it!)""",

    "day3_pulse": """Hey {name}, quick check-in! How's the lawn? Reply 1-5 (5 = perfect)""",

    "day3_review": """Awesome! Glad you love it. Would you mind leaving a quick Google review? {link}""",

    "day7_pulse": """Hi {name}, one week check-in! How's everything? Reply 1-5""",

    "day7_review": """Thanks! A quick review helps other {city} homeowners find us: {link}""",

    "low_score_alert": """Thanks for the feedback. We'll call you shortly to make this right."""
}


def load_customers():
    """Load customer database"""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    return {"customers": []}


def save_customers(data):
    """Save customer database"""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_customer(name, phone, city, install_date=None):
    """Add a new customer to the database"""
    data = load_customers()

    customer = {
        "id": len(data["customers"]) + 1,
        "name": name,
        "phone": phone,
        "city": city.lower(),
        "install_date": install_date or datetime.now().strftime("%Y-%m-%d"),
        "pulse_score": None,
        "sms_sent": [],
        "reviewed": False,
        "opted_out": False
    }

    data["customers"].append(customer)
    save_customers(data)
    print(f"Added customer: {name} ({phone}) - {city}")
    return customer


def get_review_link(city):
    """Get the review link for a city"""
    city_lower = city.lower().replace(" ", "-")
    return REVIEW_LINKS.get(city_lower, REVIEW_LINKS["default"])


def send_sms(phone, message):
    """Send SMS via Twilio"""
    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        print(f"  SMS sent to {phone}: {msg.sid}")
        return True
    except Exception as e:
        print(f"  ERROR sending to {phone}: {e}")
        return False


def send_review_request(customer, template_key):
    """Send a review request to a customer"""
    if customer["opted_out"] or customer["reviewed"]:
        return False

    if template_key in customer["sms_sent"]:
        return False

    template = TEMPLATES[template_key]
    link = get_review_link(customer["city"])

    message = template.format(
        name=customer["name"].split()[0],  # First name only
        city=customer["city"].title(),
        link=link
    )

    if send_sms(customer["phone"], message):
        customer["sms_sent"].append(template_key)
        customer["last_sms"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return True
    return False


def update_pulse_score(phone, score):
    """Update customer's pulse score (1-5)"""
    data = load_customers()

    for customer in data["customers"]:
        if customer["phone"] == phone:
            customer["pulse_score"] = score
            save_customers(data)

            if score < 4:
                print(f"⚠️  LOW SCORE ({score}) - {customer['name']} - CALL NOW: {phone}")
            return True
    return False


def mark_reviewed(phone):
    """Mark customer as having left a review"""
    data = load_customers()

    for customer in data["customers"]:
        if customer["phone"] == phone:
            customer["reviewed"] = True
            save_customers(data)
            print(f"Marked as reviewed: {customer['name']}")
            return True
    return False


def opt_out(phone):
    """Opt customer out of future messages"""
    data = load_customers()

    for customer in data["customers"]:
        if customer["phone"] == phone:
            customer["opted_out"] = True
            save_customers(data)
            print(f"Opted out: {customer['name']}")
            return True
    return False


def process_scheduled_messages():
    """Process all scheduled messages (pulse checks + review requests)"""
    data = load_customers()
    today = datetime.now().date()

    print(f"\n{'='*50}")
    print(f"Processing messages - {today}")
    print(f"{'='*50}\n")

    sent_count = 0

    for customer in data["customers"]:
        if customer["opted_out"] or customer["reviewed"]:
            continue

        install_date = datetime.strptime(customer["install_date"], "%Y-%m-%d").date()
        days_since = (today - install_date).days

        print(f"\n{customer['name']} ({customer['city']}) - Day {days_since}")

        # Day 0: Evening pulse check
        if days_since == 0 and "day0" not in customer["sms_sent"]:
            if send_review_request(customer, "day0"):
                sent_count += 1

        # Day 3: Pulse check first
        elif days_since == 3 and "day3_pulse" not in customer["sms_sent"]:
            if send_review_request(customer, "day3_pulse"):
                sent_count += 1

        # Day 7: Pulse check first
        elif days_since == 7 and "day7_pulse" not in customer["sms_sent"]:
            if send_review_request(customer, "day7_pulse"):
                sent_count += 1

    save_customers(data)
    print(f"\n{'='*50}")
    print(f"Sent {sent_count} messages")
    print(f"{'='*50}\n")


def handle_reply(phone, score):
    """Handle customer's pulse score reply and send appropriate follow-up"""
    data = load_customers()

    for customer in data["customers"]:
        if customer["phone"] == phone:
            customer["pulse_score"] = score

            if score >= 4:
                # Happy customer - send review request
                link = get_review_link(customer["city"])
                if "day3_pulse" in customer["sms_sent"] and "day3_review" not in customer["sms_sent"]:
                    msg = TEMPLATES["day3_review"].format(
                        name=customer["name"].split()[0],
                        city=customer["city"].title(),
                        link=link
                    )
                    send_sms(phone, msg)
                    customer["sms_sent"].append("day3_review")
                elif "day7_pulse" in customer["sms_sent"] and "day7_review" not in customer["sms_sent"]:
                    msg = TEMPLATES["day7_review"].format(
                        name=customer["name"].split()[0],
                        city=customer["city"].title(),
                        link=link
                    )
                    send_sms(phone, msg)
                    customer["sms_sent"].append("day7_review")
                print(f"✓ {customer['name']} scored {score} - review request sent")
            else:
                # Unhappy customer - alert and acknowledge
                send_sms(phone, TEMPLATES["low_score_alert"])
                print(f"⚠️  ALERT: {customer['name']} scored {score} - CALL NOW: {phone}")

            save_customers(data)
            return True
    return False


def list_customers():
    """List all customers and their status"""
    data = load_customers()

    print(f"\n{'='*70}")
    print(f"{'Name':<20} {'City':<15} {'Install':<12} {'Score':<6} {'SMS':<15} {'Status'}")
    print(f"{'='*70}")

    for c in data["customers"]:
        status = "✓ Reviewed" if c["reviewed"] else ("Opted out" if c["opted_out"] else "Pending")
        sms = ",".join(c["sms_sent"]) or "None"
        score = c["pulse_score"] or "-"
        print(f"{c['name']:<20} {c['city']:<15} {c['install_date']:<12} {score:<6} {sms:<15} {status}")


# CLI Interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("""
SMS Review System (Pulse-First)

Usage:
  python review_sms.py add "John Smith" "+15551234567" "Houston"
  python review_sms.py reply "+15551234567" 5    # Customer replied with score
  python review_sms.py reviewed "+15551234567"   # Customer left review
  python review_sms.py optout "+15551234567"     # Stop messaging
  python review_sms.py send                      # Process scheduled messages
  python review_sms.py list                      # List all customers

Flow:
  Day 0: "How's your lawn? Reply 1-5"
  Day 3: "Quick check-in! Reply 1-5"
         → If 4-5: Send review link
         → If 1-3: Alert you, no review request
  Day 7: Final check if no response
        """)
        sys.exit(0)

    command = sys.argv[1]

    if command == "add" and len(sys.argv) >= 5:
        add_customer(sys.argv[2], sys.argv[3], sys.argv[4])

    elif command == "reply" and len(sys.argv) >= 4:
        handle_reply(sys.argv[2], int(sys.argv[3]))

    elif command == "reviewed" and len(sys.argv) >= 3:
        mark_reviewed(sys.argv[2])

    elif command == "optout" and len(sys.argv) >= 3:
        opt_out(sys.argv[2])

    elif command == "send":
        process_scheduled_messages()

    elif command == "list":
        list_customers()

    else:
        print("Invalid command. Run without arguments for help.")
