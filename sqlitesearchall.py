import sqlite3
import os

file_name = "manifest/world_sql_content_7227d0c5fd50443c8dd9e2e35f353f69.sqlite3"
with sqlite3.connect(file_name) as c:
    c.row_factory = sqlite3.Row
    cursor = c.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for tablerow in cursor.fetchall():
        table = tablerow[0]
        cursor.execute("SELECT * FROM " + table)
        for row in cursor:
            for field in row.keys():
                print(table, field, row[field])