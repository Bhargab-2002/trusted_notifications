from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class NotificationLog(db.Model):
    __tablename__ = "notification_logs"

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    device_token = db.Column(db.String(120))
    message = db.Column(db.Text)
    status = db.Column(db.String(20))  # Delivered / Failed
    final_channel_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChannelAttempt(db.Model):
    __tablename__ = "channel_attempts"

    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(
        db.Integer, db.ForeignKey("notification_logs.id"), nullable=False
    )
    channel = db.Column(db.String(20))  # SMS / EMAIL / PUSH / INBOX
    status = db.Column(db.String(20))   # success / failed
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notification = db.relationship("NotificationLog", backref="attempts")
