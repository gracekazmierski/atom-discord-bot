import sqlite3
import os

base_dir = os.path.dirname(__file__)
db_path = os.path.join(base_dir, "atom.db")
schema_path = os.path.join(base_dir, "schema.sql")

conn = sqlite3.connect(db_path)
with open(schema_path) as f:
    conn.executescript(f.read())
conn.commit()
conn.close()

print("✅ Database initialized.")
