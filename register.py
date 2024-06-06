import sqlite3
import re


# username
def check_username_format(username:str):
    database = sqlite3.connect("userdb.db")
    pattern = re.compile(r"^[a-zA-Z0-9_.]+$")
    database.close()
    return bool(pattern.match(username))

def check_username(username:str):
    database = sqlite3.connect("userdb.db")
    result = database.execute("select * from USER where username=?", (username,)).fetchone()
    database.close()
    if len(username) < 5 or len(username) > 20:
        return "username length must be from 5 to 20 characters"
    if not check_username_format(username):
        return "username can only use letters numbers underscores and periods"
    if result is not None:
        return "username isn't available"

# email
def check_email_format(email:str):
    database = sqlite3.connect("userdb.db")
    email_regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    database.close()
    return re.match(email_regex, email) is not None


def check_email(email:str):
    database = sqlite3.connect("userdb.db")
    result = database.execute("select * from USER where email=?", (email,)).fetchone()
    database.close()
    if not check_email_format(email):
        return "format of the email address isn't correct"
    if result is not None:
        return "email isn't available"
    
# password

def check_password(password:str):
    if not all(126 >= ord(c) >= 32 for c in password):
        return "password contains non-ASCII encoded characters or non-printable characters"

# register

def register(username:str, email:str, password:str) -> str:
    check_username_result = check_username(username)
    check_email_result    = check_email(email)
    check_password_result = check_password(password)

    if check_username_result is not None:
        return check_username_result
    if check_email_result is not None:
        return check_email_result
    if check_password_result is not None:
        return check_password_result
    try:
        database = sqlite3.connect("userdb.db")
        database.execute("INSERT INTO USER (username, email, password) VALUES (?, ?, ?)",
                        (username, email, password))
        database.commit()
        database.close()
        return "register successfully, redirecting to login..."
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return "error"