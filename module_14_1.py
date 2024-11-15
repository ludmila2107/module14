import sqlite3
connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')
# for i in range(1, 11):
#     cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',(f'User{i}',f'example1{i}@gmail.com', i*10, 1000))
cursor.execute('UPDATE Users SET balance = 500 WHERE id % 2 !=0')
cursor.execute('DELETE FROM Users WHERE id IN (SELECT id FROM Users WHERE id % 3 = 1)')
cursor.execute('SELECT username, email, age, balance FROM Users WHERE age!=60')
list_users = cursor.fetchall()
for i in list_users:
	username, email, age, balance = i
	print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')


cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")


connection.commit()
connection.close()
