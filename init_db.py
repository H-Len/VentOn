import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())


cur = connection.cursor()

connection.execute("INSERT INTO posts (title, content) VALUES(?, ?)",
    ('First post', 'Content for the first post')
    )

connection.execute("INSERT INTO posts (title, content) VALUES(?, ?)",
    ('Second post', 'Content for the second post')
    )

connection.commit()
connection.close()