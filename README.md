# Vacancy Poster Alert System

## 📌 Overview
This script retrieves subscription data from the Vacancy Poster API and sends email alerts to branches and an overall admin if any subscriptions have fewer than **10 credits** remaining. The script is designed to be **Dockerized** and run on a **cron schedule** for automation.

## ✨ Features
✅ Fetches subscription data from the Vacancy Poster API.  
✅ Filters out subscriptions marked as **"NOT USING"**.  
✅ Matches subscription names to predefined branches.  
✅ Sends **individual low-credit alerts** to branch-specific email addresses.  
✅ Sends an **overall report** to an admin email.  
✅ Allows **anonymous SMTP relay** for email sending.  
✅ Runs on **Docker** with scheduled execution via **cron**.  

## 🛠 Configuration
### `config.json` Example:
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
    "Thorne": "thorne@example.com",
    "Wait": "wait@example.com",
    "BranchA": "brancha@example.com",
    "BranchB": "branchb@example.com"
  },
  "overall_report_email": "admin@example.com"
}
```

## 🚀 How It Works
1️⃣ The script retrieves subscription data for each `api_accounts` entry.  
2️⃣ It cleans the data and extracts relevant subscription details.  
3️⃣ If a subscription has **fewer than 10 credits** and matches a branch, it is logged for that branch.  
4️⃣ **Emails are sent:**  
   - **Branch-specific emails**: Lists low-credit subscriptions for that branch.  
   - **Admin report**: Lists all low-credit subscriptions across all branches.  
5️⃣ Emails include a request to **contact support** if credits need to be added or to opt out of reminders for unused job boards.  
6️⃣ **Runs on Docker** and executes via **cron** for scheduled execution.  

## ▶️ Running the Script via Docker
### **Build the Docker Image:**
```sh
docker build -t vpalert .
```

### **Run the Container Manually:**
```sh
docker run --rm vpalert
```

### **Set Up a Cron Job (Automated Execution)**
Create a `crontab` entry to run the script daily:
```sh
0 9 * * * docker run --rm vpalert
```
This will run the script every day at **9 AM**.

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

---

