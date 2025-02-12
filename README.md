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
git clone https://github.com/ethannws/VPalert.git
cd VPalert
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
  "smtp_port": 25,
  "sender_email": "alerts@example.com",
  "sender_password": "",
  "branch_emails": {
    "BranchA": "brancha@example.com",
    "BranchB": "branchb@example.com"
  },
  "overall_report_email": "admin@example.com"
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

## 📧 Email Message Format
### **Branch-Specific Alerts:**
```plaintext
Subject: Vacancy Poster Low Credit Alert - [Branch Name]

The following subscriptions for [Branch Name] have less than 10 credits remaining:
- [Subscription Name] - [Remaining Credits]

Please email Support with the amount of credits if any you would like added.
Additionally, if you do not use any job boards listed, please let Support know so we can prevent further reminders for those boards. Thank you.
```

### **Overall Report to Admin:**
```plaintext
Subject: Vacancy Poster Overall Low Credit Alert

The following subscriptions across all branches have less than 10 credits remaining:
- [Subscription Name] - [Remaining Credits]
```

## 🔍 Notes
- Ensure that the **SMTP server allows anonymous email relay** if using port 25 without authentication.  
- Verify that the `branch_emails` list covers all expected branch names to **avoid missing alerts**.  
- The **Docker container** is designed to be run as a scheduled job using **cron** or a similar scheduling system.  

## 🔹 License
This project is licensed under the **MIT License**.
