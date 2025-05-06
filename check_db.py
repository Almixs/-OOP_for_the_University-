import sqlite3

conn = sqlite3.connect("nodes.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM nodes")
rows = cursor.fetchall()

print("Вузли в базі даних:")
for row in rows:
    print(row)

conn.close()
