import sqlite3
import subprocess
import re
from datetime import datetime

DB_PATH = "../logs.db"

# Regex to capture failed SSH logins
FAILED_LOGIN_REGEX = re.compile(
    r'Failed password for (invalid user )?(\w+) from ([\d\.]+) port (\d+)'
)

def parse_journalctl():
    """Parse SSH failed logins from journalctl"""
    try:
        # Run journalctl and capture sshd logs
        output = subprocess.check_output(
            ["journalctl", "-u", "ssh", "--no-pager", "-n", "500"],  # last 500 logs
            text=True,
            errors="ignore"
        )
    except subprocess.CalledProcessError as e:
        print(f"[-] Error reading journalctl: {e}")
        return []

    events = []
    for line in output.splitlines():
        match = FAILED_LOGIN_REGEX.search(line)
        if match:
            user = match.group(2)
            ip = match.group(3)

            # Extract timestamp from the beginning of the line
            try:
                parts = line.split()
                ts_str = " ".join(parts[0:3])  # e.g. Sep 17 21:29:31
                ts = datetime.strptime(ts_str, "%b %d %H:%M:%S")
                # Replace year since journalctl omits it
                ts = ts.replace(year=datetime.now().year)
                timestamp = ts.isoformat(" ")
            except Exception:
                timestamp = datetime.now().isoformat(" ")

            events.append((timestamp, "ssh_failed_login", ip, line, "medium"))
    return events

def insert_into_db(events):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for event in events:
        cursor.execute(
            "INSERT INTO logs (timestamp, log_type, source_ip, message, severity) VALUES (?, ?, ?, ?, ?)",
            event
        )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    events = parse_journalctl()
    if not events:
        print("[-] No failed SSH login events found in journalctl.")
    else:
        insert_into_db(events)
        print(f"[+] Inserted {len(events)} events into database.")

