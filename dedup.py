import hashlib
import sqlite3
import sys
from datetime import datetime

DB_PATH = "pipeline_cache.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processed (
            video_hash TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

def check_and_mark(url):
    video_hash = hashlib.sha256(url.encode()).hexdigest()
    conn = init_db()

    row = conn.execute(
        "SELECT timestamp FROM processed WHERE video_hash = ?",
        (video_hash,)
    ).fetchone()

    if row:
        print(f"Already processed on {row[0]}. Skipping.")
        conn.close()
        return 0

    conn.execute(
        "INSERT INTO processed (video_hash, url, timestamp) VALUES (?, ?, ?)",
        (video_hash, url, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()
    print("New video. Proceeding.")
    return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <url>", file=sys.stderr)
        sys.exit(2)
    sys.exit(check_and_mark(sys.argv[1]))
