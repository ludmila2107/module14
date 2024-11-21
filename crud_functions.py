import sqlite3

def initiate_db():
	connection = sqlite3.connect("data_base.db")
	cursor = connection.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS Products(
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	description TEXT NOT NULL,
	price INTEGER NOT NULL
	)
	''')

	cursor.execute('''
	CREATE TABLE IF NOT EXISTS Users(
	id INTEGER PRIMARY KEY,
	username TEXT NOT NULL,
	email TEXT NOT NULL,
	age INTEGER,
	balance INTEGER NOT NULL
	)
	''')
	products_table = [
		(1, "Продукт1", "Описание1", 100),
		(2, "Продукт2", "Описание2", 200),
		(3, "Продукт3", "Описание3", 300),
		(4, "Продукт4", "Описание4", 400)
	]
	for product in products_table:
		try:
			cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?,?)", product)
		except sqlite3.IntegrityError:
			continue

	connection.commit()
	connection.close()

initiate_db()



def add_user(username, email, age):
    connection = sqlite3.connect("data_base.db")
    cursor = connection.cursor()
    balance = 1000
    cursor.execute('''
    INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)
    ''', (username, email, age, balance))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect("data_base.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    return user is not None






