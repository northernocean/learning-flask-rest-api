import sqlite3

def test1():
    connection = sqlite3.connect("test.db")

    cursor = connection.cursor()

    #create_table = "create table users (id int, username text, password text)"
    #cursor.execute(create_table)

    delete_query = "delete from users"
    cursor.execute(delete_query)

    user = (1, "david", "password1")
    insert_query = "insert into users values(?, ?, ?)"
    cursor.execute(insert_query, user)

    users = [
        (2, "sally", "password2"),
        (3, "margaret", "password3")
    ]
    cursor.executemany(insert_query, users)

    select_query = "select * from users"

    for row in cursor.execute(select_query):
        print(row)

    connection.commit()
    connection.close()

def test2():

    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    # all users
    select_query = "select * from users where username = 'david'"
    for row in cursor.execute(select_query):
        print(row)

    # user david
    select_query = "select * from users where username = ?"
    result = cursor.execute(select_query, ("david",))
    row = result.fetchone()
    print(row)
    
    # a non-existing user
    result = cursor.execute(select_query, ("no-name",))
    row = result.fetchone()
    print(row)
    
    connection.commit()
    connection.close()

if(__name__) == "__main__":
    test2()



