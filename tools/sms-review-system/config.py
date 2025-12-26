# SMS Review System Configuration
# Get credentials from: https://console.twilio.com

TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID"  # Replace with your Twilio SID
TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN"    # Replace with your Twilio token
TWILIO_PHONE_NUMBER = "+1XXXXXXXXXX"     # Your Twilio phone number

# Review links per city (update with your actual Google review links)
REVIEW_LINKS = {
    "houston": "https://g.page/r/YOUR_HOUSTON_LINK/review",
    "phoenix": "https://g.page/r/YOUR_PHOENIX_LINK/review",
    "jacksonville": "https://g.page/r/YOUR_JACKSONVILLE_LINK/review",
    "dallas": "https://g.page/r/YOUR_DALLAS_LINK/review",
    "atlanta": "https://g.page/r/YOUR_ATLANTA_LINK/review",
    # Add more cities as you create Google listings
    "default": "https://g.page/r/YOUR_MAIN_LINK/review"
}

# Database file for tracking
DATABASE_FILE = "customers.json"
