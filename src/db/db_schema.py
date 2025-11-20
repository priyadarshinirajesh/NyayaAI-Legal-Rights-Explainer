# src/db/db_schema.py
# provides helper to inspect DB; used optionally by admin tools

import sqlite3
from pathlib import Path
DB_PATH = Path("data/legal.db")

def print_stats():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cnt = cur.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print("Chunks:", cnt)
    sources = cur.execute("SELECT source, COUNT(*) FROM chunks GROUP BY source").fetchall()
    for s in sources:
        print(s[0], s[1])
    conn.close()

if __name__ == "__main__":
    print_stats()

