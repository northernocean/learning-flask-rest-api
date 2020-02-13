import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cmd = "create table if not exists users(id integer primary key, username text, password text);"
cursor.execute(cmd)

cmd = "create table if not exists items(id integer primary key, name text, price real, store_id integer);"
cursor.execute(cmd)

cmd = "delete from users;"
cursor.execute(cmd)

cmd = "delete from items;"
cursor.execute(cmd)

#cmd = "insert into users values (null, 'david', 'password1');"
#cursor.execute(cmd)

cmd = "insert into items values (null, 'table', 10.99),(null, 'desk', 11.99);"
cursor.execute(cmd)

connection.commit()
connection.close()

