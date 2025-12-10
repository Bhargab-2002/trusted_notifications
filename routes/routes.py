from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func

from models.models import db, NotificationLog, ChannelAttempt
from services.dispatcher import dispatch_notification

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        event_type = request.form.get("event_type")
        phone = request.form.get("phone")
        email = request.form.get("email")
        device_token = request.form.get("device_token")
        message = request.form.get("message")

        if event_type and message:
            dispatch_notification(event_type, phone, email, device_token, message)

        return redirect(url_for("main.dashboard"))

    # Summary stats
    total_notifications = NotificationLog.query.count()
    delivered_count = NotificationLog.query.filter_by(status="Delivered").count()
    failed_count = NotificationLog.query.filter_by(status="Failed").count()

    # Channel usage – number of attempts per channel
    channel_rows = (
        db.session.query(ChannelAttempt.channel, func.count(ChannelAttempt.id))
        .group_by(ChannelAttempt.channel)
        .all()
    )
    channel_usage = ", ".join(f"{row[0]}: {row[1]}" for row in channel_rows) if channel_rows else "No data yet"

    # Event log (newest first)
    logs = NotificationLog.query.order_by(NotificationLog.created_at.desc()).all()

    return render_template(
        "dashboard.html",
        total_notifications=total_notifications,
        delivered_count=delivered_count,
        failed_count=failed_count,
        channel_usage=channel_usage,
        logs=logs,
    )


@bp.route("/clear_logs")
def clear_logs():
    ChannelAttempt.query.delete()
    NotificationLog.query.delete()
    db.session.commit()
    return redirect(url_for("main.dashboard"))
