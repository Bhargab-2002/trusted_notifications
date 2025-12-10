def send_sms(phone: str, message: str) -> dict:
    """Simulate SMS sending."""
    if not phone:
        return {"status": "failed", "reason": "No phone number provided"}
    if len(phone) < 10:
        return {"status": "failed", "reason": "Invalid phone number"}
    return {"status": "success", "reason": "SMS delivered"}


def send_email(email: str, message: str) -> dict:
    """Simulate Email sending."""
    if not email:
        return {"status": "failed", "reason": "No email provided"}
    if "@" not in email:
        return {"status": "failed", "reason": "Invalid email address"}
    return {"status": "success", "reason": "Email delivered"}


def send_push(device_token: str, message: str) -> dict:
    """Simulate Push notification sending."""
    if not device_token:
        return {"status": "failed", "reason": "No device token provided"}
    # assume always success if token present
    return {"status": "success", "reason": "Push delivered"}


def send_inbox(user_id: str, message: str) -> dict:
    """Optional: In-app inbox. Here we always 'succeed'."""
    return {"status": "success", "reason": "Stored in secure inbox"}
