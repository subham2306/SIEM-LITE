from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_logs():
    conn = sqlite3.connect("../logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, source_ip, message, severity FROM logs ORDER BY timestamp DESC LIMIT 20")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_top_attackers():
    conn = sqlite3.connect("../logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT source_ip, COUNT(*) as count FROM logs WHERE source_ip != 'Unknown' GROUP BY source_ip ORDER BY count DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route("/")
def index():
    logs = get_logs()
    attackers = get_top_attackers()
    ips = [a[0] for a in attackers]
    counts = [a[1] for a in attackers]
    return render_template("dashboard.html", logs=logs, ips=ips, counts=counts)

if __name__ == "__main__":
    app.run(debug=True)

