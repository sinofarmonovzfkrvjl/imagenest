import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS files (name text, file text)"
cursor.execute(create_table)

def add_file(name: str, file: str):
    cursor.execute("INSERT OR REPLACE INTO files (name, file) VALUES (?, ?)", (name, file))
    connection.commit()
    connection.close()
    return True

def get_file(name: str):
    cursor.execute("SELECT * FROM files WHERE name=?", (name,))
    return cursor.fetchall()

def delete_file(name: str):
    cursor.execute("DELETE FROM files WHERE name=?", (name,))
    connection.commit()
    connection.close()
    return True

# print(add_file("test", "this is tests"))

print(delete_file("test"))

# print(get_file("test"))