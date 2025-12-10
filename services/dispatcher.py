from typing import List
from models.models import db, NotificationLog, ChannelAttempt
from .senders import send_sms, send_email, send_push, send_inbox


# Simple routing configuration based on event type
ROUTING_RULES = {
    "Beneficiary Added Alert": ["SMS", "PUSH", "EMAIL"],
    "Fraud Alert": ["SMS", "PUSH", "EMAIL"],
    "Login OTP": ["SMS", "PUSH", "EMAIL"],
    "Transaction OTP": ["SMS", "PUSH", "EMAIL"],
    "KYC Reminder": ["PUSH", "SMS"],
    "Monthly Statement": ["EMAIL", "PUSH"],
    "Low Balance Alert": ["PUSH", "SMS"],
    "Reward Points Update": ["PUSH", "EMAIL"],
}


def get_channel_sequence(event_type: str) -> List[str]:
    return ROUTING_RULES.get(event_type, ["SMS"])  # default: only SMS


def dispatch_notification(event_type: str,
                          phone: str,
                          email: str,
                          device_token: str,
                          message: str) -> NotificationLog:
    """Core engine: picks channels, sends, logs attempts and final result."""

    # 1. Create base notification record
    notification = NotificationLog(
        event_type=event_type,
        phone=phone,
        email=email,
        device_token=device_token,
        message=message,
        status="Pending",
        final_channel_summary=""
    )
    db.session.add(notification)
    db.session.commit()  # to generate ID

    channels = get_channel_sequence(event_type)
    attempt_summaries = []
    delivered = False

    for channel in channels:
        if channel == "SMS":
            result = send_sms(phone, message)
        elif channel == "EMAIL":
            result = send_email(email, message)
        elif channel == "PUSH":
            result = send_push(device_token, message)
        elif channel == "INBOX":
            result = send_inbox("user-1", message)
        else:
            # unknown channel - skip
            continue

        attempt = ChannelAttempt(
            notification_id=notification.id,
            channel=channel,
            status=result["status"],
            reason=result["reason"]
        )
        db.session.add(attempt)

        summary_piece = f"{channel} {result['status'].capitalize()}"
        attempt_summaries.append(summary_piece)

        if result["status"] == "success":
            delivered = True
            # stop at first success
            break

    # 3. Update notification status and final summary
    notification.status = "Delivered" if delivered else "Failed"
    notification.final_channel_summary = ", ".join(attempt_summaries)
    db.session.commit()

    return notification
