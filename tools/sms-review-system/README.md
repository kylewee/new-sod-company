# SMS Review Request System

Automated review requests via Twilio SMS at Day 0, Day 3, and Day 7.

## Setup

### 1. Install Twilio
```bash
pip install twilio
```

### 2. Get Twilio Credentials
1. Sign up: https://twilio.com (free trial includes $15)
2. Get a phone number
3. Copy Account SID and Auth Token

### 3. Configure
Edit `config.py`:
```python
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+15551234567"
```

### 4. Add Review Links
Edit `config.py` with your Google review links:
```python
REVIEW_LINKS = {
    "houston": "https://g.page/r/xxxxx/review",
    "phoenix": "https://g.page/r/xxxxx/review",
    ...
}
```

## Usage

### Add a customer after installation:
```bash
python review_sms.py add "John Smith" "+15551234567" "Houston"
```

### Record pulse score (1-5):
```bash
python review_sms.py pulse "+15551234567" 5
```
*If score < 4, they won't get review requests*

### Mark as reviewed (stop messages):
```bash
python review_sms.py reviewed "+15551234567"
```

### Opt out customer:
```bash
python review_sms.py optout "+15551234567"
```

### Send all scheduled messages:
```bash
python review_sms.py send
```

### List all customers:
```bash
python review_sms.py list
```

## Automation (Cron)

Run twice daily (morning for Day 3/7, evening for Day 0):

```bash
crontab -e
```

Add:
```
# Morning run (9 AM) - Day 3 and Day 7 messages
0 9 * * * cd /path/to/sms-review-system && python review_sms.py send

# Evening run (7 PM) - Day 0 thank you messages
0 19 * * * cd /path/to/sms-review-system && python review_sms.py send
```

## Flow

1. Job completed → Add customer to system
2. Day 0 (evening) → "Thanks! Leave a review?"
3. Day 3 → "How's the lawn? Review us!"
4. Day 7 → "Last ask!"
5. After review → Mark as reviewed

## Cost

Twilio SMS: ~$0.0079 per message
3 messages per customer = ~$0.024 per customer
1000 customers = ~$24
