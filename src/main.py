import os
import requests
import schedule
import time
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load secrets from .env
load_dotenv()
API_KEY = os.getenv("GOLDAPI_KEY")
TARGET_PRICE_22K = float(os.getenv("TARGET_PRICE_22K", "124.0"))
SENDER_EMAIL = os.getenv("GMAIL_EMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECEIVER_EMAIL = SENDER_EMAIL  # You can change if you want to send to another email

# --- Function to fetch 22K gold price from GoldAPI ---
def get_gold_price_22k():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    price_22k = data["price_gram_22k"]
    return round(price_22k, 2)

# --- Function to send email ---
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📧 Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# --- Function to check gold price and alert ---
def check_price():
    try:
        price = get_gold_price_22k()
        print(f"Current 22K Gold Price: ${price} per gram")
        
        if price <= TARGET_PRICE_22K:
            print("📢 ALERT! Gold price dropped below target!")
            subject = "Gold Price Alert!"
            body = f"22K Gold price dropped below ${TARGET_PRICE_22K}!\nCurrent price: ${price}"
            send_email(subject, body)
        else:
            print("Price is above target. No alert.")
    
    except Exception as e:
        print("Error:", e)

# --- Schedule the agent to run every 8 hours ---
schedule.every(8).hours.do(check_price)

print("Gold price agent is running...")
check_price()  # Run immediately on start

while True:
    schedule.run_pending()
    time.sleep(1)
