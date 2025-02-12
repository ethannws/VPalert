import os
import sys
import json
import subprocess
import smtplib
import requests
import xml.etree.ElementTree as ET
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Ensure required packages are installed
def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        print(f"\ud83d\udce6 Installing missing package: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_if_missing("requests")

# Load configuration from environment or JSON file
CONFIG_FILE = os.getenv("CONFIG_FILE", "config.json")

try:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"\u274c ERROR: Configuration file {CONFIG_FILE} not found!")
    sys.exit(1)

# Read API accounts
API_ACCOUNTS = config.get("api_accounts", [])

# Read SMTP settings
SMTP_SERVER = os.getenv("SMTP_SERVER", config.get("smtp_server", "smtp.example.com"))
SMTP_PORT = int(os.getenv("SMTP_PORT", config.get("smtp_port", 587)))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", config.get("sender_email", "alerts@example.com"))
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", config.get("sender_password", ""))
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", config.get("recipient_email", "recipient@example.com"))

# Function to clean malformed XML
def clean_xml(xml_text):
    xml_text = xml_text.replace("&", "&amp;")  
    xml_text = xml_text.replace("< ", "&lt; ")  
    xml_text = xml_text.replace(" > ", " &gt; ")  
    xml_text = re.sub(r"[^\x20-\x7E]", "", xml_text)  
    return xml_text

# Store low-credit subscriptions
all_low_credit_subs = []
full_results_output = []

# Iterate through API accounts
for account in API_ACCOUNTS:
    vp_email = account["email"]
    vp_password = account["password"]

    print(f"\nChecking subscriptions for {vp_email}...")

    api_url = f"https://api.vacancyposter.com/api.php?apiaction=getsubs&id={vp_email}&pwd={vp_password}"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        print(f"Successfully retrieved data for {vp_email}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data for {vp_email}: {e}")
        continue

    # Save response for debugging
    debug_filename = f"debug_response_{vp_email}.xml"
    with open(debug_filename, "w", encoding="utf-8") as file:
        file.write(response.text)

    cleaned_xml = clean_xml(response.text)

    try:
        root = ET.fromstring(cleaned_xml)
    except ET.ParseError as e:
        print(f"XML Parsing Error for {vp_email}: {e}")
        continue

    # Find low-credit subscriptions
    low_credit_subs = []
    full_results_output.append(f"\nSubscription List for {vp_email}:")

    for subscription in root.findall("subscription"):
        name = subscription.find("name").text
        remaining_str = subscription.find("remaining").text

        try:
            remaining = int(remaining_str)
        except ValueError:
            print(f"Could not convert remaining credits for {name}: '{remaining_str}'")
            continue

        entry = f"   {name}: {remaining} credits left"
        full_results_output.append(entry)

        if remaining < 10:
            low_credit_subs.append(f"{name} - {remaining} credits left")

    print("\n".join(full_results_output).encode("utf-8", "ignore").decode("utf-8"))

    if low_credit_subs:
        all_low_credit_subs.append(f"{vp_email}\n" + "\n".join(low_credit_subs))

if not all_low_credit_subs:
    print("\nAll accounts have sufficient credits.")
    sys.exit()

# Send email
subject = "Vacancy Poster Low Credit Alert"
body = "The following accounts have subscriptions with less than 10 credits remaining:\n\n" + "\n\n".join(all_low_credit_subs)
body += "\n\nFull Subscription List:\n" + "\n".join(full_results_output)

msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL
msg["Subject"] = subject
msg.attach(MIMEText(body.encode("utf-8", "ignore").decode("utf-8"), "plain"))

try:
    print(f"\nSending email alert to {RECIPIENT_EMAIL} via {SMTP_SERVER}:{SMTP_PORT}...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    
    if SMTP_PORT == 587:
        server.starttls()
        server.ehlo()
    
    if SENDER_PASSWORD.strip():
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    server.quit()
    print(f"Email sent successfully to {RECIPIENT_EMAIL}")
except Exception as e:
    print(f"Failed to send email: {e}")

sys.exit()
