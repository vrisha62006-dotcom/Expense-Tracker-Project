import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
Create table expenses(
Id integer primary key autoincrement, Name text, Amount integer, Category text, Date text)
""")

conn.commit()
conn.close()