import sqlite3


def login(username:str, password:str):
    database = sqlite3.connect("userdb.db")
    try:
        result = database.execute("select * from USER where username=? and password=?", (username, password,)).fetchone()
        database.close()
        if result is None:
            return ("the username or password is incorrect", None)
        id = result[0]
        return ("login successful", id)
    except:
        return ("error", None)

