import sqlite3
import struct

def parse_std_msgs_string(blob: bytes) -> str:
    strlen = struct.unpack_from("<I", blob, 4)[0]
    raw = blob[8:8 + strlen]
    if raw.endswith(b"\x00"):
        raw = raw[:-1]
    return raw.decode("utf-8", errors="replace")

conn = sqlite3.connect("mystery_message_0.db3")
cur = conn.cursor()

topic_id = cur.execute("""
    SELECT id FROM topics WHERE name='/draw_commands'
""").fetchone()[0]

rows = cur.execute("""
    SELECT data FROM messages WHERE topic_id=? LIMIT 10
""", (topic_id,)).fetchall()

for i, (blob,) in enumerate(rows, 1):
    print(f"[{i}] {parse_std_msgs_string(blob)}")
