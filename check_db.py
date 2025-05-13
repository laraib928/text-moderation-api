import sqlite3

def view_logs():
    conn = sqlite3.connect("moderation.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM moderation_logs")
    rows = cursor.fetchall()
    
    if not rows:
        print("No records found in moderation_logs table.")
        return
    
    print(f"Found {len(rows)} records:")
    print("-" * 80)
    for row in rows:
        print(f"ID: {row['id']}")
        print(f"User: {row['user_id']}")
        print(f"Text: {row['text']}")
        print(f"Decision: {row['decision']} (Confidence: {row['confidence']})")
        print(f"Timestamp: {row['timestamp']}")
        print("-" * 80)
    
    conn.close()

if __name__ == "__main__":
    view_logs()