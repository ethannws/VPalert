# Vacancy Poster Alert

This project monitors **Vacancy Poster API subscriptions** and sends **email alerts** for accounts with **less than 10 credits remaining**. It runs inside a **Docker container** and supports **scheduled execution** via cron jobs.

## 🔹 Features
✅ Fetches subscription data from Vacancy Poster API  
✅ Identifies accounts with **low credit balance**  
✅ Sends **email alerts** via SMTP  
✅ Securely stores **API credentials** and **SMTP details**  
✅ Fully configurable via **JSON or environment variables**  
✅ **Dockerized** for easy deployment  
✅ Supports **scheduled execution** via cron  

## 🔹 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/vp_alert.git
cd vp_alert
```

### 2️⃣ Configure API Credentials & SMTP
Modify `config.json` with your **API accounts** and **SMTP settings**:
```json
{
  "api_accounts": [
    {"email": "user1@example.com", "password": "password1"},
    {"email": "user2@example.com", "password": "password2"}
  ],
  "smtp_server": "smtp.example.com",
  "smtp_port": 587,
  "sender_email": "alerts@example.com",
  "sender_password": "yourpassword",
  "recipient_email": "recipient@example.com"
}
```

### 3️⃣ Build & Run with Docker
```sh
docker build -t vp_alert .
docker run --rm -e CONFIG_FILE=/app/config.json vp_alert
```

### 4️⃣ Schedule with Cron (Optional)
To run **every day at 8 AM**, open your crontab:
```sh
crontab -e
```
Then add this line:
```sh
0 8 * * * docker run --rm vp_alert
```

## 🔹 License
This project is licensed under the **MIT License**.
