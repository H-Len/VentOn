import sqlite3

connection = sqlite3.connect('db/database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())


cur = connection.cursor()

connection.execute("INSERT INTO posts (title, content, init_mood, post_mood) VALUES(?, ?, ?, ?)",
    ('First mood post', 'Content for the first mood post', 4, 5)
    )

connection.execute("INSERT INTO posts (title, content, init_mood, post_mood) VALUES(?, ?, ?, ?)",
    ('Second post', 'Content for the second post')
    )

connection.commit()
connection.close()