import bcrypt

from model.user import UserCreation
from . import con, cur

def get_password(username):
    cur.execute("select password from users where username = %s", (username,))
    return cur.fetchone()[0]

def is_admin(username):
    cur.execute("select is_admin from users where username = %s", (username,))
    return cur.fetchone()[0]

def create_user(user: UserCreation):
    password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    cur.execute("insert into users (username, password, name, is_admin) values (%s, %s, %s, %s)", (user.username, password, user.name, user.admin))
    con.commit()

def get_users():
    cur.execute("select * from users")
    return cur.fetchall()


def get_user_id_by_username(username):
    cur.execute("select user_id from users where username = %s", (username,))
    return cur.fetchone()[0]
