🛡️ SIEM-Lite: Mini Security Information and Event Management (SIEM)

📌 Project Overview
**SIEM-Lite** is an **intermediate-level cybersecurity project** that simulates how a real SIEM works.  
It collects system logs (e.g., failed SSH login attempts), parses them, stores them in a database, and visualizes them on a **Flask dashboard**.  

This project demonstrates key skills useful for security roles:
- 🔎 **Log collection & parsing**
- 🗄️ **Database management (SQLite)**
- 📊 **Security event visualization**
- ⚡ **Real-time attack detection**
⚙️ Features
Collects **SSH authentication logs** from Linux (`journalctl` / `/var/log/auth.log`).
Parses failed login attempts, extracting:
 Timestamp
  - Source IP
  - Attack type (e.g., SSH brute-force)
  - Severity
- Stores events in **SQLite database (`logs.db`).
- Interactive **Flask dashboard** to monitor attacks.
- Can run in **real-time mode** (live log monitoring).
- Extensible to track other events (firewall logs, sudo misuse, etc.).

🏗️ Project Structure
siem-lite/
├── collector/ # Log parser (collects + inserts events into DB)
│ └── log_parser.py
├── dashboard/ # Flask web app (visualizes logs)
│ └── app.py
├── reports/ # Generated reports (future expansion)
├── logs.db # SQLite database storing parsed logs
└── README.md # Project documentation

🚀 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/subham2306/SIEM-LITE.git
cd SIEM-LITE
2️⃣ Create Python virtual environment
python3 -m venv siem-env
source siem-env/bin/activate
3️⃣ Install dependencies
pip install flask sqlite3
4️⃣ Collect logs
Run the log collector to parse SSH failed logins:
cd collector
python3 log_parser.py
Check if logs are stored:
sqlite3 ../logs.db "SELECT * FROM logs LIMIT 5;"
5️⃣ Launch dashboard
cd ../dashboard
python3 app.py
Open 👉 http://localhost:5000 in your browser.
🔥 Live Attack Demo
From an attacker machine:
ssh fakeuser@<server-ip>
