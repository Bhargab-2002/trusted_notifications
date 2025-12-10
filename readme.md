# Trusted Notifications - Multi-Channel Notification Dispatcher

A Flask-based notification management system that intelligently routes banking alerts and OTPs across multiple channels (SMS, Email, Push Notifications, and Inbox) based on event type. The system includes a web dashboard to send notifications and track delivery status.

## Features

- **Multi-Channel Delivery**: Automatically routes notifications through SMS, Email, Push Notifications, and In-App Inbox
- **Smart Routing Rules**: Event-based routing configuration (e.g., Fraud Alerts via SMS + Push + Email)
- **Fallback Mechanism**: Tries multiple channels in sequence; stops at first successful delivery
- **Delivery Tracking**: Complete audit trail of all notification attempts with success/failure reasons
- **Web Dashboard**: User-friendly interface to send notifications and view delivery statistics
- **SQLite Database**: Persistent storage of notification logs and channel attempt records
- **Channel Validation**: Built-in validation for phone numbers, email addresses, and device tokens

## Project Structure

```
trusted_notifications/
├── app.py                 # Flask application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── models/
│   └── models.py         # Database models (NotificationLog, ChannelAttempt)
├── routes/
│   └── routes.py         # Flask routes (dashboard, send notification)
├── services/
│   ├── dispatcher.py     # Core notification routing logic
│   └── senders.py        # Channel-specific sender functions
├── templates/
│   ├── layout.html       # Base HTML template
│   ├── dashboard.html    # Main dashboard interface
│   └── send_notification.html  # Notification form
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
└── __pycache__/          # Python cache files
```

## Database Models

### NotificationLog
Stores the primary notification record:
- `event_type`: Type of event (e.g., "Fraud Alert", "Login OTP")
- `phone`, `email`, `device_token`: Recipient contact information
- `message`: Notification content
- `status`: Overall delivery status ("Delivered" or "Failed")
- `final_channel_summary`: Summary of all delivery attempts
- `created_at`: Timestamp

### ChannelAttempt
Logs individual channel delivery attempts:
- `notification_id`: Foreign key to NotificationLog
- `channel`: Channel name (SMS, EMAIL, PUSH, INBOX)
- `status`: Delivery status ("success" or "failed")
- `reason`: Failure reason or success message
- `created_at`: Timestamp

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone/Download the project**
   ```bash
   cd trusted_notifications
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:5500`

## Usage

### Sending a Notification via Dashboard

1. Fill in the notification form with:
   - **Event Type**: Select from predefined types (e.g., "Fraud Alert", "Login OTP")
   - **Phone Number**: 10+ digit phone number (optional, unless SMS is required)
   - **Email**: Valid email address (optional, unless EMAIL is required)
   - **Device Token**: Mobile app device token (optional, unless PUSH is required)
   - **Message**: Notification content

2. Click "Send Notification"

3. The system automatically routes based on event type and attempts delivery through configured channels

### Routing Rules

The system uses predefined routing rules for each event type:

```
"Beneficiary Added Alert" → SMS, PUSH, EMAIL
"Fraud Alert" → SMS, PUSH, EMAIL
"Login OTP" → SMS, PUSH, EMAIL
"Transaction OTP" → SMS, PUSH, EMAIL
"KYC Reminder" → PUSH, SMS
"Monthly Statement" → EMAIL, PUSH
"Low Balance Alert" → PUSH, SMS
"Reward Points Update" → PUSH, EMAIL
Default → SMS (fallback)
```

### Dashboard Features

- **Summary Statistics**: Total notifications sent, delivered count, failed count
- **Channel Usage**: Breakdown of attempts per channel
- **Event Log**: Chronological list of all notifications with delivery status
- **Clear Logs**: Reset all data (use with caution)

## API Endpoints

### GET / (Dashboard)
Renders the main dashboard with notification statistics and event log

### POST / (Send Notification)
Form submission endpoint for sending notifications
- **Parameters**: `event_type`, `phone`, `email`, `device_token`, `message`
- **Action**: Dispatches notification and redirects back to dashboard

### GET /clear_logs
Clears all notification logs and channel attempts from the database

## Configuration

Edit `config.py` to customize settings:

```python
SECRET_KEY = "dev-secret-key"  # Change this in production!
SQLALCHEMY_DATABASE_URI = "sqlite:///notifications.db"  # Database path
```

## How It Works

1. **User submits** a notification via the dashboard form
2. **Dispatcher** creates a NotificationLog record in the database
3. **Router** determines channel sequence based on event_type using ROUTING_RULES
4. **Senders** attempt delivery through each channel in order:
   - SMS: Validates phone number format
   - Email: Validates email address format
   - Push: Validates device token presence
   - Inbox: Always succeeds (in-app storage)
5. **Channel Attempt** records are created for each attempt with status and reason
6. **Fallback logic**: Stops at first successful delivery; if all fail, marks as "Failed"
7. **Dashboard** displays aggregated statistics and logs for monitoring

## Sender Implementations

### SMS Sender
- Validates 10+ digit phone number
- Returns success or failure with reason

### Email Sender
- Validates email format (requires "@" symbol)
- Returns success or failure with reason

### Push Notification Sender
- Validates device token presence
- Auto-succeeds if token provided

### Inbox Sender
- Always succeeds (mock in-app storage)
- Used as fallback for critical notifications

## Future Enhancements

- Integration with real SMS/Email/Push providers (Twilio, SendGrid, Firebase, etc.)
- User authentication and role-based access
- Advanced filtering and search in logs
- Notification templates and scheduled delivery
- Webhook support for external integrations
- Metrics and analytics dashboard
- Rate limiting and throttling

## Security Notes

⚠️ **Development Mode Warning**: 
- The `SECRET_KEY` in `config.py` should be changed before production deployment
- Mock senders always succeed (replace with real provider integrations)
- No authentication implemented; add before production use
- SQLite is suitable for testing; use PostgreSQL/MySQL for production

## Troubleshooting

**Port 5500 already in use**
- Change the port in `app.py`:
  ```python
  app.run(debug=True, port=5501)  # Use different port
  ```

**Database errors**
- Delete `notifications.db` and restart to reinitialize
- Ensure write permissions in the project directory

**Missing dependencies**
- Run: `pip install -r requirements.txt`
- Or manually install: `pip install flask flask-sqlalchemy`

